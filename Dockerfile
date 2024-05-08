FROM python:3.12-slim-bookworm

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD [ "python", "api/app.py"]
# We run our service on port 5000