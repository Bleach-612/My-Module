# !/usr/bin/python
# -*- coding:utf-8 -*-
import json
from yys_request import YysRequest

ST_SUCCESS = 1
ST_UNKNOWN_ERROR = 0


class FeiShuAuthorization:
    """
    创建应用链接：https://open.feishu.cn/app/
    获取  app_id, app_secret
    需要开启机器人选项
    """

    def __init__(self, app_id, app_secret, **kwargs):
        self.app_id = app_id
        self.app_secret = app_secret
        self.__url = "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
        self.requests = YysRequest()

    def get_token(self):
        token = None
        headers = {"Content-Type": "application/json; charset=utf-8"}
        data = {"app_id": self.app_id, "app_secret": self.app_secret}
        resp = self.requests.request_get(
            self.__url,
            headers=headers,
            data=json.dumps(data),
            is_json=True
        )
        return resp


class FeiShuRobot:
    __content = {
        "msg": "content-info",  # 必选，信息
        "italic": False,  # 可选，是否斜体，默认否
        "bold": False,  # 可选，是否加粗，默认否
        "pre": ""  # 可选，默认为空
    }

    def __init__(self, fs_robot_key, **kwargs):
        """
        :param wx_robot_key: 飞书机器人身份码
        :param debug_flag: 是否开启调试日志，默认关闭
        """
        self._robot_key = fs_robot_key
        self._fs_api = "https://open.feishu.cn/open-apis/bot/v2/hook/"
        self._app_id = kwargs.get("app_id", None)
        self._app_secret = kwargs.get("app_secret", None)
        self.__requests = YysRequest()

    def get_token(self, **kwargs):
        obj = FeiShuAuthorization(self._app_id, self._app_secret, **kwargs)
        return obj.get_token()

    def _post_msg(self, text_msg, file_path=None):
        """
        发送报文请求
        :param text_msg:
        :param file_path: 文件地址（选填）
        :return:
        """
        _result = None
        try:
            url = self._fs_api + self._robot_key
            resp = self.__requests.request_post(url, data=text_msg)
            if resp:
                _result = resp
        except Exception as e:
            print(e)
        return _result

    def _upload_img(self, img_path):
        """
        上传图片（发送图片需要）
        :param img_path:图片路径
        :return:
        """
        with open(img_path, 'rb') as f:
            image = f.read()
        token = self.get_token()
        if token:
            resp = self.__requests.request_post(
                req_url='https://open.feishu.cn/open-apis/image/v4/put/',
                headers={'Authorization': "Bearer " + token["app_access_token"]},
                files={"image": image},
                data={"image_type": "message"},
                stream=True,
                is_json=True,
            )
            return resp
        return False

    def _upload_file(self, file_path):
        """
        上传文件（发送文件需要）
        :param file_path:
        :return:
        """
        pass

    def send_text(self, content: str = ""):
        """
        发送普通文本
        :param content: 文本内容
        :return: 发送成功返回WF_ST_SUCCESS，反之失败
        """
        _body = {
            "msg_type": "text",
            "content": {
                "text": content
            }
        }
        _body = json.dumps(_body).encode("utf-8")

        # 发送请求
        resp = self._post_msg(_body)

        if resp == ST_SUCCESS:
            print("success send wx msg")
            return ST_SUCCESS
        else:
            print(f"fail send wx msg, error_message:{resp['error_message']}")
        return ST_UNKNOWN_ERROR

    def send_markdown(self, content_msg: str = "", content_lst: list = ""):
        """
        发送markdown文本(消息文本)
        :return:
        """

        if not any([content_msg, content_lst]):
            raise ValueError("content_msg|content_lst must input one")

        _body = {
            "msg_type": "interactive",
            "card": {
                "config": {
                    "wide_screen_mode": True,
                    "enable_forward": True
                },
                "elements": [{
                    "tag": "div",
                    "text": {
                        "content": "",
                        "tag": "lark_md"
                    }
                }]
            }
        }

        if content_msg == "":
            content = ""
            if not isinstance(content_lst, list):
                raise ValueError(f"content_lst format: {[self.__content]}")
            for rec in content_lst:
                item_msg = str(rec["msg"])

                # 前缀消息
                pre = rec.get("pre", "")
                if pre:
                    item_pre = pre + ":"
                else:
                    item_pre = ""

                # 是否加粗
                item_bold = rec.get('bold', False)
                if item_bold:
                    item_msg = "**" + item_msg + "**"

                # 是否加粗
                item_bold = rec.get('italic', False)
                if item_bold:
                    item_msg = "*" + item_msg + "*"
                content += (item_pre + item_msg + "\n")

            _body["card"]["elements"][0]["text"]["content"] = content

        else:
            _body["card"]["elements"][0]["text"]["content"] = content_msg

        _body = json.dumps(_body).encode("utf-8")

        # 发送请求
        return self._post_msg(_body)

    def send_image(self, image_path):
        """
        发送图片
        :param image_path:图片路径
        :return:
        """
        image_key = self._upload_img(image_path)
        if image_key:
            data = {
                "msg_type": "image",
                "content": {
                    "image_key": image_key["data"]["image_key"]
                }
            }
            url = self._fs_api + self._robot_key
            resp = self.__requests.request_post(url, data=json.dumps(data), is_json=True)
            return resp
        return False

    def send_file(self, file_path):
        """
        发送文件
        :param file_path:文件路径
        :return:
        """
        pass


