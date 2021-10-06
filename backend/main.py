from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sse_starlette.sse import EventSourceResponse

from typing import List, Optional
from pydantic import BaseModel

import os
import requests_async as requests
import time
from datetime import datetime
import json
from starlette.routing import Host
import yaml
from yaml.loader import SafeLoader

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

uptime = {}

class Endpoint(BaseModel):
  url: str
  state: str
  uptime = 0
  class Config:
    allow_mutation = True

class Service(BaseModel):
  id: str
  endpoints: List[Endpoint]
  uptime: Optional[str]
  class Config:
    allow_mutation = True


class ServiceList:
  services = List[Service]

#BASE = "http://{}.{}/".format(os.env("TENANT_ID"), "enterprise-test.visma.no")
BASE = "http://customer1.enterprise-test.visma.no"

_services = yaml.load(open("services.yaml").read(), Loader=SafeLoader)
services = []
for s in _services:
  services.append(Service(**s))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
  return templates.TemplateResponse("index.html", {"request": request})


async def fetchData() -> List[Service]:
  for service in services:
    for endpoint in service.endpoints:
      # do the real ping here 
      __now = datetime.utcnow()
      if uptime.get(endpoint.url) == None:
        uptime[endpoint.url] = __now
      #print("Trying: {}/{}".format(BASE, endpoint.url))
      r = await requests.get(BASE + endpoint.url, timeout = 1)
      if r.status_code == 200:
        endpoint.state = "ok"
        endpoint.uptime = (__now - uptime[endpoint.url]).total_seconds()
      else:
        endpoint.state = "nok"
        uptime[endpoint.url] = __now
      # url.state = random.choice(["ok", "nok"])
    minUptime = min([endpoint.uptime for endpoint in service.endpoints])
    service.uptime  = "{} days {} hours {} minutes".format(int(minUptime/(24*3600)), int(minUptime/3600), int(minUptime/60)) 
  return services


@app.get("/status")
async def status() -> List[Service]:
  return await fetchData()

async def statusEventGenerator():
  while True:
    yield await fetchData()
    time.sleep(3)

@app.get("/stream")
async def streamData(request:Request):
  eventGenerator = statusEventGenerator()
  return EventSourceResponse(eventGenerator)
