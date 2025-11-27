from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles#for getting simple html page for login,register and dashboard
from fastapi.responses import FileResponse


app = FastAPI()


@app.get("/")# connecting static pages to url/endpoint
def home():
    return FileResponse("static/login.html")


@app.get("/register-page")
def register_page():
    return FileResponse("static/register.html")


@app.get("/dashboard")
def dashboard_page():
    return FileResponse("static/dashboard.html")