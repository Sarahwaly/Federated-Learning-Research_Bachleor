FROM alpine:3.13 AS builder

WORKDIR /start

COPY experiment/fedat/ /start/

RUN apk add --no-cache --upgrade bash

RUN chmod +x run_fedat_distributed.sh
RUN ./run_fedat_distributed.sh

FROM scratch

COPY --from=builder /start/myfedat /

ENTRYPOINT ["/myfedat"]
