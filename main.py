from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient
import os

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client.dynamic_site

ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

@app.get("/")
def home(request: Request):
    notes = list(db.notes.find())
    news = list(db.news.find())
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "notes": notes, "news": news}
    )

@app.get("/admin")
def admin_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/admin")
def admin_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if username == ADMIN_USER and password == ADMIN_PASS:
        return templates.TemplateResponse("admin.html", {"request": request})
    return RedirectResponse("/admin", status_code=302)

@app.post("/add-note")
def add_note(title: str = Form(...), content: str = Form(...)):
    db.notes.insert_one({"title": title, "content": content})
    return RedirectResponse("/admin", status_code=302)

@app.post("/add-news")
def add_news(title: str = Form(...)):
    db.news.insert_one({"title": title})
    return RedirectResponse("/admin", status_code=302)
