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
    gcc-multilib \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -M -s /bin/false ctf
RUN mkdir /tmp/nsjail && cd /tmp/nsjail && git clone https://github.com/google/nsjail && cd nsjail && make && mv nsjail /bin && rm -rf -- /nsjail

COPY entrypoint.sh /tmp/
RUN chmod 555 /tmp/entrypoint.sh

COPY libc.so.6 ld-linux.so.2 shellyha flag.txt /var/service/

RUN chmod 555 /var/service/libc.so.6
RUN chmod 555 /var/service/ld-linux.so.2
RUN chmod 444 /var/service/flag.txt
RUN chmod 555 /var/service/shellyha
USER ctf

ENTRYPOINT /tmp/entrypoint.sh 