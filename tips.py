#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from tips import app
from tips.logging_utils import get_logger

if __name__ == "__main__":
    # Starting the logger
    wecalLogger = get_logger("tips")
    wecalLogger.info("tips started")

    sys.exit(app.run_gui())
