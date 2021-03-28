#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/3/26 18:19
# @Author  : lockcy
# @File    : logger.py


import logging
import logging.handlers

LOG_FILENAME = 'douyu_task.log'
logger = logging.getLogger(__name__)

logger.setLevel(level=logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILENAME, maxBytes=10485760, backupCount=5, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

