import puppeteer from "puppeteer";

const [, , outputPdfPath] = process.argv;

if (!outputPdfPath) {
  console.error("Usage: node exportToPDF.js <outputPdfPath>");
  process.exit(1);
}

const browser = await puppeteer.launch();
const page = await browser.newPage();

await page.goto("http://localhost:5173", { waitUntil: "networkidle0" });

await page.pdf({
  path: outputPdfPath,
  format: "A4",
  printBackground: true,
  pageRanges: "2",
});

console.log(`PDF exported as ${outputPdfPath}`);
await browser.close();
