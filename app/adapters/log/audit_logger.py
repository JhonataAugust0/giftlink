import os
import logging
from typing import Optional
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone, timedelta


class AuditLogger:
    """
    Singleton logger class for comprehensive audit logging with multiple handlers.
    
    Provides a centralized logging mechanism with configurable options for 
    logging to console and file with rotating file support.
    """
    
    _instance = None
    _logger = None

    def __new__(cls, 
                log_dir: str = './logs/', 
                log_file: str = 'audit.log', 
                max_log_size: int = 10 * 1024 * 1024,  # 10 MB default
                backup_count: int = 5):
        """
        Singleton implementation with optional log configuration.
        
        Args:
            log_dir (str): Directory to store log files. Defaults to 'logs'.
            log_file (str): Name of the log file. Defaults to 'audit.log'.
            max_log_size (int): Maximum size of log file before rotation. Defaults to 10 MB.
            backup_count (int): Number of backup log files to keep. Defaults to 5.
        """
        # Ensure only one instance is created
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._logger = cls._configure_logger(log_dir, log_file, max_log_size, backup_count)
        
        return cls._instance

    @classmethod
    def _configure_logger(cls, 
                           log_dir: str, 
                           log_file: str, 
                           max_log_size: int, 
                           backup_count: int):
        """
        Configure logger with console and file handlers.
        
        Args:
            log_dir (str): Directory for log files
            log_file (str): Name of log file
            max_log_size (int): Maximum log file size
            backup_count (int): Number of backup log files
        
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Create logger
        logger = logging.getLogger('AuditLogger')
        logger.setLevel(logging.DEBUG)
        

        # Custom timezone-aware formatter
        class TimezoneFormatter(logging.Formatter):
            def converter(self, timestamp):
                # Convert UTC time to UTC-3
                dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                return dt.astimezone(timezone(timedelta(hours=-3)))
            
            def formatTime(self, record, datefmt=None):
                dt = self.converter(record.created)
                return dt.strftime(datefmt or '%Y-%m-%d %H:%M:%S')
        
        formatter = TimezoneFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # File Handler with Rotation
        file_path = os.path.join(log_dir, log_file)
        file_handler = RotatingFileHandler(
            file_path, 
            maxBytes=max_log_size, 
            backupCount=backup_count
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger

    def log_info(self, message: str, function_name: str, id: Optional[str | int] = None, params: Optional[list] = None):
      """
      Log an informational message.

      Args:
          message (str): The main message to log.
          function_name (str): Name of the function where the log is being made.
          id (Optional[str | int]): Optional identifier for traceability (e.g., user ID or session ID).
          params (Optional[dict]): Additional parameters to include in the log for context.
      """
      log_message = f"[Function: {function_name}] [Message: {message}]"
      
      # Add the user/session ID if provided
      if id:
          log_message += f" [User/Session ID: {id}]"
      
      if params:
          params_str = ", ".join(f"{key}={value}" for key, value in params.items())
          log_message += f" [Params: {params_str}]"

      self._logger.info(log_message)
    
    def log_warning(self, message: str, function_name: str, id: Optional[str | int] = None, params: Optional[list] = None):
        """
        Log a warning message.
        
        Args:
          message (str): The main message to log.
          function_name (str): Name of the function where the log is being made.
          id (Optional[str | int]): Optional identifier for traceability (e.g., user ID or session ID).
          params (Optional[dict]): Additional parameters to include in the log for context.
      """
        log_message = f"[Function: {function_name}] [Message: {message}]"
      
        if id:
            log_message += f" [User/Session ID: {id}]"
        
        if params:
            params_str = ", ".join(f"{key}={value}" for key, value in params.items())
            log_message += f" [Params: {params_str}]"
        self._logger.warning(log_message)

    def log_error(self, message: str, function_name: str, error: str, id: Optional[str | int] = None, params: Optional[list] = None):
        """
        Log an error message.
        
        Args:
          message (str): The main message to log.
          function_name (str): Name of the function where the log is being made.
          id (Optional[str | int]): Optional identifier for traceability (e.g., user ID or session ID).
          params (Optional[dict]): Additional parameters to include in the log for context.
      """
        log_message = f"[Function: {function_name}] [Message: {message}] [Error: {error}]"
      
        # Add the user/session ID if provided
        if id:
            log_message += f" [User/Session ID: {id}]"
        
        if params:
            params_str = ", ".join(f"{key}={value}" for key, value in params.items())
            log_message += f" [Params: {params_str}]"
        self._logger.error(log_message)