from bootstrap.server import Application
from app.adapters.langchain.message_adapter import LangChainMessageAdapter
from app.api.exceptions.globalException import ConversationNotFoundException
from app.config.settings import logger
import asyncio
import json
from app.core.security import CurrentUser


class ChatService:

    def __init__(self, application):
        self.app = application

    async def stream_message(self, conversation_id: str, message: str, user: CurrentUser):
        conversation_service = self.app.conversation_service
        conversation = conversation_service.get_conversation(conversation_id)

        conversation_service.add_user_message(conversation_id=conversation.id, content=message)

        history = conversation_service.get_history(conversation.id)
        is_new_conversation = len(history) == 1

        title_task = None
        if is_new_conversation:
            title_task = asyncio.create_task(
                self.app.conversation_title_agent.generate_title(message)
            )

        langchain_messages = LangChainMessageAdapter.to_langchain(history)

        # Inject identity as a SystemMessage at the front of the message list
        from langchain_core.messages import SystemMessage
        identity_message = SystemMessage(
            content=f"The current logged-in user's name is {user.name}. "
                    f"Their user id is {user.id}. Use this if they ask about themselves."
        )
        langchain_messages = [identity_message] + langchain_messages

        logger.info(langchain_messages)

        final_response = ""
        async for chunk, metadata in self.app.workflow.graph.astream(
            {"messages": langchain_messages},
            stream_mode="messages",
        ):

            if metadata.get("langgraph_node") != "final_response":
                continue

            if not chunk.content:
                continue

            final_response += chunk.content

            # Proper SSE framing ("data: ...\n\n") instead of raw text.
            # Content-Type is already text/event-stream — proxies and
            # browsers specifically flush real SSE-framed events
            # immediately, whereas unframed chunked text claiming to be
            # event-stream can get buffered by intermediaries (this is
            # what was happening through the ngrok tunnel).
            # json.dumps also safely escapes newlines inside the token,
            # which would otherwise break SSE framing.
            payload = json.dumps({"content": chunk.content})
            yield f"data: {payload}\n\n"

        yield "event: done\ndata: {}\n\n"

        # Save complete assistant response
        conversation_service.add_assistant_message(
            conversation_id=conversation.id,
            content=final_response,
            agent="multi-agent",
        )
        if title_task:
            title = await title_task

            conversation_service.update_title(
                conversation.id,
                title.title,
            )