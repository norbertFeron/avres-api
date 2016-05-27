# Graph Rider Api
This is a simple Rest full Api to interact with neo4j database and query opencare users, posts and comments

## How to
1. change config file
```
cp config.example.ini config.ini
nano config.ini
```

### locally
2. install requirements
```
pip install -r requirements.txt
```
3. launch api server
```
python app.py
```

### with docker
2. Dockerfile
```
FROM python:3-onbuild
EXPOSE 5000
CMD [ "python", "./app.py" ]
```
3. build
```
docker build -t graph-ryder-api .
```
4. run
```
docker run -d -p 5000:5000 --name my-graph-ryder-api graph-ryder-api
```