FROM python:3.10-slim-bullseye

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libssl-dev

RUN pip install cryptography
RUN pip install pyinstaller

RUN useradd -ms /bin/bash student
USER student

ENV HOME /home/student
WORKDIR $HOME/app

CMD [ "tail", "-f", "/dev/null" ]
