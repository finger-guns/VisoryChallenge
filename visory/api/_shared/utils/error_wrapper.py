from asyncio import iscoroutinefunction
from functools import wraps
from traceback import format_exc

from fastapi import HTTPException, status

from api.config import get_settings
from api._shared.schema.error import WhereIsItHTTPException
from .logger import error, debug

settings = get_settings()


def catch_general_exceptions_to_http(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            if iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        except Exception as e:
            debug(message=str(e))
            error_message = format_exc()
            if not isinstance(e, (HTTPException, WhereIsItHTTPException)):
                user_msg = settings.BACKEND_ERROR_MESSAGE
                if settings.RETURN_EXCEPTION_REASON:
                    error(message=str(e))
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=error_message,
                        user_message=user_msg,
                    )
                else:
                    error(message=str(e))
                    raise WhereIsItHTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        message=user_msg,
                        user_message=user_msg,
                    )
            else:
                error(message=str(e))
                raise e

    return wrapper
