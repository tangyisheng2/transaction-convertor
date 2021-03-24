# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   cmb.py
@Contact :   tangyisheng2@sina.com
@License :   (C)Copyright 1999-2021, Tang Yisheng

@Modify Time        @Author     @Version        @Description
------------        -------     --------        -----------
2021/3/18     tangyisheng2        1.0             CMB Helper
"""
# 账户管理首页，交易查询
from helper import base
import os
import re
import pandas as pd
import datetime


class CMB(base.TransactionBase):
    # def set_init_amount(self, amount):
    #     """
    #     设定上月余额
    #     :param amount: 初始余额
    #     :return:
    #     """
    #     self.cur_balance = {f"CMB余额": amount}

    def read(self, path):
        """
        在目录中搜索CMB账单
        :param path: 搜索路径
        :return:
        """
        file_names = os.listdir(path)
        for name in file_names:
            if "CMB" in name:
                self.name = name
                self.path = os.path.join(path, self.name)
                self._find_date()
                break

        self.transactions = pd.read_csv(self.path, header=6, index_col=False, encoding="gbk").iloc[:-2]

    def _find_date(self):
        """
        获取账单周期
        :return:
        """
        csv = pd.read_csv(self.path, encoding="gbk", nrows=5, header=None)
        time_data = csv.iloc[-1]
        pattern = re.compile(r'\d{8}')
        date = re.findall(pattern, time_data[0])
        self.start_date = datetime.datetime.strptime(date[0], "%Y%m%d")
        self.end_date = datetime.datetime.strptime(date[1], "%Y%m%d")

    def _find_card_number(self):
        """
        获取卡号
        :return:
        """
        pattern = re.compile("\d{4}")
        card_number = re.findall(pattern, self.name)
        self.card_number = card_number[-1]

    def _pre_process(self):
        """
        文件预处理
        0. 清除数据中的\t
        1. 录入卡号
        :return:
        """
        # 0. 清除 \t
        for column_head in self.transactions.columns:
            try:
                self.transactions[column_head] = self.transactions[column_head].str.replace("\t", "")  # 去掉数据的空格
            except AttributeError:
                continue
        # 1. 录入卡号
        self._find_card_number()

    def _summary(self):
        """
        获取每天最后的银行余额
        :return:
        """
        date_list = set(self.transactions["交易日期"])
        self.summary = pd.DataFrame(index=date_list, columns=[f"CMB({self.card_number})余额"])
        for date in date_list:
            latest_transaction_time = max(self.transactions.loc[self.transactions["交易日期"] == date, "交易时间"])
            index = (self.transactions["交易日期"] == date) & (self.transactions["交易时间"] == latest_transaction_time)
            self.summary.loc[date] = float(self.transactions.loc[index, "余额"])


if __name__ == '__main__':
    test = CMB()
    test.read("../input")
    test._pre_process()
    test._summary()
    pass
