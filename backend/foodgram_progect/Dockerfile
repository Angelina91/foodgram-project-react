FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt .

# уточнить правильность "/"
RUN pip3 install -r ./requirements.txt --no-cache-dir 

# уточнить: ". ." или "./ /"
COPY . .

CMD ["gunicorn", "foodgram_progect.wsgi:application", "--bind", "0:8000" ] 