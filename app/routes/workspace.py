from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "../templates")
)


@router.get("/workspace", response_class=HTMLResponse)
async def workspace(request: Request):

    return templates.TemplateResponse(
        "pages/workspace.html",
        {
            "request": request
        }
    )