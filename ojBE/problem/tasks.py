import requests
import logging

logger = logging.getLogger(__name__)

def send_test_case_to_judge(url, data=None, files=None):
    try:
        res = requests.post(url, data=data, files=files)
        res = eval(res.text)
        if res['msg'] == 'Uploaded zip file is bad':
            res['code'] = -3
        elif res['msg'] == 'Uploaded zip file is empty':
            res['code'] = -4
        return res
    except Exception as e:
        logger.exception(e)
        res = {'code': -5, 'msg': 'connect judge server except', 'data': {}}
        return res