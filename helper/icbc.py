# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   icbc.py
@Contact :   tangyisheng2@sina.com
@License :   (C)Copyright 1999-2021, Tang Yisheng

@Modify Time        @Author     @Version        @Description
------------        -------     --------        -----------
2021/3/16     tangyisheng2        1.0             ICBC Helper
"""
from helper import base
import os
import re
import pandas as pd
import datetime


class ICBC(base.TransactionBase):
    def set_init_amount(self, amount):
        """
        设定上月余额
        :param amount: 初始余额
        :return:
        """
        self.cur_balance = {"ICBC余额": amount}

    def read(self, path):
        """
        在目录中搜索ICBC账单
        :param path: 搜索路径
        :return:
        """
        file_names = os.listdir(path)
        for name in file_names:
            if "hisdetail" in name:
                self.name = name
                self.path = os.path.join(path, self.name)
                self._find_date()
                break

        self.transactions = pd.read_csv(self.path, header=3, index_col=False).iloc[:-1]

    def _find_date(self):
        """
        获取账单周期
        :return:
        """
        pass

    def _pre_process(self):
        """
        文件预处理
        1. 清除空格和制表符
        :return:
        """
        for column in self.transactions.columns:
            try:
                self.transactions[column] = self.transactions[column].str.replace(" ", "")
                self.transactions[column] = self.transactions[column].str.replace("\t", "")
            except AttributeError:
                continue

    def _get_balance(self):
        return self.transactions["余额"]

if __name__ == '__main__':
    test = ICBC()
    test.read("../input")
    test._pre_process()
    pass