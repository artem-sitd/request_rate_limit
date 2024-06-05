from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from crud import router as crud_router
from database import engine, Base

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="./frontend"), name="frontend")

app.include_router(crud_router)


@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("frontend/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
