FROM alpine:3.13 AS builder

WORKDIR /start

COPY experiment/fedat/run_fedat_distributed.sh/ /start/

RUN apk add --no-cache --upgrade python3

FROM python:3.9-alpine

COPY --from=builder /start/run_fedat_distributed.sh /start/

WORKDIR /start

ENTRYPOINT ["python3", "run_fedat_distributed"]



