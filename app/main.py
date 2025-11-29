from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from app.db.database import Base, engine
from app.api.routers import auth, chat
from app.api.routers import states
from app.core.config import settings


from app.llm_client import send_prompt

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.PROJECT_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def check_authentication(request: Request, call_next):
    public_paths = ["/", "/login", "/static", "/docs", "/redoc", "/api/auth"]
    
    if any(request.url.path.startswith(path) for path in public_paths):
        return await call_next(request)
    
    session_token = request.cookies.get("session_token")
    auth_header = request.headers.get("authorization")
    
    if not session_token and not auth_header:
        return RedirectResponse(url="/login")
    
    response = await call_next(request)
    return response


# Создание таблиц при старте
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    # Проверяем подключение к Ollama
    try:
        test = send_prompt("ping")
        print("LLM connected:", test)
    except Exception as e:
        print("LLM connection error:", e)


app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(states.router, prefix="/api", tags=["States"])

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/main", response_class=HTMLResponse)
async def read_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})
