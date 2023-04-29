FROM maptiler/tileserver-gl

VOLUME /data
WORKDIR /data

RUN apt install -y python3-pip

COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

COPY main.py /main.py
RUN python3 /main.py
