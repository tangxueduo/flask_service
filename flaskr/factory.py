import os
import yaml

from flask import Flask, Blueprint
from flaskr.celery import celery_app
from .utils import db
from .api import auth, blog
from .api.router import router


def create_app(config_name=None, config_path=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # 读取配置文件
    if not config_path:
        pwd = os.getcwd()
        config_path = os.path.join(pwd, 'config/config.yaml')
    if config_name is None:
        config_name = 'PRODUCTION'

    # 读取配置文件
    conf = read_yaml(config_name, config_path)
    app.config.update(conf)
    
    # 更新Celery配置信息
    celery_conf = "redis://{}:{}/{}".format(app.config['REDIS_HOST'], app.config['REDIS_PORT'], app.config['REDIS_DB'])
    celery_app.conf.update({"broker_url": celery_conf, "result_backend": celery_conf})
    
    # 注册接口
    register_api(app=app, routers=router)

    # 注册数据库连接
    db.init_app(app)

    # 日志文件目录
    if not os.path.exists(app.config['LOGGING_PATH']):
        os.mkdir(app.config['LOGGING_PATH'])

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app

def register_api(app, routers):
    for router_api in routers:
        if isinstance(router_api, Blueprint):
            app.register_blueprint(router_api)
        else:
            try:
                endpoint = router_api.__name__
                view_func = router_api.as_view(endpoint)
                # 如果没有服务名,默认 类名小写
                if hasattr(router_api, "service_name"):
                    url = '/{}/'.format(router_api.service_name.lower())
                else:
                    url = '/{}/'.format(router_api.__name__.lower())
                if 'GET' in router_api.__methods__:
                    app.add_url_rule(url, defaults={'key': None}, view_func=view_func, methods=['GET', ])
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['GET', ])
                if 'POST' in router_api.__methods__:
                    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
                if 'PUT' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['PUT', ])
                if 'DELETE' in router_api.__methods__:
                    app.add_url_rule('{}<string:key>'.format(url), view_func=view_func, methods=['DELETE', ])
            except Exception as e:
                raise ValueError(e)
def read_yaml(config_name, config_path):
    """
    config_name:需要读取的配置内容
    config_path:配置文件路径
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')