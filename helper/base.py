# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   base.py
@Contact :   tangyisheng2@sina.com
@License :   (C)Copyright 1999-2021, Tang Yisheng

@Modify Time        @Author     @Version        @Description
------------        -------     --------        -----------
2021/2/11     tangyisheng2        1.0           Base Helper
"""
import pandas as pd
import datetime


class TransactionBase:
    name = str
    path = str
    start_date = datetime.date
    end_date = datetime.date
    transactions = pd.DataFrame
    summary = pd.DataFrame
    cur_balance = dict

