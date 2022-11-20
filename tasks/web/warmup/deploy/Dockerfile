FROM golang:1.16-buster

COPY src /src

WORKDIR /src

RUN go build . 

CMD ./passwordkv

