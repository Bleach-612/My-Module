#!encoding:utf-8
import json
import copy
import time
import requests
from iso3166 import countries


class SimilarWeb(object):
    rank = {
        "global_rank": 0,
        "country_name": None,
        "country_rank": 0,
        "category_rank": 0,
        "category_main": None,
        "category_sub": None,
        "total_visits": 0,
        "title": None,
        "desc": None,
        "LargeScreenshot": None,
        "TopCountryShares": None,
        "Social": None,
        "TrafficSources": None,
        "EstimatedMonthlyVisits": None
    }

    def get_info(self, domain, proxy=None, headers=None):
        """
        获取接口数据 global_rank(默认为0代表404无数据返回，-1则是403超时或者其他原因无数据返回)
        :param domain: 域名
        :param proxy: 代理
        """
        infos = {"Similar_info": {}, "status": 0}
        url = f"http://data.similarweb.com/api/v1/data?domain={domain}"
        res = self.get_html_souce(url, proxy=proxy, headers=headers)
        infos["Similar_info"]["rank"] = copy.deepcopy(self.rank)
        if res["status"] > 0:
            if res["data"]:
                infos["Similar_info"]["rank"] = self.parse_json(res["data"])
                infos["status"] = 1
        else:
            if res['http_code'] != 404:
                infos["Similar_info"]["rank"]["global_rank"] = -1
            infos["status"] = -1
        return infos

    def parse_json(self, content):
        """
        解析json数据
        :param content:
        :return
        """
        rank = copy.deepcopy(self.rank)
        result = json.loads(content)

        if "Description" in result.keys():
            rank["desc"] = json.dumps(result["Description"])
        rank["LargeScreenshot"] = json.dumps(result["LargeScreenshot"])
        rank["TrafficSources"] = json.dumps(result["TrafficSources"])
        rank["Social"] = result["TrafficSources"]["Social"]
        rank["EstimatedMonthlyVisits"] = json.dumps(result["EstimatedMonthlyVisits"])
        rank["TopCountryShares"] = json.dumps(result["TopCountryShares"])
        rank["Social"] = result["TrafficSources"]["Social"]
        rank["title"] = json.dumps(result["Title"])
        rank["global_rank"] = result["GlobalRank"]["Rank"]
        # 利用iso3166库找出对应编码国家名
        rank["country_name"] = countries.get(result["CountryRank"]["Country"]).name
        rank["country_rank"] = result["CountryRank"]["Rank"]
        try:
            category_name = result["Category"]
        except:
            category_name = ''

        cate_li = category_name.split("/")
        rank["category_main"] = category_name
        if len(cate_li) > 1:
            rank["category_main"] = cate_li[0]
            rank["category_sub"] = cate_li[1]
        rank["category_rank"] = int(result["CategoryRank"]["Rank"])
        visits_dic = result["EstimatedMonthlyVisits"]
        rank["total_visits"] = sorted(visits_dic.items(), key=lambda x: x[0], reverse=True)[0][1]
        return rank

    @staticmethod
    def get_html_souce(url, run_max_count=3, n_timeout=30, proxy=None, headers=None,
                       success_code_range: tuple = (200, 200), **kwargs):
        """
        爬取url源码信息, 返回爬取源码，是否成功标志，真实url链接
        返回字典，优化返回码，可扩展
        :param url:
        :param run_max_count: 最大重试次数
        :param n_timeout: 超时退出时间，默认30s
        :param proxy: 代理
        :param headers: 请求头
        :param success_code_range: 请求成功状态码区间(双向闭合)，默认200为成功
        :param kwargs: requests.get()方法其他参数
        :return:
        """
        ret = {
            "status": 0,
            "data": None,
            "http_code": None,
        }
        count = 0
        while True:
            try:
                if proxy is not None:
                    r = requests.get(url, proxies=proxy, headers=headers, timeout=n_timeout, **kwargs)
                else:
                    r = requests.get(url, headers=headers, timeout=n_timeout, **kwargs)

                if success_code_range[0] <= r.status_code <= success_code_range[1]:
                    html = str(r.content, 'utf-8', errors='ignore')
                    ret["status"] = 1
                    ret["http_code"] = r.status_code
                    ret["data"] = html
                    return ret
                else:
                    count += 1
                    time.sleep(1)
                    if count > run_max_count:
                        ret["status"] = 0
                        ret["http_code"] = r.status_code
                        ret["data"] = ""
                        return ret
                    continue
                break
            except Exception as e:
                print("error:[%s]" % (str(e)))
                count += 1
                time.sleep(1)
                if count > run_max_count:
                    ret["status"] = 0
                    ret["http_code"] = r.status_code
                    ret["data"] = ""
                    return ret


def similar_test():
    similar = SimilarWeb()
    domain_li = ["baidu.com", "qq.com", "163.com"]
    # 传递headers和proxy，否则无数据返回
    for domain in domain_li:
        result = similar.get_info(domain)
        print(result)


if __name__ == '__main__':
    similar_test()
