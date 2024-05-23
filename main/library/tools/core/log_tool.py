import sys, os, pytest
sys.path.insert(0, os.path.abspath("."))
from datetime import datetime

class LogTool:
    """
    A utility class for logging messages with different log levels.
    """

    def __init__(self):
        """
        Initializes a new instance of the LogTool class.
        The log level is determined by the LOG_LEVEL environment variable.
        If the variable is not set, the default log level is 'debug'.
        """
        self.log_level = os.getenv("LOG_LEVEL", "debug")

    def info(self, msg: str) -> None:
        """
        Logs an informational message.

        Args:
            msg (str): The message to be logged.
        """
        if self.log_level == "debug":
            self._log("[INFO]", msg)

    def warn(self, msg: str) -> None:
        """
        Logs a warning message.

        Args:
            msg (str): The message to be logged.
        """
        if self.log_level in ["debug", "warning"]:
            self._log("[WARN]", msg)

    def error(self, msg: str) -> None:
        """
        Logs an error message.

        Args:
            msg (str): The message to be logged.
        """
        if self.log_level in ["debug", "warning", "error"]:
            self._log("[ERROR]", msg, to_stderr=True)

    def _log(self, tag: str, msg: str, to_stderr: bool = False) -> None:
        """
        Logs a message with the specified tag.

        Args:
            tag (str): The tag to be included in the log message.
            msg (str): The message to be logged.
            to_stderr (bool, optional): Whether to log the message to stderr. Defaults to False.
        """
        log_msg = f"{datetime.now()} {tag} {msg}"
        if to_stderr:
            print(log_msg, file=sys.stderr)
        else:
            print(log_msg)