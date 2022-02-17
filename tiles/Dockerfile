FROM ubuntu:20.04

COPY tegola .
COPY static /static
COPY configs /configs

RUN chmod +x tegola

ENTRYPOINT ./tegola serve --config=/configs/tegola.toml
