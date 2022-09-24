# docker build -t bcrcalc .
# docker run -d --name bcrcalc -p 8084:80 --rm bcrcalc

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY ./app /app/app