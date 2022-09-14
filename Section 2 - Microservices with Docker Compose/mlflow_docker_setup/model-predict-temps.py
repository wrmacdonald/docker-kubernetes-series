# Databricks notebook source
# MAGIC %md
# MAGIC # Predict Max Temperature from a given data set
# MAGIC The goal for this sprint is to understand feature stores and to build a simple data pipeline.  We'll be using the feature store that is integrated in Databricks.  
# MAGIC The scoring criteria are at the bottom, but in general:
# MAGIC  - Create a feature store table and load the training data into it.  Use the existing database mlops_hackathon_fs.  Your table name should include your userid.
# MAGIC  - Create a separate script or notebook that reads the live data, runs your data cleaning function/class and updates your feature store table.
# MAGIC  - Create a job/workflow to update your feature store table by running the code you created in the step above.
# MAGIC  - Modify the model training code to load and train from the feature store instead of the .csv file.  You should add parameters to specify the training time period to use instead of always assuming all data in the table.
# MAGIC  - Remember to check your code into your user branch
# MAGIC  - By the end of this sprint, you should have at least 3 separate code files.  One for each of the MLOps pipelines discussed so far: data pipeline / feature store, model training pipeline, and inference pipeline
# MAGIC  
# MAGIC ### Helpful Links
# MAGIC - https://docs.databricks.com/applications/machine-learning/feature-store/index.html?utm_source=rafael.pierre&utm_medium=web
# MAGIC - https://docs.databricks.com/applications/machine-learning/feature-store/python-api.html
# MAGIC - https://adb-2033544226399369.9.azuredatabricks.net/?o=2033544226399369#notebook/4308876174313806/command/4308876174313807
# MAGIC - https://docs.microsoft.com/en-us/azure/databricks/_static/notebooks/machine-learning/feature-store-taxi-example.html
# MAGIC - https://databricks.com/blog/2022/05/10/introducing-databricks-workflows.html
# MAGIC - https://docs.microsoft.com/en-us/azure/databricks/data-engineering/jobs/jobs

# COMMAND ----------

##################
# USEFUL CODE BITS
##################

# Use the following 2 lines of code to set the database in which your feature store table will be created.

db_name_fs='mlops_hackathon_fs'
spark.sql(f'USE DATABASE {db_name_fs};')

###
# your code here
# Make sure that the name of the feature store table you create contains your userid
###


# Your feature store table should ingest data from the 'live' table instead of the .csv file used previously
# Use the following 3 lines of code to read in a dataframe from the 'live' table

db_name_live_data='mlops_hackathon'
spark.sql(f'USE DATABASE {db_name_live_data};')
df = spark.table("DailyTempsRaleigh") # this is the ‘live’ table you will read from

###
# your code here
###


# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Libraries

# COMMAND ----------

from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
from mlflow import tracking
import logging
import numpy as np

# COMMAND ----------

dbutils.widgets.dropdown("Test Window (days)", "30", ["7", "14", "30", "60"])

# COMMAND ----------

# MAGIC %md
# MAGIC ## Load Temperature Data

# COMMAND ----------

# this is a static data set for training, but it is a snapshot of real data
temps = spark.read.option("header",True).csv("dbfs:/FileStore/temperature_data_Raleigh_012020_062022.csv")

# COMMAND ----------

temps.show(5)

# COMMAND ----------

# MAGIC %md
# MAGIC ## EDA - Exploritory Data Analysis 
# MAGIC ### (aka Data Munging)

# COMMAND ----------

# prophet expects a pandas df, so we will convert now
pdtemps = temps.toPandas()

# COMMAND ----------

# check data types
pdtemps.dtypes

# COMMAND ----------

