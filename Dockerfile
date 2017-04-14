FROM python:3.6.1

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

# librdkafka
ENV LIBRDKAFKA_VERSION 0.9.4
RUN curl -Lk -o /root/librdkafka-${LIBRDKAFKA_VERSION}.tar.gz https://github.com/edenhill/librdkafka/archive/v${LIBRDKAFKA_VERSION}.tar.gz && \
    tar -xzf /root/librdkafka-${LIBRDKAFKA_VERSION}.tar.gz -C /root && \
    cd /root/librdkafka-${LIBRDKAFKA_VERSION} && \
    ./configure && make && make install && ldconfig && make clean && ./configure --clean

# install python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /code

# copy application code
COPY . /code

# expose default connection port
EXPOSE 8000
