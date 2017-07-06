# Tulip Api
New version of graph-ryder-api with sockets to manage trace history

####1. change config file
```
cp config.example.ini config.ini
nano config.ini
```

## Local Installation
####2. install requirements
```
pip install -r requirements.txt
```
####3. Tulip dependencies

This project need tulip-python 5.0

The layout OrthoTree is needed to display the trace
 - See the tulip doc to add layout algorithm from folder orthotree
 - Or use another layout in graphtulip/manage.py line 151 for example 'Tree Leaf'


####4. launch api server
```
python app.py
```

## Docker Installation
####3. build
```
docker build -t graph-ryder-api .
```
####4. run
```
docker run -d -p 5000:5000 --name my-graph-ryder-api graph-ryder-api
```