# -*- coding: utf-8 -*-
import logging, logging.handlers

def get_configured_logger(name):
    logger = logging.getLogger(name)
    if (len(logger.handlers) == 0):
        # This logger has no handlers, so we can assume it hasn't yet been configured
        # (Configure logger)
        logginghandler = False
    return logger

# Assign application logger to a global var  
logger = get_configured_logger(request.application)
