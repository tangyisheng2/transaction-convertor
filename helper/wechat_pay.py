# !/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   wechat_pay.py
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


class WechatPay(base.TransactionBase):
    def set_init_amount(self, lingqian, lingqiantong):
        self.cur_balance = {"零钱": lingqian, "零钱通": lingqiantong}

    def _find_date(self):
        """
        从文件名中提取日期
        :return:
        """
        pattern = re.compile(r'\d{8}')
        date_list = re.findall(pattern, self.name)
        self.start_date = date_list[0]
        self.end_date = date_list[1]

    def read(self, path):
        """
        在目录中搜索微信支付的账单
        :return:
        """
        file_names = os.listdir(path)
        for name in file_names:
            if "微信支付账单" in name:
                self.name = name
                self.path = os.path.join(path, self.name)
                self._find_date()
                break
        self.transactions = pd.read_csv(self.path, header=16)

    def _pre_process(self):
        """
        文件预处理
        1. 交易时间约整到日
        2. 交易金额转为float
        :return:
        """
        pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
        for index in range(0, self.transactions["交易时间"].__len__()):
            self.transactions["交易时间"][index] = re.match(pattern, self.transactions["交易时间"][index]).group()
        for index in range(0, self.transactions["金额(元)"].__len__()):
            self.transactions["金额(元)"][index] = float(self.transactions["金额(元)"][index].lstrip("¥"))

    def date_summarize(self):
        """
        整合同天相同消费
        :return:
        """
        summarized_date = list(set(self.transactions["交易时间"]))
        summarized_date.sort()  # 时间排序
        result = pd.DataFrame(index=summarized_date, columns=["零钱", "零钱通"])
        for date in summarized_date:
            all_account = self.transactions[self.transactions["交易时间"] == date]
            lingqian_account = all_account[all_account["支付方式"] == "零钱"]
            if lingqian_account.empty:
                lingqian_expense, lingqian_income = 0, 0
            else:
                lingqian_expense = lingqian_account[lingqian_account["收/支"] == "支出"]["金额(元)"].sum()
                lingqian_income = lingqian_account[lingqian_account["收/支"] == "收入"]["金额(元)"].sum()
            lingqiantong_account = all_account[all_account["支付方式"] == "零钱通"]
            if lingqiantong_account.empty:
                lingqiantong_expense, lingqiantong_income = 0, 0
            else:
                lingqiantong_expense = lingqiantong_account[lingqiantong_account["收/支"] == "支出"]["金额(元)"].sum()
                lingqiantong_income = lingqiantong_account[lingqiantong_account["收/支"] == "收入"]["金额(元)"].sum()
            lingqian_balance = round(self.cur_balance["零钱"] + lingqian_income - lingqian_expense, 2)
            lingqiantong_balance = round(self.cur_balance["零钱通"] +lingqiantong_income - lingqiantong_expense, 2)
            result.loc[date] = [lingqian_balance, lingqiantong_balance]  # 保留两位小数
        self.summary = result


if __name__ == '__main__':
    test = WechatPay()
    test.read("../input")
    test.set_init_amount(lingqian=0,lingqiantong=0)
    test._pre_process()
    test.date_summarize()
    pass
