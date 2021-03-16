# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   alipay.py
@Contact :   tangyisheng2@sina.com
@License :   (C)Copyright 1999-2021, Tang Yisheng

@Modify Time        @Author     @Version        @Description
------------        -------     --------        -----------
2021/2/11     tangyisheng2        1.0             数据库链接
"""
from helper import base
import os
import re
import pandas as pd
import datetime


class AliPay(base.TransactionBase):
    def set_init_amount(self, amount):
        self.cur_balance = {"支付宝总资产": amount}

    def _find_date(self):
        """
        从文件名中提取日期
        :return:
        """
        csv = pd.read_csv(self.path, encoding="gbk", nrows=3, header=None)
        time_data = csv.iloc[2]
        pattern = re.compile(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
        date = re.findall(pattern, time_data[0])
        self.start_date = datetime.datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S")
        self.end_date = datetime.datetime.strptime(date[1], "%Y-%m-%d %H:%M:%S")

    def read(self, path):
        """
        在目录中搜索微信支付的账单
        :return:
        """
        file_names = os.listdir(path)
        for name in file_names:
            if "alipay_record" in name:
                self.name = name
                self.path = os.path.join(path, self.name)
                self._find_date()
                break

        self.transactions = pd.read_csv(self.path, header=4, encoding="gbk").iloc[0:-7]

    def _pre_process(self):
        """
        文件预处理
        0. 清除column和数据的的空格
        1. 交易时间约整到日
        2. 交易金额转为float
        :return:
        """
        new_column = dict()
        for index in range(0, self.transactions.columns.__len__() - 1):
            new_column.update({self.transactions.columns[index]: self.transactions.columns[index].rstrip(" ")})
        self.transactions = self.transactions.rename(columns=new_column)
        for column_head in self.transactions.columns:
            try:
                self.transactions[column_head] = self.transactions[column_head].str.strip()  # 去掉数据的空格
            except AttributeError:
                continue
        # 交易时间约整到日
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        for index in range(0, self.transactions["交易创建时间"].__len__()):
            # self.transactions["交易创建时间"][index] = re.match(pattern, self.transactions["交易创建时间"][index]).group()
            self.transactions.loc[index, "交易创建时间"] = re.match(pattern, self.transactions.loc[index, "交易创建时间"]).group()
        # 交易净额转为float
        for index in range(0, self.transactions["金额（元）"].__len__()):
            # self.transactions["金额（元）"][index] = round(self.transactions["金额（元）"][index], 2)
            self.transactions.loc[index, "金额（元）"] = round(self.transactions.loc[index, "金额（元）"], 2)

    def summarize(self):
        """
        整合同天相同消费
        :return:
        """
        self._pre_process()
        summarized_date = list(set(self.transactions["交易创建时间"]))
        summarized_date.sort()  # 时间排序
        result = pd.DataFrame(index=summarized_date, columns=["支付宝总资产"])
        for date in summarized_date:
            all_account = self.transactions[self.transactions["交易创建时间"] == date].copy()
            income = all_account[all_account["资金状态"] == "已收入"]["金额（元）"].copy().sum()
            expenses = all_account[all_account["资金状态"] == "已支出"]["金额（元）"].copy().sum()
            self.cur_balance["支付宝总资产"] = round(self.cur_balance["支付宝总资产"] + expenses - income, 2)
            result.loc[date] = self.cur_balance["支付宝总资产"]  # 保留两位小数
        self.summary = result
        pass


if __name__ == '__main__':
    test = AliPay()
    test.read("../input")
    test.summarize()
    pass
