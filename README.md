# shaclAPI

Web server wrapping the TopBraid Shacl API tool. 
Implementated for Imaging Plaza. 
Based on https://github.com/SDSC-ORD/shacl

## How to use it?



## How to use docker?

```
docker build -t sdsc-ordes/shacl-api:latest . 
```

```
docker run -it --rm -p 8000:15400 -p 8501:8501 sdsc-ordes/shacl-api:latest 
docker run -it --rm -p 7200:15400 -p 3000:8501 sdsc-ordes/shacl-api:latest 
```

```
docker-compose up # add -d for detached
```

## LOGS

```
if [ $1 == validate ] ; then
	set -- shaclvalidate.sh "$@"
elif [ $1 == infer ] ; then
	set -- shaclinfer.sh "$@"
```

```
root@cbb169b97823:/# shaclvalidate.sh
Missing -datafile, e.g.: -datafile myfile.ttl
root@cbb169b97823:/# shaclinfer.sh
Missing -datafile, e.g.: -datafile myfile.ttl
```

# Changelog

- v0.0.5: Update Ontology to v0.8
- v0.0.4: Update Ontology to v0.6
- v0.0.3: Update shapesfile to v0.0.3