def clean_df(df):
    ###################
    # Input: dataframe with columns:
    #   [TempMax, TempMin, TempAvg, TempDeparture, HDD, CDD, Precipitation, NewSnow, SnowDepth]
    # Output: dataframe with columns:
    #   [TempMax, TempMin, TempAvg, year, month, day, weekofyear]
    #
    # Function changes the data type from string to date or numeric and creates helper features such as year, month and day
    ###################
    
    df['MeasurementDate'] = pd.to_datetime(df['MeasurementDate'], format='%m/%d/%Y')
    df['year'] = df['MeasurementDate'].apply(lambda x : x.year)
    df['month'] = df['MeasurementDate'].apply(lambda x : x.month)
    df['day'] = df['MeasurementDate'].apply(lambda x : x.day)
    df['weekofyear'] = df['MeasurementDate'].apply(lambda x : x.weekofyear)
    df['TempMax'] = pd.to_numeric(df['TempMax'],errors='coerce')
    df['TempMin'] = pd.to_numeric(df['TempMin'],errors='coerce')
    df['TempAvg'] = pd.to_numeric(df['TempAvg'],errors='coerce')
    
    # drop the columns we don't need
    df.drop(['TempDeparture', 'HDD', 'CDD', 'Precipitation', 'NewSnow', 'SnowDepth'], axis=1, inplace=True)
    
    return df

# COMMAND ----------

pdtemps = clean_df(pdtemps)
pdtemps.head(3)

# COMMAND ----------

# check for NAs
pdtemps.isna().sum()

# COMMAND ----------

# check min and max dates to see how much this data set covers
print(pdtemps['MeasurementDate'].min())
print(pdtemps['MeasurementDate'].max())

# COMMAND ----------

# plot max temperature overtime
pdtemps.plot("MeasurementDate","TempMax")
plt.show()

# COMMAND ----------

# let's take a looks at the data grouped by month
grp = pdtemps.groupby(["month"])

months = []
means = []
counts = []
for name, group in grp:
    months.append(name)
    means.append(group["TempMax"].mean())
    counts.append(group["TempMax"].count())

# COMMAND ----------

# plot average max temperature by month
fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
ax.bar(months,means)
plt.show()

# COMMAND ----------

# Check the distribution of the data.  Do we have a similar number of entries for each month?
counts

# COMMAND ----------

# The data covers 2.5 years, so the counts per month look about right.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Build Time Series Model

# COMMAND ----------

test_win = int(dbutils.widgets.get("Test Window (days)"))

# COMMAND ----------

# we don't want to train the model on all the data we have
# we want to reserve some so that we can measure how our model performs when compared to real values, so we will filter out the most recent X number of days
trainDF = pdtemps.sort_values(by='MeasurementDate').iloc[0:-test_win]

# COMMAND ----------

trainDF.tail(5)

# COMMAND ----------

# create a df of just the date and temp we want to predict
prophetDF = pd.DataFrame()
prophetDF['ds'] = trainDF["MeasurementDate"]
prophetDF['y'] = trainDF["TempMax"]

# COMMAND ----------

# MAGIC %md
# MAGIC ## Create and Run MLFlow Experiment

# COMMAND ----------

# MAGIC %md
# MAGIC An experiment is a logical grouping of MLFlow runs. A run is a single execution of model code.

# COMMAND ----------

# Create experiment
model_name = "prophet-time-series-model"
USER_ID = dbutils.notebook.entry_point.getDbutils().notebook().getContext().userName().get()
EXPERIMENT_NAME = f"/Users/{USER_ID}/{USER_ID.split('@')[0]}_mlops"
mlflow.set_experiment(EXPERIMENT_NAME)
experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
experiment_id = experiment.experiment_id
print("experiment_id:", experiment_id)

# COMMAND ----------

# MAGIC %md
# MAGIC Run the code below a few times changing the `growth`, `daily_seasonality`, `weekly_seasonality`, and `yearly_seasonality` variables for each run.

# COMMAND ----------

