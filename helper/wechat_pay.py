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
        for name in os.listdir(path):
            if "微信支付账单" in name:
                self.name = name
                self._find_date()
                self.path = os.path.join(path, self.name)
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
        summarized_date = set(self.transactions["交易时间"])

        result = pd.DataFrame(index=summarized_date, columns=["零钱", "零钱通"])
        for date in summarized_date:
            all_account = self.transactions[self.transactions["交易时间"] == date]
            lingqian_account = all_account[all_account["支付方式"] == "零钱"]["金额(元)"].sum()
            lingqiantong_account = all_account[all_account["支付方式"] == "零钱通"]["金额(元)"].sum()
            result.loc[date] = [round(lingqian_account, 2), round(lingqiantong_account, 2)]  # 保留两位小数
        self.summary = result


if __name__ == '__main__':
    test = WechatPay()
    test.read("../input")
    test._pre_process()
    test.date_summarize()
    pass
