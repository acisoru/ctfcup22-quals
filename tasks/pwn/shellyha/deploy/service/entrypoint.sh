#!/bin/sh

nsjail \
    --mode l \
    --port 31337 \
    --time_limit 30 \
    --disable_proc \
    --bindmount_ro /bin/ \
    --bindmount_ro /usr/bin/ \
    --bindmount_ro /lib \
    --bindmount_ro /lib32 \
    --bindmount_ro /lib64 \
    --bindmount_ro /usr/lib \
    --bindmount_ro /dev/null \
    --bindmount_ro /dev/urandom \
    --bindmount_ro /etc/passwd \
    --bindmount_ro /etc/group \
    --bindmount_ro /var/service/ \
    --cwd /var/service/ \
    --hostname ctf \
    --max_cpus 1 \
    --stderr_to_null \
    -- \
    ./shellyha