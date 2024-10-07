FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

ARG IDEA_MONGODB_URI
ENV IDEA_MONGODB_URI=${IDEA_MONGODB_URI}

CMD ["python", "run_api.py"]