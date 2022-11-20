FROM golang:1.18-alpine AS build_base

RUN apk add --no-cache git

# Set the Current Working Directory inside the container
WORKDIR /tmp/gpb_math_pong

# We want to populate the module cache based on the go.{mod,sum} files.
COPY go.mod .
COPY go.sum .

RUN go mod download

COPY . .

# Build the Go app
RUN go build -o ./out/main .

# Start fresh from a smaller image
FROM alpine

ENV GPB_MATH_PONG_PORT ":8181"
ENV GPB_MATH_PONG_FLAG_PRICE "1000"
ENV GPB_MATH_PONG_FLAG "CUP{GPBctfOneLove_____}"

RUN apk add ca-certificates

COPY --from=build_base /tmp/gpb_math_pong/out/main /app/main

# This container exposes port 8080 to the outside world
EXPOSE 8181

# Run the binary program produced by `go install`
CMD ["/app/main"]
