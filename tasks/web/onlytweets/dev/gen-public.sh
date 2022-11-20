#!/bin/bash

mkdir web-onlytweets

cp -r ../deploy/* web-onlytweets/

cp config.env web-onlytweets/config.env

zip -r "web-onlytweets.zip" web-onlytweets

rm -rf web-onlytweets

mv web-onlytweets.zip ../public/