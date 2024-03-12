from flaskr.api.api_test import bp as bp_api_test
from flaskr.api.auth import bp as bp_auth
from flaskr.api.blog import bp as bp_blog
router = [
    bp_api_test,  # 接口测试
    bp_auth,
    bp_blog
]