# syntax=docker/dockerfile:1

ARG BUILD_ENV=copy

FROM louis-data AS build_copy
ARG LOUIS_SCHEMA
WORKDIR /data
ONBUILD COPY dumps/${LOUIS_SCHEMA}/ /data

FROM louis-data AS build_nocopy
ONBUILD RUN echo "No data copied, mount data to /data"

FROM build_${BUILD_ENV}
RUN apk add && apk add postgresql-client
COPY docker-entrypoint.sh /entrypoint.sh
ENV LOUIS_DSN=
ENV LOUIS_SCHEMA=
ENV LOAD_DATA_ONLY=
ENV DISABLE_TRIGGER_ALL=
ENV DROP_SCHEMA=
VOLUME /data
ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]
