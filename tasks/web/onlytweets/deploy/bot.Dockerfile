FROM node:19-buster

RUN apt-get update \
    && apt-get install -y wget gnupg fonts-ipafont-gothic fonts-freefont-ttf firefox-esr --no-install-recommends

COPY admin_bot .

RUN PUPPETEER_PRODUCT=firefox npm install

CMD ["node", "index.js"]
