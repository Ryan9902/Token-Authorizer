import time
from datetime import datetime
from colorama import Fore , init
from threading import  Lock
from .constants import debug
init()

class Log:
    """
    A class to log messages to the console which i stole from my other project obv
    
    """
    lock = Lock()
    log_file = None 
    @staticmethod
    def set_log_file(filename):
        Log.log_file = open(filename, 'a')

    @staticmethod
    def _log(level, prefix, message):
        timestamp = datetime.fromtimestamp(time.time()).strftime("%H:%M:%S")
        log_message = f"[{Fore.LIGHTBLACK_EX}{timestamp}{Fore.RESET}] {prefix} {message}"

        with Log.lock:
            if Log.log_file:
                Log.log_file.write(log_message + '\n')
                Log.log_file.flush()
            print(log_message)

    @staticmethod
    def Success(message, prefix="(+)", color=Fore.LIGHTGREEN_EX):
        Log._log("SUCCESS", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Error(message, prefix="(-)", color=Fore.LIGHTRED_EX):
        Log._log("ERROR", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Debug(message, prefix="(*)", color=Fore.LIGHTYELLOW_EX):
        if debug:
            Log._log("DEBUG", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Info(message, prefix="(?)" , color=Fore.LIGHTWHITE_EX):
        Log._log("INFO", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def Warning(message, prefix="(!)", color=Fore.LIGHTMAGENTA_EX):
        Log._log("WARNING", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def info(message, prefix="(?)" , color=Fore.LIGHTWHITE_EX):
        Log._log("INFO", f"{color}{prefix}{Fore.RESET}", message)
    
    @staticmethod
    def error(message, prefix="(-)", color=Fore.LIGHTRED_EX):
        Log._log("ERROR", f"{color}{prefix}{Fore.RESET}", message)

    @staticmethod
    def warning(message, prefix="(!)", color=Fore.LIGHTMAGENTA_EX):
        Log._log("WARNING", f"{color}{prefix}{Fore.RESET}", message)
    