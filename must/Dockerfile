FROM alpine:latest

RUN apk add --update --no-cache python3 py3-pip gcc python3-dev musl-dev
RUN pip3 install --no-cache --upgrade pip setuptools minimalmodbus influxdb influxdb-client[ciso]

RUN mkdir /must
WORKDIR /must
COPY ./must.py /must

RUN echo "* * * * * python3 /must/must.py" >> /etc/crontabs/root && crontab -l
CMD crond -f -l 8