def test(test_key):
    """
    测试用例
    :return:
    """
    tor = FeiShuRobot(test_key)
    # 测试用例1：发普通文本
    res = tor.send_text("test_File")
    print(res)
    # 测试用例2：发送完整markdown文本
    complete_msg = '<font color="info">任务结果:</font>\n' \
                   '**任务名称**:   **<font color="warning">阴阳师监控</font>**\n' \
                   '**任务创建者**:    kasper\n' \
                   '**任务执行时间**:    2021-12-24 11:00<:31\n' \
                   '**任务执行结果**:  \n**<font color="comment">。。。。</font>**'

    res = tor.send_markdown(content_msg=complete_msg)
    print(res)
    # 测试用例3：发送完整markdown文本（列表形式）
    content_msg = [
        {'msg': '异常信息', "bold": True},
        {'msg': '2021-05-09 13:00:00', "pre": "异常时间", "italic": True}  # 是否斜体
    ]
    res = tor.send_markdown(content_lst=content_msg)
    print(res)

    # 测试用例4（含未支持的type和head）
    emsg = "由于获取失败，date：2021-11-11，计算失败"
    exc_info = [
        {'type': 'warning', 'msg': '计算异常', "bold": True, "head": 4},
        {'msg': emsg, "pre": "详情信息", },
        {'msg': '2021-11-11', "pre": "异常时间"}
    ]
    res = tor.send_markdown(content_lst=exc_info)
    print(res)


if __name__ == "__main__":
    robot_key = "75bc0a22-3b19-412a-bed42b5"
    # test_case(robot_key)
    tor = FeiShuRobot(robot_key)
    # 测试用例0: 发送图片
    # 飞书应用凭证,需启用机器人
    app_id = "cli_a15c1a1500d"
    app_secret = "9RwjDDSre3Ml8e0S2qfQphYdyJ"
    tor = FeiShuRobot(robot_key, app_id=app_id, app_secret=app_secret)
    img_path = "xxxxx.png"
    print(tor.send_image(img_path))
    # 结果：{'Extra': None, 'StatusCode': 0, 'StatusMessage': 'success'}

    # import time
    # test_content_lst = [
    #     {'msg': '斗技记录-Success'},
    #     {'msg': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "pre": "开始时间"},
    #     {'msg': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "pre": "完成时间"}
    # ]
    # res = tor.send_markdown(content_lst=test_content_lst)
    # print(res)
