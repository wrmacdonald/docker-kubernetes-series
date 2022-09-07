import logging
from typing import Callable, List

import pandas as pd

from errors import key_error_handler


class DataCleaner:
    """Cleans dataset from DataFrame
    
    Modify, add, or drop columns in Pandas DataFrame without modifying the
    original.
    
    Attributes:
        _dataframe(DataFrame): Copy of a Pandas DataFrame
        _date_column_name (str): Name of column containing date data (ex. `MyDateData`)
        _default_rows (int): Number of rows to display when printing out DataFrame
    """
    
    def __init__(self, dataframe: pd.DataFrame, date_column_name: str=None):
        """
        Args:
            dataframe (DataFrame): A Pandas DataFrame
            date_column_name (str): Name of a column containing date data (ex. `MyDateData`)
        """
        self._dataframe = dataframe
        self._date_column_name = date_column_name
        self._default_rows = 5

    @property
    def dataframe(self):
        """DataFrame: Top n rows of dataframe"""
        return self._dataframe
    
    @property
    def date_column_name(self):
        """str: Name of column to use for date methods"""
        return self._date_column_name

    @date_column_name.setter
    def date_column_name(self, value):
        try:
            self._date_column_name = str(value)
        except TypeError:
            logging.error("Column name must be of type str.", exc_info=True)

    @property
    def default_rows(self):
        """int: Top n rows to show when displaying DataFrame"""
        return self._default_rows
    
    @default_rows.setter
    def default_rows(self, value: int):
        self._default_rows = int(value)
        
    def __date_column_extractor(self, column_name: str, date_part_expression: Callable[[pd.Series], int]) -> None:
        """Append a new column to dataframe"""
        self._dataframe[column_name] = self._dataframe[self._date_column_name].apply(date_part_expression)
    
    @key_error_handler
    def convert_date(self, date_format: str = "%d/%m/%Y") -> None:
        """Converts specified column data to datetime format.
        
        Args: 
            date_format (str): strftime to parse time
        
        Returns:
            Pandas series object.
        """
        try:
            self._dataframe[self._date_column_name] = pd.to_datetime(self._dataframe[self._date_column_name], format='%m/%d/%Y')
        except ValueError as ve:
            logging.error('Not a valid datetime column.', exc_info=True)
            raise
            
    @key_error_handler
    def create_year_column(self, new_year_column_name: str = 'year') -> pd.Series:
        """Appends a new column with year data to dataframe.
        
        Args:
            new_year_column_name (str): The name of the new year data column.
            
        Returns:
            A Pandas series object.
        """
        self.__date_column_extractor(new_year_column_name, date_part_expression=lambda x: x.year)
        return self._dataframe[new_year_column_name]
    
    @key_error_handler
    def create_month_column(self, new_month_column_name: str = 'month') -> pd.Series:
        """Appends a new column with month data to dataframe.
        
        Args:
            new_month_column_name (str): The name of the new month data column.
            
        Returns:
            A Pandas Series object.
        """
        self.__date_column_extractor(new_month_column_name, date_part_expression=lambda x: x.month)
        return self._dataframe[new_month_column_name]
    
    @key_error_handler
    def create_day_column(self, new_day_column_name: str = 'day') -> pd.Series:
        """Appends a new column with day data to dataframe
        
        Args:
            new_day_column_name (str): The name of the new day data column.
            
        Returns:
            A Pandas Series object.
        """
        self.__date_column_extractor(new_day_column_name, date_part_expression=lambda x: x.day)
        return self._dataframe[new_day_column_name]
    
    @key_error_handler
    def create_week_of_year_column(self, new_woy_column_name: str = 'weekofyear') -> pd.Series:
        """Appends a new column with week of year data to dataframe
        
        Args:
            new_woy_column_name (str): The name of the new week of year data column.
            
        Returns:
            A Pandas Series object.
        """
        self.__date_column_extractor(new_woy_column_name, date_part_expression=lambda x: x.weekofyear)
        return self._dataframe[new_woy_column_name]
    
    @key_error_handler
    def convert_to_numeric(self, *args, verbose: bool = False) -> None:
        """Converts arbitrary number of columns to numeric type.
        
        Args:
            *args (str): Columns to be converted.
            verbose (bool): If True, prints out copy of converted values.
        """
        for arg in args:
            self._dataframe[arg] = pd.to_numeric(self._dataframe[arg], errors='coerce')
            
                
    def drop_columns(self, drop_list: List[str] = [], errors: str = 'ignore') -> None:
        """Drop list of columns from dataframe.
        
        Args:
            drop_list (list): List of columns to be dropped. Column names should be 
              str format. Default is an empty list.
            errors (str): Whether to ignore errors. Default is `ignore`
        """
        self._dataframe.drop(drop_list, axis=1, inplace=True, errors=errors)