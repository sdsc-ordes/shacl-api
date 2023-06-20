from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import subprocess
import os
import base64

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the SHACL API"}


@app.post("/validate")
def validate(datafile:str=Form(...), 
             shapesfile:str=Form(...)):
 
    datafile = base64.b64decode(str.encode(datafile))
    shapesfile = base64.b64decode(str.encode(shapesfile))
    print(datafile)

    with open("datafile.ttl", 'wb') as f: 
         f.write(datafile)
    
    with open("shapesfile.ttl", 'wb') as f: 
         f.write(shapesfile)

    output = subprocess.run(["shaclvalidate.sh", "-datafile", "datafile.ttl", "-shapesfile", "shapesfile.ttl"], stdout=subprocess.PIPE)

    os.remove("datafile.ttl")
    os.remove("shapesfile.ttl")
    with open("validationTest.ttl", 'wb') as f: 
         f.write(output.stdout)

    return {"output": output.stdout}


@app.post("/inference")
def validate(datafile:str=Form(...), 
             shapesfile:str=Form(...)):
 
    datafile = base64.b64decode(str.encode(datafile))
    shapesfile = base64.b64decode(str.encode(shapesfile))
    print(datafile)

    with open("datafile.ttl", 'wb') as f: 
         f.write(datafile)
    
    with open("shapesfile.ttl", 'wb') as f: 
         f.write(shapesfile)

    output = subprocess.run(["shaclinfer.sh", "-datafile", "datafile.ttl", "-shapesfile", "shapesfile.ttl"], stdout=subprocess.PIPE)

    os.remove("datafile.ttl")
    os.remove("shapesfile.ttl")
    with open("validationTest.ttl", 'wb') as f: 
         f.write(output.stdout)

    return {"output": output.stdout}
