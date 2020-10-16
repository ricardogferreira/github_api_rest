FROM python:3.6-alpine

WORKDIR /opt/workspace
RUN apk add --no-cache --update postgresql-dev build-base python3-dev

COPY requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh

COPY . .

CMD [ "sh", "app.sh" ]