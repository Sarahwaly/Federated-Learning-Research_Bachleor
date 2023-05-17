FROM ubuntu:20.04 AS builder

WORKDIR /start

COPY experiment/fedat/run_fedat_distributed.sh /start/

RUN chmod +x /start/run_fedat_distributed.sh

FROM ubuntu:20.04

COPY --from=builder /start/run_fedat_distributed.sh /start/

ENTRYPOINT ["bash", "run_fedat_distributed.sh"]
