FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:5000", "wsgi:app"]
