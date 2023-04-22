FROM python:3.10-slim

COPY app/line_provider/build/ /var/app/build/
COPY ci/.env* /

RUN pip install -r /var/app/build/requirements.txt

WORKDIR /var/app/

CMD ["uvicorn", "server:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
