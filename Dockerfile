FROM python:3.6-alpine

WORKDIR /opt/workspace
RUN apk add --no-cache --update gcc postgresql-dev jpeg-dev bash build-base python3-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

CMD [ "bash", "app.sh" ]