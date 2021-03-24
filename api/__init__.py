from flask import Blueprint

api_bp = Blueprint("api", __name__, url_prefix='/api/v1')

from . import auth  # 身份认证api
from . import post  # 树洞功能api
from . import su    # 管理员api