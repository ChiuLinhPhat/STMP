from fastapi import FastAPI ,Request
from starlette.background import BackgroundTasks
from  fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles

from config import MailBody
from schemas import send_mail


app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def index():
    return {"status": "fastapi mailserver is running."}


@app.post("/send-email", )
async def schedule_mail(req: MailBody, tasks: BackgroundTasks,request: Request):
    data = req.dict()
    # content= templates.TemplateResponse("MessageType.html", {"request": request}).body
    tasks.add_task(send_mail(data),data)
    # send_mail(data)
    return {"status": 200, "message": "email has been scheduled"}

@app.get("/send-email",response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("MessageType.html", {"request": request})