import puppeteer from "puppeteer";

const browser = await puppeteer.launch();
const page = await browser.newPage();

await page.goto("http://localhost:5173", { waitUntil: "networkidle0" });

await page.pdf({
  path: "resume.pdf",
  format: "A4",
  printBackground: true,
  pageRanges: "2",
});

console.log("PDF exported as resume.pdf");
await browser.close();
