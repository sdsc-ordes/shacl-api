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
docker run -it --rm -p 8000:15400 -p 8501:8501 -v $(pwd)/app:/app sdsc-ordes/shacl-api:latest 
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
