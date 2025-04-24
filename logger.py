################################################################################################
# File: logger.py
#
#
# Author: Randle
#
# Copyright (c) 2024, Randle
#
################################################################################################

import logging

class Color:
    GRAY   = "\x1b[34;20m"
    RED    = "\x1b[31;20m"
    GREEN  = "\x1b[32;20m"
    B_RED  = "\x1b[31;1m"
    YELLOW = "\x1b[33;20m"
    RESET  = "\x1b[0m"
    ITALIC = "\x1b[3m"
    ITALIC_RESET = "\x1b[23m"



class PrettyLogger(logging.Logger):
    def __init__(self, name, level=logging.INFO):
        super().__init__(name, level)
        class CustomFormatter(logging.Formatter):
            if level==logging.INFO:
                format = "%(levelname)8s - %(name)s:: %(message)s"
            else:
                format = "%(levelname)8s - %(name)s:: %(message)s \t\t\t\t " + Color.ITALIC + "(%(filename)s:%(lineno)d)" + Color.ITALIC_RESET

            FORMATS = {
                logging.DEBUG:    Color.GRAY   + format + Color.RESET,
                logging.INFO:     Color.RESET  + format + Color.RESET,
                logging.WARNING:  Color.YELLOW + format + Color.RESET,
                logging.ERROR:    Color.RED    + format + Color.RESET,
                logging.CRITICAL: Color.B_RED  + format + Color.RESET
            }

            def format( self, record):
                log_fmt = self.FORMATS.get(record.levelno)
                formatter = logging.Formatter(log_fmt)
                return formatter.format(record)
            
        handler = logging.StreamHandler()
        handler.setFormatter(CustomFormatter())
        self.addHandler(handler)
        self.propagate= False