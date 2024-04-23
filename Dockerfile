FROM python:latest

COPY requirements.txt /usr/src/app/

RUN pip3 install -r /usr/src/app/requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

EXPOSE 5000

ENTRYPOINT ["python3", "main.py"]
