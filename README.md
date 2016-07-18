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
3. include Export Sigma Plugin
```
cp exportsigma.py /usr/local/lib/python3.5/site-packages/tulip/native/plugins/exportsigma.py
```
4. launch api server
```
python app.py
```

### with docker
2. Dockerfile
```
FROM python:3-onbuild
EXPOSE 5000
COPY exportsigma.py /usr/local/lib/python3.5/site-packages/tulip/native/plugins/exportsigma.py
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

## Generate static graphs
- via web browser
```
http://localhost:5000/generateGraphs
```
- via graph-ryder-dashboard settings / Generate Graphs
```
http://localhost:9000/#/dashboard/settings
```

### Generate the apidoc
- install apidoc
```
npm install apidoc -g
```
- generate the doc
```
apidoc -i ./routes/ -o ./routes/apidoc/
```