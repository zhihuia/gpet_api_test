import unittest
from common.do_request import send_request
from common import do_logs
import logging
from common.do_match import match


url = "https://gpetdev.gemii.cc"
method1 = "post"
method2 = "get"
headers1 = {"Content-Type": "application/json"}

# 1.获取token
method = "post"
url1 = "https://gpetdev.gemii.cc/auth"
request_data = {"union_id": ""}
expected_data = '{"access_token":".*","code":1200,"msg":""}'
#
# 8.
# 判断用户是否注册
# - url: GET / users / {union_id / registered
#                       - 非鉴权
#                       - 入参：链接参数
#                            - 出参：
# {
#     "code": int, // 1200：正常
# "data": boolean // True：注册, False: 没注册
# "description": "描述",
# "page_info": {}
# }


class TestAPIV1(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     print("========start test========")
    #
    # @classmethod
    # def tearDown(cls):
    #     print("========end   test========")

    def test_get_token(self):
        logging.info("========开始一个接口测试========")
        logging.info("请求url为：\n{0}".format(url+"/auth"))
        logging.info("请求方法为：{0}".format(method1))
        logging.info("请求数据为：\n{0}".format({"union_id": "oVzypxFj3QKKtrHx-jlQo8absiQ4"}))
        # 调用发送接口请求数据的方法，将所有测试用例的测试数据发送出去
        res_obj = send_request(method1, url+"/auth", {"union_id": "oVzypxFj3QKKtrHx-jlQo8absiQ4"}, headers1)
        logging.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*token.*', res_obj.text)






