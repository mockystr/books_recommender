FROM python:3.7

COPY requirements.txt /
RUN pip install -r /requirements.txt

WORKDIR /code
COPY api api
COPY model model
COPY scripts scripts


EXPOSE 8080
CMD ["./scripts/aioserver_setup.sh"]
