FROM python:3.8.16-alpine

COPY ./src /src
WORKDIR /src

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "main.py"]