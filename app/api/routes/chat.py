from fastapi import APIRouter,Depends,Request
from fastapi.responses import StreamingResponse
from fastapi import status
from app.api.service.conversation import ConversationAPIService

from app.api.schema.chat import SendMessageRequest,SendMessageResponse
from app.api.service.chat import ChatService
from app.core.security import CurrentUser, get_current_user

router = APIRouter(prefix="/chat",tags=["Chat"],)

@router.post("/{conversation_id}/messages", status_code=status.HTTP_200_OK)
async def send_message(
    conversation_id: str,
    body: SendMessageRequest,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
):
    application = request.app.state.application
    service = ChatService(application)
    conService = ConversationAPIService(application)

    conService.require_conversation(conversation_id, current_user.id)

    return StreamingResponse(
        service.stream_message(
            conversation_id=conversation_id,
            message=body.message,
            user=current_user,          # <-- pass it through
        ),
        media_type="text/event-stream",
    )