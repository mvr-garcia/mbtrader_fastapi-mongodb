FROM python:3.9

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc wget

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# # TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz
RUN pip install ta-lib

COPY . /code/

EXPOSE 8000