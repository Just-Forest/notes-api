import os

from authx import AuthX, AuthXConfig
from dotenv import load_dotenv

load_dotenv()

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["headers"]
security: AuthX = AuthX(config=config)