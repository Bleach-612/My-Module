# -*- coding: utf-8 -*-
import json
from redis import ConnectionPool, Redis

HEAD = "head"
TAIL = "tail"


class RedisClient:
    def __init__(self, host, password=None, port=6379):
        """
        :param host: 主机ip
        :param port: 端口
        :param password: 密码
        """
        self.redis_type = None
        self.host = host
        self.port = port
        self.password = password
        self.conn = self.__connect()

    def __connect(self):
        num = 1
        while True:
            try:
                pool = ConnectionPool(host=self.host, port=self.port, password=self.password,
                                      decode_responses=True, health_check_interval=30)
                redis = Redis(connection_pool=pool)
                redis.ping()
            except (ConnectionError, TimeoutError) as e:
                if num >= 3:
                    break
                print('redis连接失败,正在尝试重连--%s' % num)
                continue
            else:
                return redis

    # 设置操作类型
    def set_redis_type(self, redis_type):
        if redis_type == TAIL:
            self.redis_type = "r"
        if redis_type == HEAD:
            self.redis_type = "l"

    def insert(self, name, value, _head=True):
        """
        插入单个数据
        :param :name 键名
        :param :value 值
        :param :_head 默认从头插入，反之尾部插入
        """
        if _head:
            self.set_redis_type(HEAD)
        else:
            self.set_redis_type(TAIL)
        value_str = json.dumps(value, ensure_ascii=False)
        try:
            exec(f'self.conn.{self.redis_type}push(name, value_str)')
        except Exception as e:
            print(e)
            return False
        return True

    def read(self, name, start=0, end=-1):
        """
        读取redis
        :param :name 键名
        :param :start 起始位置
        :param :end 结束位置
        """
        result = self.conn.lrange(name, start, end)
        return [json.loads(i) for i in result]

    def update(self, name, value, index=-1):
        """
        更新数据
        :param name: 键名
        :param value: 转换的变量值
        :param index: 下标，默认修改最后一个
        """
        value_str = json.dumps(value, ensure_ascii=False)
        try:
            result = self.conn.lset(name, index, value_str)
        except Exception as e:
            print(str(e))
            return False
        return result

    def llen(self, name):
        """
        获取key长度
        :param :name key name
        """
        return self.conn.llen(name)

    def get_names(self):
        """
        获取key name列表
        """
        return self.conn.keys()

    def delete(self, *names):
        """
        删除 一个或多个key
        :param :names 一个key或list keys
        """
        # if self.conn.flushdb():
        if self.conn.delete(*names):
            print('successfully deleted')
        else:
            print('failed to delete')

    def __IfJsonData(self, datas):
        for _ in datas:
            try:
                yield json.loads(_)
            except:
                yield _

    def batch_pick(self, name, num, _head=False):
        """
        批量取出
        :param :name 名称
        :param :num 取出数量
        :param :_head 从头部取出，默认True，反之从尾部取
        """
        _size = self.llen(name)
        with self.conn.pipeline(transaction=False) as p:
            if num < _size:
                if _head:
                    p.lrange(name, 0, num - 1)
                    p.ltrim(name, num, -1)
                else:
                    p.lrange(name, _size-num, _size)
                    p.ltrim(name, 0, _size - num - 1)
                datas, flag = p.execute()
                data = list(self.__IfJsonData(datas))

            else:
                p.lrange(name, 0, _size)
                try:
                    datas = p.execute()[0]
                    if isinstance(datas, list):
                        data = list(self.__IfJsonData(datas))
                    self.delete(name)
                except Exception as e:
                    print(e)

            return data

    def batch_pop(self, name, num=100, pop_head=True):
        """
        批量取出 默认从头取数据
        :param name: 键名
        :param num: 取出数量
        """
        if pop_head:
            self.set_redis_type(HEAD)
        else:
            self.set_redis_type(TAIL)

        with self.conn.pipeline(transaction=False) as p:
            while self.llen(name) > 0:
                if num < self.llen(name):
                    number = num
                else:
                    number = self.llen(name)

                for i in range(number):
                    exec(f'p.{self.redis_type}pop(name)')
                break
            data = list(self.__IfJsonData(p.execute()))
            return data

    def batch_push(self, name, values: list, push_head=False):
        """
        批量插入 默认从尾部插入
        :param name: 键名
        :param values: 插入list变量值
        """
        if push_head:
            self.set_redis_type(HEAD)
        else:
            self.set_redis_type(TAIL)

        with self.conn.pipeline(transaction=False) as p:
            if isinstance(values, list):
                for value in values:
                    if isinstance(value, dict):
                        value_str = json.dumps(value, ensure_ascii=False)
                    else:
                        value_str = value
                    exec(f'p.{self.redis_type}push(name, value_str)')
                p.execute()


def test():
    key_name = "test"
    redis_host = "127.0.0.1"
    redis_port = 6379
    client = RedisClient(host=redis_host, port=redis_port)
    key_name_li = client.get_names()
    print(f"key name list is {key_name_li}")
    # 插入单个数据
    client.insert(key_name, {"d": 4})
    values = []
    for i in range(10):
        value = {"a": i, "b": 2*i}
        values.append(value)
    # 批量插入 默认从尾插入
    client.batch_push(key_name, values)
    # 获取长度
    num = client.llen(key_name)
    print(f"{key_name} size is {num}")
    # 读取
    data = client.read(key_name, 1, 2)
    print(f"读取数据：{data}")
    # 默认修改最后一个
    print(f"修改成功: {client.update(key_name, {'cc': 1})}")
    # 批量取出 默认从头取
    data = client.batch_pop(key_name, 2)
    print(f"批量取出(默认从头取):{data}")
    # 批量取出 默认尾巴取
    data = client.batch_pick(key_name, 8, _head=False)
    print(f"批量取出(默认尾巴取): {data}")
    # 清空
    # client.delete(key_name)


if __name__ == '__main__':
    test()


