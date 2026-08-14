from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from app.api.schema.error import ErrorResponse

from app.api.exceptions.conversation import ConversationNotFoundException


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(ConversationNotFoundException)
    async def conversation_not_found_handler(
        request: Request,
        exc: ConversationNotFoundException,
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content=ErrorResponse(
                code="CONVERSATION_NOT_FOUND",
                message=str(exc),
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred.",
            ).model_dump(),
        )