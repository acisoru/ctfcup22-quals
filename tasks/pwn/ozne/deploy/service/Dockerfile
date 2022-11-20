FROM ubuntu:22.10

RUN apt-get update -yyq && apt-get upgrade -yyq
RUN apt install socat -yyq
RUN apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    git \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -M -s /bin/false ctf
RUN mkdir /tmp/nsjail && cd /tmp/nsjail && git clone https://github.com/google/nsjail && cd nsjail && make && mv nsjail /bin && rm -rf -- /nsjail

COPY entrypoint.sh /tmp/
RUN chmod 555 /tmp/entrypoint.sh

COPY ozne ld-linux-x86-64.so.2 libc.so.6 flag.txt /var/service/
COPY flag.txt /tmp/

RUN chmod 444 /tmp/flag.txt
RUN chmod 444 /var/service/flag.txt
RUN chmod 555 /var/service/ozne
RUN chmod 555 /var/service/ld-linux-x86-64.so.2
RUN chmod 555 /var/service/libc.so.6

USER ctf

ENTRYPOINT /tmp/entrypoint.sh 
