FROM python:3.7-alpine

ARG mode 

COPY ./deploy/supervisord.conf /etc/supervisord.conf
COPY ./requirements.txt requirements.txt

RUN apk update && apk add --no-cache supervisor

# Install app dependencies
RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    && pip install -r requirements.txt \
    && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + \
    && runDeps="$( \
        scanelf --needed --nobanner --recursive /usr/local \
                | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                | sort -u \
                | xargs -r apk info --installed \
                | sort -u \
    )" \
    && apk add --virtual .rundeps $runDeps \
    && apk del .build-deps

RUN adduser -D -u 1000 appuser

#USER appuser

WORKDIR /app

COPY . /app

ENV PORT 80

EXPOSE $PORT

CMD [ "sh", "-c", "./deploy/entry.sh"]

