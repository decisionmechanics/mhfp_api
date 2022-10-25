# docker build -t andrewtait/mhfp .
# docker run -d --name mhfp -p 8084:80 --rm andrewtait/mhfp

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY ./app /app/app