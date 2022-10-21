# docker build -t andrewtait/csfp .
# docker run -d --name csfp -p 8084:80 --rm andrewtait/csfp

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY ./app /app/app