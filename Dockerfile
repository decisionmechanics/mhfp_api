# docker build -t bcrfpmhapi .
# docker run -d --name bcrfpmhapi -p 8084:80 --rm bcrfpmhapi

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY ./app /app/app