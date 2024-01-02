from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from routes import router

app = FastAPI()
app.include_router(router)

