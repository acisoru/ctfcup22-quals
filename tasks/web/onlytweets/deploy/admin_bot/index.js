const puppeteer = require('puppeteer');
const Deque = require("double-ended-queue");
const PromiseTimers = require("timers/promises");
const redis = require('redis');

const sleep = d => new Promise(r => setTimeout(r, d));

const REDIS_HOST = process.env.REDIS_HOST || 'redis';
const BOT_USER = process.env.ADMIN_LOGIN || "admin";
const BOT_PASS = process.env.ADMIN_PASSWORD || "12345";
const LOGIN_URL = process.env.LOGIN_URL || "http://localhost:5000/login";

async function visitUrl(browser, url) {
    const context = await browser.createIncognitoBrowserContext();
    let page = await context.newPage();
    console.log(LOGIN_URL, BOT_USER, BOT_PASS);
    console.log("opening new page");
    await Promise.all([
        page.goto(LOGIN_URL),
        page.waitForNavigation({waitUntil: 'load'}),
    ]);
    console.log("content loaded");
    await page.waitForSelector('#id_username');
    console.log('waited for selector');
    await page.$eval('#id_username', (el, val) => {
        el.value = val;
    }, BOT_USER);
    await page.$eval('#id_password', (el, val) => {
        el.value = val;
    }, BOT_PASS);
    // await page.type('#id_username', BOT_USER);
    // await page.type('#id_password', BOT_PASS);
    await page.click('#submitButton');
    console.log("clicked");

    await page.waitForSelector('#myTab');

    await page.goto(url);
    console.log('visited ' + url)
    await sleep(2000)
}

async function launchPup() {
    return await puppeteer.launch({
        product: 'firefox',
        headless: true
    });
}

(async function () {
    let redisUrl = `redis://${REDIS_HOST}:6379`
    const client = redis.createClient({
        url: redisUrl
    });

    client.on('error', (err) => console.log('Redis Client Error', err));

    let pup = await launchPup();

    for await (const startTime of PromiseTimers.setInterval(2500, Date.now())) {
        await client.connect();

        let queueEntry = await client.lPop('report-queue');
        if (queueEntry == null) {
            await client.disconnect();
            continue;
        }
        let data = JSON.parse(queueEntry);

        await visitUrl(pup, data.url)

        await client.set('reports:' + data.uid, 'true')

        await client.disconnect();
    }
}())