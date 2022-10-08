// This file will scrape program data of 
// camp type - day&night according to url of urls.json

// puppeteer-extra is a drop-in replacement for puppeteer,
// it augments the installed puppeteer with plugin functionality
const puppeteer = require('puppeteer-extra')

// add stealth plugin and use defaults (all evasion techniques)
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

// file helper
const fs = require('fs');
const csvWriter = require('csv-write-stream')
const finalPathFile = './football.csv';
// import config
const jsonData = require("./urls.json")
// csv fuc
async function writeToCSV(siteName, team1, team2, result1, result2, resultX) {
  if (!fs.existsSync(finalPathFile))
    writer = csvWriter({
      headers: ["site", "team1", "team2", "result1", "resultX", "result2", "time"]
    });
  else
    writer = csvWriter({
      sendHeaders: false
    });

  writer.pipe(fs.createWriteStream(finalPathFile, {
    flags: 'a'
  }));

  writer.write({
    site: siteName,
    team1: team1,
    team2: team2,
    result1: result1,
    resultX: resultX,
    result2: result2,
    time: formatDate(new Date()),
  });

  writer.end();
  return new Promise(resolve => {
    setTimeout(() => {
      resolve('resolved');
    }, 100);
  });
}
// time formating
function formatDate(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var seconds = date.getSeconds();
  var years = date.getFullYear();
  var months = date.getMonth() + 1;
  var days = date.getDate();
  if (months < 10) months = '0' + months;
  if (days < 10) days = '0' + days;
  if (hours < 10) hours = '0' + hours;
  if (minutes < 10) minutes = '0' + minutes;
  if (seconds < 10) seconds = '0' + seconds;
  var strTime = years + '' + months + '' + days + '' + hours + '' + minutes + '' + seconds;
  return strTime;
}
// wait
function delay(time) {
  return new Promise(function (resolve) {
    setTimeout(resolve, time)
  });
}
process.on('unhandledRejection', error => {
  console.log('error..')
  // browser.close();
  console.log('please try again a few minutes later..')
});
// puppeteer usage as normal
puppeteer.launch({
  headless: true,
  args: ['--disable-dev-shm-usage', '--unhandled-rejections=strict']
}).then(async browser => {

  process.on('unhandledRejection', error => {
    browser.close();
  });
  for (const [site, links] of Object.entries(jsonData)) {
    console.log('site:', site);
    console.log('links:', links);
    // for (let key in links) {

    // const url = links[key];
    // console.log('url', url);
    if (site != 'bwin') continue;

    const page = await browser.newPage()
    // Configure the navigation timeout
    await page.setDefaultNavigationTimeout(0);
    await page.goto(links);
    console.log('goto url')

    if (site == 'unibet') {
      try {
        let cols = await page.$x("//div[@class='fa117']");
        console.log('in cols', cols.length)
        for (let col in cols) {

          let teams = await cols[col].$x("//div[@class='af24c']");
          for (let team in teams) {
            let teamname = await (await teams[team].getProperty('innerText')).jsonValue();
            console.log(teamname)
          }
        }

        await page.close();
      } catch (error) {
        console.log(error, 'unibet')
        continue;
      }
    } else if (site == 'bwin') {
      console.log('in bwin')
      let bwinTeam = [];
      let bwinX12 = [];
      try {
        await delay(2000);
        let cols = await page.$x("//div[@class='grid-event-wrapper']");
        await delay(2000);

        for (let col in cols) {
          if (col > 0) continue;
          let teams = await cols[col].$x("//div[@class='participant-container']");
          for (let team in teams) {
            let teamname = await (await teams[team].getProperty('innerText')).jsonValue();
            bwinTeam.push(teamname);
          }

          let x12s = await cols[col].$x("//div[@class='option-indicator']");
          for (let x12 in x12s) {
            let res = await (await x12s[x12].getProperty('innerText')).jsonValue();
            bwinX12.push(res);
          }
        }
        console.log(bwinTeam)
        console.log(bwinX12)
        await page.close();
        console.log('page close')
        // write into csv
        for (let i = 0; i < bwinTeam.length / 2; i++) {
          team1 = bwinTeam[i * 2];
          team2 = bwinTeam[i * 2 + 1];
          result1 = bwinX12[i * 3];
          resultX = bwinX12[i * 3 + 1];
          result2 = bwinX12[i * 3 + 2];
          let res = await writeToCSV("bwin", team1, team2, result1, result2, resultX);

        }
      } catch (error) {
        console.log(error, 'bwin')
      }
    } else if (site == 'toto') {
      let totoTeam = [];
      let totoX12 = [];
      try {
        const liElm = await page.$x("//div[@class='event-list__item__content']");
        console.log(liElm.length)
        await page.close();

        // write into csv
        // for (let i = 0; i < totoTeam.length / 2; i++) {
        //   team1 = totoTeam[i * 2];
        //   team2 = totoTeam[i * 2 + 1];
        //   result1 = totoX12[i * 3];
        //   resultX = totoX12[i * 3 + 1];
        //   result2 = totoX12[i * 3 + 2];

        //   let res = await writeToCSV("toto", team1, team2, result1, result2, resultX);
        //   console.log(res, i)
        // }
      } catch (error) {
        console.log(error, 'toto')
      }
    } else {
      console.log('not in urls')
    }
    // }
  }

  // await page.waitForTimeout(5000)
  await browser.close()
  console.log(`All done, Move to next. ✨`)
})