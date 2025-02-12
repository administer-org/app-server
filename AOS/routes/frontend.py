# pyxfluff 2024-2025

from AOS import globals
from AOS.database import db

from ..frontend import *

if not globals.is_dev:
    from AOS.reporting.report import daily_report
else:
    def daily_report(db):
        print("[x] Request to spawn daily report ignored due to missing modules")


from time import time
from pathlib import Path

from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

root = Path(__file__).parents[1]
day = 0


class Frontend():
    def __init__(self, app):
        self.app = app
        self.t = time()
    
    def initialize_frontend(self):
        @self.app.get("/")
        async def index(req: Request):
            global day

            if day != round(time() / 86400):
                day = round(time() / 86400)
                (globals.is_dev) and print(
                    "Ignoring reporting request, this will go through on prod"
                ) or daily_report(db)

            return FileResponse(root / "frontend" / "index.html")


        @self.app.get("/app/{app:str}")
        def app_frontend(req: Request, app: str):
            pass


        @self.app.get("/to/{path:path}")
        def social_to(path: str):
            if path.startswith("discord"):
                return RedirectResponse("https://discord.gg/3Q8xkcBT3M")
            elif path.startswith("git"):
                return RedirectResponse(
                    f"https://github.com/administer-org/{path.removeprefix("git/")}"
                )
            elif path.startswith("discourse"):
                return RedirectResponse(
                    "https://devforum.roblox.com/t/administer-modern-modular-free-admin-system-12/3179989"
                )
            elif path.startswith("roblox"):
                return RedirectResponse(
                    "https://create.roblox.com/store/asset/127698208806211/Administer"
                )
            elif path.startswith("docs"):
                return RedirectResponse("https://docs.administer.notpyx.me")

            return {"error": "That path isn't a valid shortlink."}


        for mount in [
            ("/", StaticFiles(directory=root / "frontend")),
        ]:
            self.app.mount(*mount)
