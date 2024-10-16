import asyncio

from typing import Annotated

from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel

from images import jail, pet

# Disable docs because we are not using it
__version__ = "1.0.0-alpha.2"
app = FastAPI(openapi_url=None, version=__version__)


@app.get("/")
def get_root():
    return {"version": app.version}


@app.post("/jail")
async def post_jail(file: UploadFile = File(...)):
    # Read the uploaded image
    contents = await file.read()

    # Add jail overlay to the image and return it
    contents = await asyncio.to_thread(jail, contents)

    return StreamingResponse(contents, media_type="image/png")


@app.post("/pet")
async def post_pet(file: UploadFile = File(...)):
    # Read the uploaded image
    contents = await file.read()

    # Add pet overlay to the image and return it
    contents = await asyncio.to_thread(pet, contents)

    return StreamingResponse(contents, media_type="image/gif")


@app.exception_handler(NotImplementedError)
async def not_implemented_error_handler(request: Request, exc: NotImplementedError):
    return JSONResponse(
        status_code=503,
        content={"detail": "This feature is not implemented yet."},
    )
