from common import do_logs1
import logging
import re


def match(expected_data=None, actual_data=None):
    try:
        a = re.search(expected_data, actual_data)
        assert a is not None
        logging.info("期望结果与实际结果匹配，用例成功！")
    except Exception as e:
        logging.error("期望结果与实际结果不匹配，用例失败！")
        logging.exception("断言异常：")
        raise e


