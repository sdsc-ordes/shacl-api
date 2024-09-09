# shaclAPI
Implementation of Imaging Plaza Microservice for SHACL Validation

Based in https://github.com/SDSC-ORD/shacl

## How to use it?



## How to use docker?

```
docker build -t caviri/shaclapi:latest .
```

```
docker run --rm -p 8501:15400 caviri/shaclapi:latest
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

v0.0.4: Update Ontology to v0.6
v0.0.3: Update shapesfile to v0.0.3