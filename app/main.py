from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the SHACL API"}