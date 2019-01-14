import unittest
from common.do_request import send_request
# from common import do_logs1
# import logging
from common.do_logs1 import logger
from common.do_match import match
import re
from common.do_db import DoPgsql
from common import dir_config


class TestAPIV1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("========start test========")
        cls.url = "https://gpetdev.gemii.cc"
        cls.headers1 = {"Content-Type": "application/json"}
        cls.temp = send_request("post", cls.url+"/auth",
                             {"union_id": "oVzypxFj3QKKtrHx-jlQo8absiQ4"}, cls.headers1)
        try:
            cls.a = re.search('.*token.*', cls.temp.text)
            assert cls.a is not None
            logger.info("====数据准备：获取token成功===")
            cls.headers2 = {"Content-Type": "application/json",
                            "Authorization": "Bearer {token}".format(token=cls.temp.json()["access_token"])}
        except Exception as e:
            logger.exception("===数据准备：获取token失败===")
            raise e
        cls.global_var = {}

    # @classmethod
    # def tearDown(cls):
    #     cls.temp = DoPgsql(dir_config.dbconfig_dir)
    #     cls.id = cls.temp.select_data('SELECT a.nickname from robot_group_map as a , group as b where \
    #                                 a.group_id = b.id and b.code =cls.global_var["group_code"];')
    #     if cls.id == "api测试1":
    #         update_sql = " UPDATE robot_group_map SET nickname = 'api复原' WHERE robot_group_map.group_id IN \
    #                       (SELECT id FROM group WHERE code = 'AA7E12E5B6218E645B7C9D56FBD18552');"
    #         cls.temp.update_data(update_sql)
    #     cls.temp.close_conn()
    #     logger.info("========end   test========")

    def log_method(self, case_name, method, suffix, params=None):
        logger.info("========casename：{case_name}========".format(case_name=case_name))
        logger.info("请求方法为：{method}".format(method=method))
        logger.info("请求url为：\n{url}".format(url=self.url+suffix))
        logger.info("请求参数为：\n{params}".format(params=params))

    # 分配机器人
    def test_01_distribution(self):
        params = {
            "open_id": "ocSwr1CozCsE1TLQMbwipQtest01",
            "union_id": "oVzypxFj3QKKtrHx-jlQo8test01",
            "sharing_user_id": "4b7802aa-2e04-4543-80a7-5a0b104a107d",
            "channel": "TEST"
        }
        self.log_method("分配机器人", "post", "/robot/distribution", params=params)
        res_obj = send_request("post", self.url+"/robot/distribution", request_data=params, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 检验当前服务状态
    def test_02_status(self):
        self.log_method("检验当前服务状态，服务正常", "get", "/app/status", params=None)
        res_obj = send_request("get", self.url+"/app/status", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 判断用户是否注册 --已注册用户
    def test_03_is_registered(self):
        self.log_method("判断用户是否注册，已注册", "get", "/users/oVzypxFj3QKKtrHx-jlQo8absiQ4/registered", params=None)
        res_obj = send_request("get", self.url+"/users/oVzypxFj3QKKtrHx-jlQo8absiQ4/registered",
                               request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*true.*', res_obj.text)

    # 判断用户是否注册 --未注册用户
    def test_04_not_registered(self):
        self.log_method("判断用户是否注册，未注册", "get", "/users/oVzypxFj3QKKtrHx-jlQo8absiQ2/registered", params=None)
        res_obj = send_request("get", self.url+"/users/oVzypxFj3QKKtrHx-jlQo8absiQ2/registered",
                               request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*false.*', res_obj.text)

    # 获取当前token的用户ID --验证成功
    def test_05_get_userid_success(self):
        self.log_method("获取当前token的用户ID，验证成功返回user_id", "get", "/auth/me", params=None)
        res_obj = send_request("get", self.url+"/auth/me", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 获取当前token的用户ID --验证失败
    def test_06_get_userid_failed(self):
        self.log_method("获取当前token的用户ID，验证失败", "get", "/auth/me", params=None)
        res_obj = send_request("get", self.url+"/auth/me", request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1401.*', res_obj.text)

    # 判断用户是否封号 --未封号
    def test_07_not_block(self):
        self.log_method("判断用户是否封号，未封号", "get", "/users/block_verify", params=None)
        res_obj = send_request("get", self.url+"/users/block_verify", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*false.*', res_obj.text)

    # 首页获取群数量和徒弟徒孙数量
    def test_08_get_groups_and_disciples_num(self):
        self.log_method("首页获取群数量和徒弟徒孙数量", "get", "/user/groups/disciples", params=None)
        res_obj = send_request("get", self.url+"/user/groups/disciples", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 首页获取群数量和徒弟徒孙数量--不鉴权
    def test_09_get_groups_and_disciples_failed(self):
        self.log_method("首页获取群数量和徒弟徒孙数量", "get", "/user/groups/disciples", params=None)
        res_obj = send_request("get", self.url+"/user/groups/disciples", request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1401.*', res_obj.text)

    # 群列表,status=1正常
    def test_10_get_group_status1(self):
        self.log_method("群列表，status=1（正常）", "get", "/groups?status=1", params=None)
        res_obj = send_request("get", self.url+"/groups?status=1", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)
        if res_obj.json()["data"][0]["code"] is not None:
            self.global_var["group_code"] = res_obj.json()["data"][0]["code"]
            print("获取第一个群Code在修改群列表机器人昵称接口使用")
            print("此时global_var的数据为：\n", self.global_var)

    # 群列表,status=0待同步
    def test_11_get_group_status0(self):
        self.log_method("群列表，status=0（待同步）", "get", "/groups?status=0", params=None)
        res_obj = send_request("get", self.url+"/groups?status=0", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 群列表,status=1正常--不鉴权
    def test_12_get_group_status1(self):
        self.log_method("群列表，status=1（正常）", "get", "/groups?status=1", params=None)
        res_obj = send_request("get", self.url+"/groups?status=1", request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1401.*', res_obj.text)

    # 群列表,status不存在
    def test_13_get_group_status3(self):
        self.log_method("群列表，status=3（不存在）", "get", "/groups?status=3", params=None)
        res_obj = send_request("get", self.url+"/groups?status=3", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 徒弟徒孙列表，leave=1徒弟列表
    def test_14_get_apprentice_leave1(self):
        self.log_method("徒弟徒孙列表，leave=1徒弟列表", "get", "/user/apprentice?current_page=&page_size=&leave=1")
        res_obj = send_request("get", self.url+"/user/apprentice?current_page=&page_size=&leave=1",
                               request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)
        temp_data1 = []
        temp_data2 = []
        temp_data3 = []
        if res_obj.json()["data"] is not None:  # 遍历data列表
            for i in range(0, len(res_obj.json()["data"])):
                if res_obj.json()["data"][i]["is_remind"] == 1:
                    if res_obj.json()["data"][i]["is_import"] is False and res_obj.json()["data"][i]["is_apprentice"] is False:
                        # 未导群未收徒
                        temp_data1.append(res_obj.json()["data"][i])
                    if res_obj.json()["data"][i]["is_import"] is False and res_obj.json()["data"][i]["is_apprentice"] is True:
                        # 未导群已收徒
                        temp_data2.append(res_obj.json()["data"][i])
                    if res_obj.json()["data"][i]["is_import"] is True and res_obj.json()["data"][i]["is_apprentice"] is False:
                        # 已导群未收徒
                        temp_data3.append(res_obj.json()["data"][i])
            if temp_data1:
                self.global_var["id_not_not"] = temp_data1[0]["user_id"]
                print("获得未导群未收徒的uesr_id")
            else:
                print("没有未导群已收徒的数据")
            if temp_data2:
                self.global_var["id_not_is"] = temp_data2[0]["user_id"]
                print("获得未导群已收徒的uesr_id")
            else:
                print("没有未导群未收徒的数据")
            if temp_data3:
                self.global_var["id_is_not"] = temp_data3[0]["user_id"]
                print("获得已导群未收徒的uesr_id")
            else:
                print("没有已导群未收徒的数据")
        print("此时global_var的数据为：\n", self.global_var)

    # 徒弟徒孙列表，leave=2徒孙列表
    def test_15_get_apprentice_leave2(self):
        self.log_method("徒弟徒孙列表，leave=2徒弟列表", "get", "/user/apprentice?current_page=&page_size=&leave=2")
        res_obj = send_request("get", self.url+"/user/apprentice?current_page=&page_size=&leave=2",
                               request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 徒弟徒孙列表，leave=2徒孙列表--不鉴权
    def test_16_get_apprentice_leave2(self):
        self.log_method("徒弟徒孙列表，leave=2徒弟列表", "get", "/user/apprentice?current_page=&page_size=&leave=2")
        res_obj = send_request("get", self.url+"/user/apprentice?current_page=&page_size=&leave=2",
                               request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1401.*', res_obj.text)

    # 徒弟徒孙列表，leave=3不存在
    def test_17_get_apprentice_leave3(self):
        self.log_method("徒弟徒孙列表，leave=3徒弟列表", "get", "/user/apprentice?current_page=&page_size=&leave=3")
        res_obj = send_request("get", self.url+"/user/apprentice?current_page=&page_size=&leave=3",
                               request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 修改群列表机器人昵称
    def test_18_update_robot_name(self):
        params = {"remark_name": "api测试1"}
        if self.global_var is not None:
            for item, value in self.global_var.items():
                if "group_code" == item:
                    self.log_method("修改群列表机器人昵称", "put",
                                    "/groups/{group_code}/robot_name".format(group_code=self.global_var['group_code']),
                                    params=params)
                    res_obj = send_request("put",
                                           self.url+"/groups/{group_code}/robot_name".format(group_code=self.global_var['group_code']),
                                           request_data=params, headers=self.headers2)
                    logger.info("响应的结果为：\n{0}".format(res_obj.text))
                    match('.*1200.*', res_obj.text)
                    break
            else:
                print("group_code不存在，该条case不执行")
        else:
            print("入参不存在，该条case不执行")

    # 群收益
    def test_19_profit(self):
        self.log_method("群收益", "get", "/profit")
        res_obj = send_request("get", self.url+"/profit", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 提现
    def test_20_withdraw(self):
        self.log_method("提现", "get", "/withdraw")
        res_obj = send_request("get", self.url+"/withdraw", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 徒弟唤醒，未导群未收徒
    def test_21_awakening_not_not(self):
        if self.global_var is not None:
            for item, value in self.global_var.items():
                if "id_not_not" == item:
                    params = {
                                "is_import": False,
                                "is_apprentice": False,
                                "user_id": "{id}".format(id=self.global_var["id_not_not"])
                                }
                    self.log_method("徒弟唤醒，未导群未收徒", "post", "/apprentice/awakening", params=params)
                    res_obj1 = send_request("post", self.url+"/apprentice/awakening", request_data=params, headers=self.headers2)
                    logger.info("响应的结果为：\n{0}".format(res_obj1.text))
                    match('.*1200.*', res_obj1.text)
                    logger.info("再次请求徒弟列表，校验该徒弟是否还能再次做唤醒操作")
                    res_obj2 = send_request("get", self.url + "/user/apprentice?current_page=&page_size=&leave=1",
                                            request_data=None, headers=self.headers2)
                    logger.info("再次请求徒弟列表的响应结果为：\n{0}".format(res_obj2.text))
                    match('.*1200.*', res_obj2.text)
                    if res_obj2.json()["data"] is not None:
                        for i in range(0, len(res_obj2.json()["data"])):
                            if self.global_var["id_not_not"] == res_obj2.json()["data"][i]["user_id"]:
                                match("0", str(res_obj2.json()["data"][i]["is_remind"]))
                    break
            else:
                print("未导群未收徒数据不存在，该条case不执行")
        else:
            print("入参不存在，该条case不执行")

    # 徒弟唤醒，未导群已收徒
    def test_22_awakening_not_is(self):
        if self.global_var is not None:
            for item, value in self.global_var.items():
                if "id_not_is" == item:
                    params = {
                        "is_import": False,
                        "is_apprentice": True,
                        "user_id": "{id}".format(id=self.global_var["id_not_is"])
                    }
                    self.log_method("徒弟唤醒，未导群已收徒", "post", "/apprentice/awakening", params=params)
                    res_obj1 = send_request("post", self.url+"/apprentice/awakening", request_data=params, headers=self.headers2)
                    logger.info("响应的结果为：\n{0}".format(res_obj1.text))
                    match('.*1200.*', res_obj1.text)
                    logger.info("再次请求徒弟列表，校验该徒弟是否还能再次做唤醒操作")
                    res_obj2 = send_request("get", self.url + "/user/apprentice?current_page=&page_size=&leave=1",
                                            request_data=None, headers=self.headers2)
                    logger.info("再次请求徒弟列表的响应结果为：\n{0}".format(res_obj2.text))
                    match('.*1200.*', res_obj2.text)
                    if res_obj2.json()["data"] is not None:
                        for i in range(0, len(res_obj2.json()["data"])):
                            if self.global_var["id_not_is"] == res_obj2.json()["data"][i]["user_id"]:
                                match("0", str(res_obj2.json()["data"][i]["is_remind"]))
                    break
            else:
                print("未导群已收徒数据不存在，该条case不执行")
        else:
            print("入参不存在，该条case不执行")

    # 徒弟唤醒，已导群未收徒
    def test_23_awakening_is_not(self):
        if self.global_var is not None:
            for item, value in self.global_var.items():
                if "id_is_not" == item:
                    params = {
                        "is_import": True,
                        "is_apprentice": False,
                        "user_id": "{id}".format(id=self.global_var["id_is_not"])
                    }
                    self.log_method("徒弟唤醒，已导群未收徒", "post", "/apprentice/awakening", params=params)
                    res_obj1 = send_request("post", self.url+"/apprentice/awakening", request_data=params, headers=self.headers2)
                    logger.info("响应的结果为：\n{0}".format(res_obj1.text))
                    match('.*1200.*', res_obj1.text)
                    logger.info("再次请求徒弟列表，校验该徒弟是否还能再次做唤醒操作")
                    res_obj2 = send_request("get", self.url + "/user/apprentice?current_page=&page_size=&leave=1",
                                            request_data=None, headers=self.headers2)
                    logger.info("再次请求徒弟列表的响应结果为：\n{0}".format(res_obj2.text))
                    match('.*1200.*', res_obj2.text)
                    if res_obj2.json()["data"] is not None:
                        for i in range(0, len(res_obj2.json()["data"])):
                            if self.global_var["id_is_not"] == res_obj2.json()["data"][i]["user_id"]:
                                match("0", str(res_obj2.json()["data"][i]["is_remind"]))
                    break
            else:
                print("已导群未收徒数据不存在，该条case不执行")
        else:
            print("入参不存在，该条case不执行")

    # 获取当前最大额度机器人
    def test_24_robot_show(self):
        self.log_method("获取当前最大额度机器人", "get", "/robot/show", params=None)
        res_obj = send_request("get", self.url+"/robot/show", request_data=None, headers=self.headers2)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1200.*', res_obj.text)

    # 获取当前最大额度机器人--不鉴权
    def test_25_robot_show(self):
        self.log_method("获取当前最大额度机器人", "get", "/robot/show", params=None)
        res_obj = send_request("get", self.url+"/robot/show", request_data=None, headers=self.headers1)
        logger.info("响应的结果为：\n{0}".format(res_obj.text))
        match('.*1401.*', res_obj.text)









