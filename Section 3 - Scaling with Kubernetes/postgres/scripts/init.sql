CREATE TABLE IF NOT EXISTS raleigh_temps(
    MeasurementDate date,
    TempMax float,
    TempMin float,
    TempAvg float,
    TempDeparture float,
    HDD float,
    CDD float,
    Precipitation text,
    NewSnow text,
    SnowDepth text
);

COPY raleigh_temps 
FROM '/var/lib/postgresql/csvs/raleigh_temps.csv'
DELIMITER ',' 
CSV HEADER;
