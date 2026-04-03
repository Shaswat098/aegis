FROM python:3.11-slim

WORKDIR /app

COPY requirements/base.txt /app/requirements.txt

RUN apt-get update && apt-get install -y libgomp1

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]