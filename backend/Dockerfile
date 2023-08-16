FROM python:3.7-slim
# RUN apt update && apt install -y libpq-dev gcc
RUN apt update && apt install -y libpq-dev gcc netcat-traditional

LABEL author='Angelina91' prodject='foodgram_progect'

WORKDIR /app
COPY requirements.txt ./

RUN pip install -U pip &&\
    pip install -r requirements.txt --no-cache-dir
COPY . .

RUN chmod +x run_app.sh
# CMD ["bash", "/app/run_app.sh"]
ENTRYPOINT ["/app/run_app.sh"]
