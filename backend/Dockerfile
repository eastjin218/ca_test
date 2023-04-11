FROM pytorch/pytorch:1.12.1-cuda11.3-cudnn8-runtime

COPY ./src /src
WORKDIR /src

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5001

CMD ["python3", "main.py"]