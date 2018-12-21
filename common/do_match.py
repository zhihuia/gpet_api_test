from common import do_logs
import logging
import re


def match(expected_data=None, actual_data=None):
    try:
        a = re.search(expected_data, actual_data)
        # print(a)
        if a is not None:
            logging.info("期望结果与实际结果匹配，用例成功！")
        else:
            logging.info("期望结果与实际结果不匹配，用例失败！")
    except Exception as e:
        logging.error("具体错误信息：")
        logging.exception("断言异常：")
        raise e


# re.search('.*token.*',
#           '{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNGI3ODAyYWEtMmUwNC00NTQzLTgwYTctNWEwYjEwNGExMDdkIiwiZXhwIjoxNTQ1MzgyMTQwfQ.OBTmKFGN2vA_cIolNY6-5BKzaAIFQWrEcfotlXfs9n4","code":1200,"msg":""}')

# match('.*token.*','{"access_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNGI3ODAyYWEtMmUwNC00NTQzLTgwYTctNWEwYjEwNGExMDdkIiwiZXhwIjoxNTQ1MzgyMTQwfQ.OBTmKFGN2vA_cIolNY6-5BKzaAIFQWrEcfotlXfs9n4","code":1200,"msg":""}')
# print(re.search("a.*", "abc"))
