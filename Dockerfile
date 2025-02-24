FROM python:3.9

WORKDIR /app
COPY . /app

RUN apt update && apt install -y gcc && pip3 install -r requirements.txt
RUN gcc raj.c -o raja -pthread && chmod +x raja

CMD ["python3", "bot.py"]
