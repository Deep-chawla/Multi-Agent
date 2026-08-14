from fastapi import APIRouter, Depends, Request, status

from app.api.schema.conversation import (ConversationResponse,ConversationListResponse,ConversationMessagesResponse)
from app.api.service.conversation import ConversationAPIService
from app.core.security import CurrentUser, get_current_user

router = APIRouter(prefix="/conversations",tags=["Conversations"],)


@router.post("/create", response_model=ConversationResponse,status_code=status.HTTP_201_CREATED,)
async def create_conversation(
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
):
    application = request.app.state.application

    service = ConversationAPIService(application)

    return service.create_conversation(current_user.id)


@router.get("/list", response_model=ConversationListResponse,status_code=status.HTTP_200_OK,)
async def list_conversations(
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
):
   
    application = request.app.state.application
    service = ConversationAPIService(application)
    return service.list_conversations(current_user.id)


@router.get("/{conversation_id}/messages",response_model=ConversationMessagesResponse,status_code=status.HTTP_200_OK,)
async def get_messages(
    conversation_id: str,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
):
    application = request.app.state.application
    service = ConversationAPIService(application)
    return service.get_messages(conversation_id, current_user.id)