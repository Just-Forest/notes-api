from authx import AuthX, AuthXConfig

from src.config import settings

config = AuthXConfig()
config.JWT_SECRET_KEY = settings.jwt_secret_key
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["headers"]
security: AuthX = AuthX(config=config)
