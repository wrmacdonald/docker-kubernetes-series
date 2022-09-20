import functools
import logging

def key_error_handler(function):
    """Decorator for capturing KeyErrors in DataCleaner class."""
    
    @functools.wraps(function)
    def _date_error_handler(*args, **kwargs):
        try: 
            return function(*args, **kwargs)
        except KeyError as ke:
            logging.error("The column {} does not exist.".format(ke))
            raise
    return _date_error_handler