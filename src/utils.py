from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from typing import Literal
from src.schemas import ResponseBaseWithObject, ResponseBase


def create_response(
        message: str,
        status: Literal['success', 'error'] = 'success',
        obj=None,
        **kwargs,
):
    # todo: consider customizing JSONResponse class:
    #  https://github.com/zhanymkanov/fastapi-best-practices/issues/4#:~:text=Custom%20Response%20Serializers%20%26%20BaseSchema

    if obj:
        content = ResponseBaseWithObject(
            status=status,
            detail=message,
            obj=obj,
        )
    else:
        content = ResponseBase(
            status=status,
            detail=message,
        )

    return JSONResponse(
        content=jsonable_encoder(content),
        **kwargs
    )
