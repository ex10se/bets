FROM python:3.10-slim

COPY app/bet_maker/build/ /var/app/build/
COPY ci/.env* /
COPY ci/bet_maker/entrypoint.sh /

RUN pip install -r /var/app/build/requirements.txt

WORKDIR /var/app/

RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]
