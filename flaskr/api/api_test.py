import logging
import random
import uuid
import os
from flask import Blueprint, jsonify, session, request
from datetime import datetime, timedelta
from decimal import Decimal

from flaskr.utils.code import ResponseCode
from flaskr.utils.response import ResMsg
from flaskr.utils.tool import route, Redis, CaptchaTool
# from flaskr.utils.auth import Auth, login_required
from flaskr.celery import add, flask_app_context

bp = Blueprint("test", __name__, url_prefix='/')

logger = logging.getLogger(__name__)


# -----------------原生蓝图路由---------------#


@bp.route('/logs', methods=["GET"])
def test_logger():
    """
    测试自定义logger
    :return:
    """
    logger.info("this is info")
    logger.debug("this is debug")
    logger.warning("this is warning")
    logger.error("this is error")
    logger.critical("this is critical")
    return "ok"


@bp.route("/unifiedResponse", methods=["GET"])
def test_unified_response():
    """
    测试统一返回消息
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    res.update(code=ResponseCode.Success, data=test_dict)
    return jsonify(res.data)


# --------------使用自定义封装蓝图路由--------------------#


@route(bp, '/packedResponse', methods=["GET"])
def test_packed_response():
    """
    测试响应封装
    :return:
    """
    res = ResMsg()
    test_dict = dict(name="zhang", age=18)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    # 此处不再需要用jsonify，如果需要定制返回头或者http响应如下所示
    # return res.data,200,{"token":"111"}
    return res.data


@route(bp, '/typeResponse', methods=["GET"])
def test_type_response():
    """
    测试返回不同的类型
    :return:
    """
    res = ResMsg()
    now = datetime.now()
    date = datetime.now().date()
    num = Decimal(11.11)
    test_dict = dict(now=now, date=date, num=num)
    # 此处只需要填入响应状态码,即可获取到对应的响应消息
    res.update(code=ResponseCode.Success, data=test_dict)
    # 此处不再需要用jsonify，如果需要定制返回头或者http响应如下所示
    # return res.data,200,{"token":"111"}
    return res.data


# --------------Redis测试封装--------------------#

@route(bp, '/testRedisWrite', methods=['GET'])
def test_redis_write():
    """
    测试redis写入
    """
    # 写入
    Redis.write("test_key", "test_value", 60)
    return "ok"


@route(bp, '/testRedisRead', methods=['GET'])
def test_redis_read():
    """
    测试redis获取
    """
    data = Redis.read("test_key")
    return data


# -----------------图形验证码测试---------------------------#

@route(bp, '/testGetCaptcha', methods=["GET"])
def test_get_captcha():
    """
    获取图形验证码
    :return:
    """
    res = ResMsg()
    new_captcha = CaptchaTool()
    img, code = new_captcha.get_verify_code()
    res.update(data=img)
    session["code"] = code
    return res.data


@route(bp, '/testVerifyCaptcha', methods=["POST"])
def test_verify_captcha():
    """
    验证图形验证码
    :return:
    """
    res = ResMsg()
    obj = request.get_json(force=True)
    code = obj.get('code', None)
    s_code = session.get("code", None)
    print(code, s_code)
    if not all([code, s_code]):
        res.update(code=ResponseCode.InvalidParameter)
        return res.data
    if code != s_code:
        res.update(code=ResponseCode.VerificationCodeError)
        return res.data
    return res.data


# --------------------JWT测试-----------------------------------------#

# @route(bp, '/testLogin', methods=["POST"])
# def test_login():
#     """
#     登陆成功获取到数据获取token和刷新token
#     :return:
#     """
#     res = ResMsg()
#     obj = request.get_json(force=True)
#     user_name = obj.get("name")
#     # 未获取到参数或参数不存在
#     if not obj or not user_name:
#         res.update(code=ResponseCode.InvalidParameter)
#         return res.data

#     if user_name == "qin":
#         # 生成数据获取token和刷新token
#         access_token, refresh_token = Auth.encode_auth_token(user_id=user_name)

#         data = {"access_token": access_token.decode("utf-8"),
#                 "refresh_token": refresh_token.decode("utf-8")
#                 }
#         res.update(data=data)
#         return res.data
#     else:
#         res.update(code=ResponseCode.AccountOrPassWordErr)
#         return res.data


# @route(bp, '/testGetData', methods=["GET"])
# @login_required
# def test_get_data():
#     """
#     测试登陆保护下获取数据
#     :return:
#     """
#     res = ResMsg()
#     name = session.get("user_name")
#     data = "{}，你好！！".format(name)
#     res.update(data=data)
#     return res.data


     
# --------------------测试Celery-------------------------------#


@route(bp, '/testCeleryAdd', methods=["GET"])
def test_add():
    """
    测试相加
    :return:
    """
    result = add.delay(1, 2)
    return result.get(timeout=1)


@route(bp, '/testCeleryFlaskflaskr.ontext', methods=["GET"])
def test_flask_app_context():
    """
    测试获取flask上下文
    :return:
    """
    result = flask_app_context.delay()
    return result.get(timeout=1)