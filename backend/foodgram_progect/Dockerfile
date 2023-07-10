FROM python:3.7-slim

# LABEL author='Angelina91' prodject='foodgram_progect'

# RUN apt-get update &&\
#     apt-get upgrade -y &&
#     # apt-get install - libpg-dev gcc netcat

WORKDIR /app
COPY requirements.txt ./

RUN pip install -U pip &&\
    pip3 install -r requirements.txt --no-cache-dir 
COPY ./ /

RUN chmod +x run_app.sh
ENTRYPOINT [ "/app/run_app.sh" ]
# CMD ["gunicorn", "foodgram_progect.wsgi:application", "--bind", "0:8000" ] 