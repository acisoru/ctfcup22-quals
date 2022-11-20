#!/bin/bash

mkdir web-legacy

cp -r ../deploy/* web-legacy/

cp env.env web-legacy/env.env

zip -r "web-legacy.zip" web-legacy

rm -rf web-legacy

mv web-legacy.zip ../public/