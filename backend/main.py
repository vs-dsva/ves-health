from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

services = [
    {"id": "HRM", "urls": [
        {"url": "/ping", "state": "ok"}
    ]},
    {"id": "ECONOMY", "urls": [

    ]},  
    {"id": "PROCUREMENT", "urls": [

    ]}, 
    {"id": "COMMON", "urls": [

    ]}
]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/status")
async def status():
    for service in services:
        urls = {}
        for url in service["urls"]:
            # do the real ping here 
            url["state"] = "ok"
    return services

