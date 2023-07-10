from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
import subprocess
import os
import base64

from rdflib import Graph
from rdflib.namespace import Namespace, NamespaceManager

import requests

app = FastAPI()

@app.get("/")
def index():
    return {"title": "Hello, welcome to the SHACL API"}

@app.post("/validate-jsonld")
def validate(data:str=Form(...)):

     # This is generating the datafile necesary to run inference.
     graph = Graph()
     graph.parse(data=data, format="json-ld")
     
     SCHEMA = Namespace("http://schema.org/")
     graph.namespace_manager.bind('schema', SCHEMA, override=True, replace=True)
     graph.serialize(destination='datafile.ttl',format='turtle')


     # Download from github and rename as shapesfile.ttl
     # It seems I can use the token just before the web. 
     # https://stackoverflow.com/questions/18126559/how-can-i-download-a-single-raw-file-from-a-private-github-repo-using-the-comman
     #shapesfile = requests.get("https://raw.githubusercontent.com/SDSC-ORD/ImagingPlazaSHACL/main/ImagingOntologyShapes.ttl?token=GHSAT0AAAAAAB6SMHWSF2NPK74LPFTKLDJAZFFZCFA")
     #shapesfile = shapesfile.content

     #with open("shapesfile.ttl", 'wb') as f: 
     #    f.write(shapesfile)

     output = subprocess.run(["shaclvalidate.sh", "-datafile", "datafile.ttl", "-shapesfile", "/app/shapesfile.ttl"], stdout=subprocess.PIPE)

     os.remove("datafile.ttl")
     #os.remove("shapesfile.ttl")

     ### Read and provide JSON-LD
     graph = Graph()
     graph.parse(output.stdout, format="turtle")
     SCHEMA = Namespace("http://schema.org/")
     graph.namespace_manager.bind('schema', SCHEMA, override=True, replace=True)
     jsonld = str(graph.serialize(format='json-ld'))

     return {"output": jsonld}


@app.post("/inference-jsonld")
def validate(data:str=Form(...)):
 
     # This is generating the datafile necesary to run inference.
     graph = Graph()
     graph.parse(data, format="json-ld")
     
     SCHEMA = Namespace("http://schema.org/")
     graph.namespace_manager.bind('schema', SCHEMA, override=True, replace=True)
     graph.serialize(destination='datafile.ttl',format='turtle')


     # Download from github and rename as shapesfile.ttl
     # It seems I can use the token just before the web. 
     # https://stackoverflow.com/questions/18126559/how-can-i-download-a-single-raw-file-from-a-private-github-repo-using-the-comman
     #shapesfile = requests.get("https://raw.githubusercontent.com/SDSC-ORD/ImagingPlazaSHACL/main/ImagingOntologyShapes.ttl?token=GHSAT0AAAAAAB6SMHWSF2NPK74LPFTKLDJAZFFZCFA")
     #shapesfile = shapesfile.content

     #with open("shapesfile.ttl", 'wb') as f: 
     #    f.write(shapesfile)

     output = subprocess.run(["shaclinfer.sh", "-datafile", "datafile.ttl", "-shapesfile", "/app/shapesfile.ttl"], stdout=subprocess.PIPE)

     os.remove("datafile.ttl")
     #os.remove("shapesfile.ttl")

     ### Read and provide JSON-LD
     graph = Graph()
     graph.parse(output.stdout, format="turtle")
     SCHEMA = Namespace("http://schema.org/")
     graph.namespace_manager.bind('schema', SCHEMA, override=True, replace=True)
     jsonld = str(graph.serialize(format='json-ld'))

     return {"output": jsonld}



@app.post("/validate")
def validate(datafile:str=Form(...), 
             shapesfile:str=Form(...)):
 
    datafile = base64.b64decode(str.encode(datafile))
    shapesfile = base64.b64decode(str.encode(shapesfile))

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
