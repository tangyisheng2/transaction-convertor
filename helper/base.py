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
from datetime import datetime


class TransactionBase:
    name = str
    path = str
    start_date = datetime.date
    end_date = datetime.date
    transactions = pd.DataFrame
    summary = pd.DataFrame
    cur_balance = dict

    def _set_start_end_date(self, start, end):
        """
        设置开始结束时间
        :param start: 开始时间(YYYY-MM-DD)
        :param end: 结束时间(YYYY-MM-DD)
        :return:
        """
        self.start_date = datetime.strptime(start, "%Y-%m-%d")
        self.end_date = datetime.strptime(end, "%Y-%m-%d")
