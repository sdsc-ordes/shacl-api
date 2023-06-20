# shaclAPI
Implementation of Imaging Plaza Microservice for SHACL Validation

Based in https://github.com/SDSC-ORD/shacl

## How to use it?



## How to use docker?

```
docker build -t caviri/shaclAPI:latest . 
```

```
docker run -it --rm -p 8000:15400 caviri/shaclapi:latest bash
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