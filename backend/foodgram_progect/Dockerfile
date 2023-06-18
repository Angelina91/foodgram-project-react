FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install -U pip &&\
    pip3 install -r ./requirements.txt --no-cache-dir 
COPY . .
RUN chmod +x run_app.sh
ENTRYPOINT [ "/app/run_app.sh" ]
# CMD ["gunicorn", "foodgram_progect.wsgi:application", "--bind", "0:8000" ] 