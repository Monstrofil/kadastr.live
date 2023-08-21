FROM maptiler/tileserver-gl

VOLUME /data
WORKDIR /data

RUN echo "deb http://archive.debian.org/debian stretch main contrib non-free" | tee /etc/apt/sources.list
RUN apt update
RUN apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev -y


RUN wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz && tar -xf Python-3.9.7.tgz \
    && cd Python-3.9.7 && ./configure --enable-optimizations && make -j 8 && make altinstall

COPY requirements.txt /requirements.txt
RUN python3.9 -m pip install -r /requirements.txt

COPY main.py /main.py
RUN python3.9 /main.py
