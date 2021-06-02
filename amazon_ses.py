import os
import json
import boto3
from botocore.exceptions import ClientError
from botocore.config import Config


class AmazonEmail:
    def __init__(self, access_key, secret_key, region, service="ses", charset="utf-8", retries_times=3, proxy=None):
        my_config = Config(
            region_name=region,
            signature_version='v4',
            retries={
                'max_attempts': retries_times,
                'mode': 'standard'
            },
            proxies=proxy,
        )
        self.client = boto3.client(
            service_name=service,
            config=my_config,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.charset = charset

    def get_email_template(self, template_name):
        """
        查看邮件模板
        :param template_name: 模板名称
        """
        return self.client.get_template(TemplateName=template_name)

    def delete_email_template(self, template_name):
        """
        删除邮件模板
        :param template_name: 模板名称
        """
        return self.client.delete_email_template(TemplateName=template_name)

    def create_email_template(self, template_name, subject_part, html_part, text_part=""):
        """
        创建邮件模板
        :param template_name: 模板名称
        :param subject_part: 主题
        :param html_part: 支持html格式
        :param text_part: 不显示html格式的客户端，默认空
        """
        response = self.client.create_template(
            Template={
                'TemplateName': template_name,
                'SubjectPart': subject_part,
                'TextPart': text_part,
                'HtmlPart': html_part
            }
        )
        return response

    def verify_email(self, email):
        """验证邮箱"""
        response = self.client.verify_email_identity(EmailAddress=email)
        return response

    def send_email_normal(self, sender_email: str, recipient_email: str, subject: str, body_html: str,
                          body_text: str = ""):
        """
        发送普通邮件
        :param sender_email: 发件人邮箱地址
        :param recipient_email: 收件人邮箱地址
        :param subject: 邮件主题
        :param body_html: 支持html样式
        :param body_text: 不支持html显示的客户端可使用, 默认为空
        :return:
        """
        message = {
            'Body': {
                'Text': {
                    'Charset': self.charset,
                    'Data': body_text,
                },
                'Html': {
                    'Charset': self.charset,
                    'Data': body_html,
                }
            },
            'Subject': {
                'Charset': self.charset,
                'Data': subject,
            }
        }

        return self.email_send_process(recipient_email=recipient_email, message=message, sender_email=sender_email)

    def send_email_dynamic(self, sender_email: str, recipient_email: str, subject: str, template_info: dict):
        """
        发送动态模板邮件
        :param sender_email: 发件人邮箱地址
        :param recipient_email: 收件人邮箱地址
        :param template_info: 模板信息
        :param subject: 邮件主题
        :return:
        """
        return self.email_send_process(recipient_email=recipient_email, sender_email=sender_email, is_template=True,
                                      template_info=template_info)

    def email_send_process(self, recipient_email: str, sender_email: str, tries_times: int = 3, message: dict = {},
                           is_template: bool = False, template_info: dict = None):
        """
        邮件发送操作
        :param recipient_email: 收件人地址
        :param sender_email: 寄件人地址
        :param tries_times: 重试次数
        :param message: 消息主体
        :param is_template: 是否发送模板邮件，默认关闭
        :param template_info: 模板信息字典
        :return:
        """
        ret = False
        destination = {'ToAddresses': [recipient_email]}
        cnt = 0
        while True:
            try:
                if is_template is False:
                    response = self.client.send_email(Destination=destination, Message=message, Source=sender_email)
                else:
                    template_name = template_info["template_name"]
                    template_data = json.dumps(template_info["template_data"])
                    template_arn = template_info["template_arn"]
                    response = self.client.send_templated_email(
                        Destination=destination,
                        Source=sender_email,
                        Template=template_name,
                        TemplateData=template_data,
                        TemplateArn=template_arn
                    )
                if response['MessageId']:
                    print(f"MessageId: {response['MessageId']}")
                    ret = True
                    break
                else:
                    cnt += 1
                    if cnt >= tries_times:
                        return ret
                    continue
            except ClientError as e:
                if cnt >= tries_times:
                    break
                print(e.response['Error']['Message'])
                cnt += 1
        return ret


def test_case():
    """
    测试用例
    """
    sender_email = "test1@qq.com"
    recipient_email = "test2@qq.com"
    # 当前模板名称写死 amazon-email
    template_name = "amazon-email"
    subject_part = "模板"

    access_key = "AKIU3SUUDCZJ"
    secret_key = "NfBjshU+Yliok8RvcHeh/EsQasfdp"
    region = "us-east-2"

    # 这是模板里需要替换的参数，如下html
    """<span>Dear {{info.name}}</span>
    Your phone number is {{phone_num}}
    href="https://xxxxx.com/?sex={{info.sex}}" 
    """
    template_info = {
        "template_name": template_name,
        "template_data": {
            "info": {"name": "张三", "sex": "男"},
            "phone_num": "132412345235",
            "sender_email": sender_email
        },
        "template_arn": ""
    }

    aws_ses = AmazonEmail(access_key, secret_key, region)

    # 创建test邮件模板
    # template_name = "amazon-email"
    # with open("./test.html", "r") as f:
    #     html_part = f.read()
    # resp = aws_ses.create_email_template(template_name, subject_part, html_part)
    # print("创建模板：\n %s" % resp)
    # 查看test邮件模板
    # resp = aws_ses.get_email_template(template_name)
    # print("邮件模板信息：\n %s", resp)
    body_html = """
    <html>
        <head></head>
        <body>
          <h1>Amazon SES Test (SDK for Python)</h1>
          <p>This email was sent with
            <a href='https://aws.amazon.com/ses/'>Amazon SES</a> 
            using theAWS SDK for Python (Boto)
            </a>.
        </p>
        </body>
    </html>"""
    # 发送普通邮件
    ret = aws_ses.send_email_normal(sender_email=sender_email, recipient_email=recipient_email, subject="测试邮件",
                                    body_html=body_html)
    print(ret)
    # 发送模板邮件
    ret = aws_ses.send_email_dynamic(sender_email=sender_email, recipient_email=recipient_email, subject=subject_part,
                               template_info=template_info)
    print(ret)


if __name__ == "__main__":
    test_case()



