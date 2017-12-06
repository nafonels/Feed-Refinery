#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from setting import logfile

__version__ = "$"

_defaultLogLevel = logging.DEBUG

logger = logging.getLogger('default_logger')
logger.setLevel(_defaultLogLevel)

# StreamHandler -> output is print out to std
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

# create formatter for sh/fh
# and add_method formatter to sh/fh
sh_formatter = logging.Formatter('%(asctime)s [%(module)s] (%(levelname)s)\t: <%(funcName)s>(%(lineno)d) %(message)s',
                                 datefmt = '%Y/%m/%d %H:%M:%S')
sh.setFormatter(sh_formatter)

# add_method sh to logger
logger.addHandler(sh)

# StreamHandler -> output is saved to filename
fh = logging.FileHandler(logfile, 'a', 'utf-8')
fh.setLevel(logging.NOTSET)
fh.setFormatter(sh_formatter)

logger.addHandler(fh)

logger.info("Logger online")
