FROM python:3.12-alpine

RUN apk update
RUN apk add fontconfig poppler-utils
RUN apk add --no-cache font-noto font-dejavu font-liberation
RUN apk add --no-cache font-microsoft

ENTRYPOINT ["tail", "-f", "/dev/null"]

