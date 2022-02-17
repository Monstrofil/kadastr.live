FROM tiangolo/uvicorn-gunicorn:python3.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

RUN apt update
RUN apt install -y binutils libproj-dev gdal-bin

COPY ./ /app