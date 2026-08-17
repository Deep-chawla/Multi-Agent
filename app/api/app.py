from fastapi import FastAPI
from app.api.exceptions.globalException import register_exception_handlers
from fastapi.middleware.cors import CORSMiddleware

from bootstrap.server import start_application
from app.api.routes.chat import router as chat_router
from app.api.routes.conversation import router as conversation_router
from app.database.base import Base
from app.database.session import engine

application = start_application()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "https://police-espresso-buffer.ngrok-free.dev",
        "https://rearview-bobbing-obscure.ngrok-free.dev",
        "https://sporting-zombie-kennel.ngrok-free.dev",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.application = application

register_exception_handlers(app)

Base.metadata.create_all(bind=engine)

app.include_router(conversation_router)
app.include_router(chat_router)