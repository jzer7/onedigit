"""A standardized logger for the application."""

import logging
import logging.handlers


# Set loggers quickly, as they are used in multiple places
logging.basicConfig(level=logging.DEBUG)

main_logger = logging.getLogger("onedigit")
main_logger.setLevel(logging.INFO)

# -----------------------------------------------------------
# Configure logging
# * The console will get messages INFO and higher, things
#   we want the user to see right away.
# * The log file will get messages DEBUG and higher,
#   information for post execution analysis
# -----------------------------------------------------------

# Main logger : used only by other libraries
logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Logger for the CLI
main_logger.setLevel(logging.DEBUG)

# create formatters
__fileformatter = logging.Formatter("%(asctime)s, %(name)s, %(levelname)s, %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z")
__consoleformatter = logging.Formatter("%(levelname)s - %(message)s")

# create file handler which logs even debug messages
fh = logging.handlers.RotatingFileHandler(filename="calculate.log", maxBytes=100000, backupCount=5, encoding="utf-8")
fh.setLevel(logging.DEBUG)
fh.setFormatter(__fileformatter)
main_logger.addHandler(fh)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
ch.setFormatter(__consoleformatter)
main_logger.addHandler(ch)
