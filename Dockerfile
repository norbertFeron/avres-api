FROM python:3.5

ADD requirements.txt /tmp/requirements.txt
RUN cd /tmp && pip install -r requirements.txt

COPY exportsigma.py /usr/local/lib/python3.5/site-packages/tulip/native/plugins/exportsigma.py

WORKDIR /opt/app
ADD . /opt/app

EXPOSE 5000
CMD [ "python", "./app.py" ]
