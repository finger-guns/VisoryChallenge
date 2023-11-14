from enum import Enum
from json import loads
from os import getenv
from os.path import dirname, join

from api._shared.schema.base import WhereIsItBaseModel
from pydantic import Field
from pydantic_settings import BaseSettings


class EnvironmentTypes(str, Enum):
    LOCAL = "LOCAL"

    LOCAL_DEVELOPMENT = "LOCAL_DEVELOPMENT"
    LOCAL_USER_ACCEPTANCE_TESTING = "LOCAL_UAT"
    LOCAL_PRODUCTION = "LOCAL_PRODUCTION"

    DEVELOPMENT = "DEVELOPMENT"
    USER_ACCEPTANCE_TESTING = "USER_ACCEPTANCE_TESTING"
    PRODUCTION = "PRODUCTION"


def get_version() -> str:
    with open(join(dirname(__file__), "version.json"), "r") as f:
        version = loads(f.read())
        return version


class Settings(BaseSettings):
    SERVICE_NAME: str = "where_is_it"

    APP_BASE_URL: str = "/where_is_it/"
    APP_TITLE: str = "where_is_it"
    APP_VERSION: str = get_version() or "0.0.0"
    APP_DESCRIPTION: str = "Where is something streaming"

    VERBOSE_LOGGING: bool = True
    RETURN_EXCEPTION_REASON: bool = True

    BACKEND_ERROR_MESSAGE: str = "The backend encounted and error."
    DATABASE_ERROR_MESSAGE: str = "An error occured while accessing the database."

    ENVIRONMENT_TYPE: str = getenv(
        "ENVIRONMENT_TYPE",
        default=EnvironmentTypes.LOCAL,
    )

    USE_SSL: bool = False

    SSL_SERVER_CA_PATH: str = ""
    SSL_CERT_PATH: str = ""
    SSL_KEY_PATH: str = ""

    TICKETMASTER_API_URL: str = "https://app.ticketmaster.com/discovery/v2/"
    TICKETMASTER_API_KEY: str = Field(default="")

    class Config:
        secrets_dir = "/etc/"


class WhereIsItLogConfig(WhereIsItBaseModel):
    LOGGER_NAME: str = "where_is_it"
    LOG_FORMAT: str = "%(levelprefix)s | %(path)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers: dict = {
        "where_is_it": {"handlers": ["default"], "level": LOG_LEVEL},
    }
