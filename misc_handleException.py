import datetime
import os
import traceback
from functools import wraps
from PySide6.QtWidgets import  QPlainTextEdit
from PySide6.QtCore import Signal

def exception2msg(ex: Exception):
    '''
    Convert exception object to formatted message string for safe cross-thread transmission.
    Use this before emitting exceptions through Qt signals across threads.
    
    Args:
        ex (Exception): The exception object to convert.
    
    Returns:
        str: Formatted exception message with full traceback details.
    '''
    msg_lines = [f"{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}>>>Traceback Error: {type(ex).__name__}: {ex}"]
    
    exc_tb = ex.__traceback__
    while exc_tb is not None:
        exc_dir = exc_tb.tb_frame.f_code.co_filename
        exc_line = exc_tb.tb_lineno
        exc_func = exc_tb.tb_frame.f_code.co_name
        exc_plain = '\t'.join([f"File: {exc_dir}", f"| Line: {exc_line}", f"| Function: {exc_func}"])
        msg_lines.append(exc_plain)
        exc_tb = exc_tb.tb_next
    
    msg_lines.append("Error End.")
    return '\n'.join(msg_lines)
    

def msg2file(msgline, filename='DevLog', folder='DevLog'):
    '''
    Write message to log file in DevLog folder.
    Creates today's log file if it doesn't exist.
    
    Args:
        msgline (str): The message to write to the log file.
        filename (str, optional): The name of the log file. Defaults to 'DevLog'.
        folder (str, optional): The folder where the log file will be saved. Defaults to 'DevLog'.
    '''
    os.makedirs(folder, exist_ok=True)
    DATE = datetime.date.today().strftime("%Y%m%d")
    with open(fr'.\{folder}\{DATE}-{filename}.txt', 'a') as file:
        file.write(msgline + '\n')


def errorDeco(signal=None, logger=None):
    '''
    Decorator to automatically wrap functions in try-except logic.
    Catches exceptions, converts them to messages, and outputs via logger widget and/or signal.
    
    Usage:
        # With logger widget only
        @errorDeco(logger='self.Log')
        def my_function(self):
            # your code
        
        # With signal only (for thread-safe exception handling)
        @errorDeco(signal='self.logMsg')
        def connectDevice(self):
            # your code
    
    Args:
        signal (str, optional): Attribute path to signal (e.g., 'self.logMsg'). Defaults to None.
        logger (str, optional): Attribute path to logger widget (e.g., 'self.Log'). Defaults to None.
        log_to_file (bool, optional): Whether to write exception to log file. Defaults to True.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                error_msg = exception2msg(ex)
                print(error_msg)
                msg2file(error_msg)
                
                # Emit via signal if specified
                if signal and len(args) > 0:
                    try:
                        # Get the object (usually 'self' from args[0])
                        obj = args[0]
                        # Parse attribute path like 'self.logMsg' → 'logMsg'
                        attr_path = signal.replace('self.', '').split('.')
                        signal_obj = obj
                        for attr in attr_path:
                            signal_obj = getattr(signal_obj, attr)
                        
                        # Emit the message through the signal
                        if hasattr(signal_obj, 'emit'):
                            signal_obj.emit(error_msg)
                    except (AttributeError, IndexError):
                        pass
                
                # Display in logger widget if specified
                if logger and len(args) > 0:
                    try:
                        # Get the object (usually 'self' from args[0])
                        obj = args[0]
                        # Parse attribute path like 'self.Log' → 'Log'
                        attr_path = logger.replace('self.', '').split('.')
                        logger_obj = obj
                        for attr in attr_path:
                            logger_obj = getattr(logger_obj, attr)
                        
                        # Append to logger widget
                        if isinstance(logger_obj, QPlainTextEdit):
                            logger_obj.appendPlainText(error_msg)
                    except (AttributeError, IndexError):
                        pass
        
        return wrapper
    return decorator
