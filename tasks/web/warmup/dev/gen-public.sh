#!/bin/bash

mkdir web-warmup

cp -r ../deploy/* web-warmup/

echo "CUP{example}" > web-warmup/conf/db_password

zip -r "web-warmup.zip" web-warmup

rm -rf web-warmup

mv web-warmup.zip ../public/