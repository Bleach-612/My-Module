#!encoding:utf-8
import time
import datetime


# 返回距离今天几天的日期
# def get_few_days(days=0):
#     from datetime import date, timedelta, dateti
#     """ 正数表示延后日期，负数表示之前日期，默认则为今天 """
#     if isinstance(days, int):
#         return date.today() + timedelta(days=days)
#     return None


class TimeTools:
    @staticmethod
    def get_now():
        """获取当前时间格式yyyy-mm-dd hh:mm:ss"""
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    @classmethod
    def get_special_time(cls, h_m_s):
        """获取当前年月日+指定时分秒"""
        return cls.get_day() + " " + h_m_s

    @staticmethod
    def get_now_special_bef_aft(days=0, hours=0, now='', h_m_s='00:00:00'):
        """
        获取指定时间点前后时间间隔的时间, 可指定返回时刻值h_m_s
        :param days: 正数代表：几天前，负数反之
        :param hours:正数代表：几小时前，负数反之
        :param now: 指定时间，默认今日，格式：yy-mm-dd
        :param h_m_s:指定时刻，默认'00:00:00'
        :return:
        """
        if now == '':
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.strptime(now, '%Y-%m-%d')
        otherStyleTime = now - datetime.timedelta(days=days, hours=hours)
        otherStyleTime = otherStyleTime.strftime("%Y-%m-%d ")
        otherStyleTime += h_m_s
        return otherStyleTime

    @staticmethod
    def get_now_bef_aft(days=0, hours=0, now='', minutes=0, seconds=0):
        """
        获取当前时间点前后时间间隔的时间
        :param days:正数代表：几天前，负数反之
        :param hours:正数代表：几小时前，负数反之
        :param now:指定时间，默认当前时间，格式：yy-mm-dd hh:mm:ss
        :param minutes:正数代表：几分钟前，负数反之
        :param seconds:正数代表：几秒总前，负数反之
        :return:
        """
        if now == '':
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
        otherStyleTime = now - datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        otherStyleTime = otherStyleTime.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

    @classmethod
    def get_day(cls):
        """获取当前日期"""
        return cls.get_now()[:10]

    @staticmethod
    def get_D_value(time1: datetime.datetime, time2: datetime.datetime):
        """获取两个时间的差值"""
        return (time1 - time2).days

    @staticmethod
    def get_timestamp():
        """获取时间戳"""
        return int(time.time())

    @staticmethod
    def timestamp2time(timestamp):
        """
        时间戳转时间，格式：yy-mm-dd hh:mm:ss
        :param timestamp:
        :return:
        """
        # 转换成localtime
        time_local = time.localtime(timestamp)
        # 转换成新的时间格式(2016-05-05 20:28:54)
        return time.strftime("%Y-%m-%d %H:%M:%S", time_local)


def test_case():

    # 获取当前时间-->2021-05-10 11:56:45
    print(TimeTools.get_now())
    # 获取今日 01:02:03 --> 2021-05-10 01:02:03
    print(TimeTools.get_special_time("01:02:03"))
    # 获取明天的14:00:00
    print(TimeTools.get_now_special_bef_aft(days=-1, h_m_s="14:00:00"))
    # 获取2021-05-10 13:37:00一小时后
    print(TimeTools.get_now_bef_aft(hours=-1, now="2021-05-10 13:37:00"))
    # 获取今日日期-->2021-05-10
    print(TimeTools.get_day())
    # 比较两个datetime.datetime类型时间间隔【datetime.datetime(年, 月, 日)】
    print(TimeTools.get_D_value(datetime.datetime(2021, 3, 1), datetime.datetime(2021, 3, 2)))
    # 时间戳转时间，格式yy-mm-dd hh:mm:ss
    print(TimeTools.timestamp2time(1620625704.778211))


if __name__ == '__main__':
    test_case()