with mlflow.start_run(experiment_id=experiment.experiment_id, run_name="sprint_3") as time_series_tracking_run:
    
    growth = 'flat'
    daily_seasonality = False
    weekly_seasonality = True
    yearly_seasonality = True
    
    # define the model
    m = Prophet(growth=growth, 
              daily_seasonality=daily_seasonality, 
              weekly_seasonality=weekly_seasonality,
              yearly_seasonality=yearly_seasonality
             )
    # https://facebook.github.io/prophet/docs/seasonality,_holiday_effects,_and_regressors.html
    # consider improving model by changing default settings:
    #    growth='linear' or 'flat'
    #    daily_seasonality=True or False,
    #    weekly_seasonality=True or False,
    #    yearly_seasonality=True or False,
    # m.add_seasonality(name='monthly', period=30.5, fourier_order=5)

    # train the model using the df we created
    prophet_time_series_model = m.fit(prophetDF)

    # building a prophet model changes the default logging level, so we will change it back
    logger = spark._jvm.org.apache.log4j
    logging.getLogger("py4j.java_gateway").setLevel(logging.ERROR)
    
    # Log model
    mlflow.prophet.log_model(pr_model=prophet_time_series_model, artifact_path="time-series-model", input_example=prophetDF[:5])
    
    # Log model parameters
    mlflow.log_param('growth', growth)
    mlflow.log_param('daily_seasonality', daily_seasonality)
    mlflow.log_param('weekly_seasonality', weekly_seasonality)
    mlflow.log_param('yearly_seasonality', yearly_seasonality)
    
    # now, predict values for the next X number of days
    futureDF = m.make_future_dataframe(periods=test_win)
    forecastDF = m.predict(futureDF)
    
    # measure model performance using RMSE (root mean squared error)
    # the goal is to minimize the error / RMSE

    # join forecast values with the actual measured values, but only for the last X number of days
    performDF = pd.merge(forecastDF.iloc[-test_win:], pdtemps, left_on="ds", right_on="MeasurementDate")
    # calculate RMSE
    se = np.square(performDF.loc[:, 'yhat'] - performDF.loc[:, 'TempMax'])
    mse = np.mean(se)
    rmse = np.sqrt(mse)
    print("RMSE is:", rmse)
    
    # Log rmse value from this run
    mlflow.log_metric("rmse", rmse)

    # Log artifacts
    fig1 = m.plot(forecastDF)
    fig2 = m.plot_components(forecastDF)
    
    mlflow.log_figure(fig1, 'forecast.png')
    mlflow.log_figure(fig2, 'forecast_components.png')
    

# COMMAND ----------

# MAGIC %md
# MAGIC ## Register Model

# COMMAND ----------

# MAGIC %md
# MAGIC We will now choose our best model to deploy to to the build-in model registry. A model registry is a central location where models are stored facilitating the sharing of expertise and knowledge.

# COMMAND ----------

runs_df = mlflow.search_runs(experiment_id)
display(runs_df)

# COMMAND ----------

# Select the best run based on rmse
client = tracking.MlflowClient()
runs = client.search_runs(experiment_id, order_by=["metrics.rmse ASC"])
best_run_id = runs[0].info.run_id
best_run_id

# COMMAND ----------

# Register your best performing model
model_name = f"prophet-time-series-model"
model_uri = f"runs:/{best_run_id}/time-series-model"
model_details = mlflow.register_model(model_uri=model_uri, name=model_name)

# COMMAND ----------

# Promote your model to staging
client.transition_model_version_stage(
    name=model_details.name,
    version=model_details.version,
    stage="Staging"
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Hackathon Scoring

# COMMAND ----------

# MAGIC %md
# MAGIC You will be evaluated based on the questions below. Each **reviewer** will answer these questions based on your code.
# MAGIC 1. Has a feature store table been created in the mlops_hackathon_fs database (table name should include userid) and is there data in it? Y / N
# MAGIC 2. Is there a separate script or notebook to read from the 'live' data and update the feature store table (aka data pipeline)? Y / N
# MAGIC 3. Is there a job/workflow to run the data pipeline which updates the feature store table from the 'live' data? Y / N
# MAGIC 4. Has the model training code been updated to train from the feature store?  Y / N
# MAGIC 
# MAGIC Link for the reviewer: [Scoring Form](https://forms.office.com/Pages/ResponsePage.aspx?id=EnVjbBfEeE6dYrYSWOS2GZXOPkOh46dDhHfyYHEuItJUNzRPNEdKU1dONjFYNzA2WUcwNUFCQU5CVy4u)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Reviewer Comments

# COMMAND ----------

# Comments
