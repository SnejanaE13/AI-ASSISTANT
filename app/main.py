from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.db.database import Base, engine
from app.api.routers import auth, chat

app = FastAPI(
    title="Ultron Learning Assistant API",
    description="API для регистрации, авторизации и работы чат-бота.",
    version="0.1.0",
    docs_url="/api/docs",  # Документация, как в тз
    redoc_url="/api/redoc",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Настройка CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для простоты разработки
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Создание таблиц при старте
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/main", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
