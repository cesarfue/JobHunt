import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";

const [, , outputPdfPath] = process.argv;

if (!outputPdfPath) {
  console.error("Usage: node exportToPDF.js <outputPdfPath>");
  process.exit(1);
}

// Expand ~ to home directory if present
const expandedPath = outputPdfPath.startsWith("~")
  ? path.join(process.env.HOME, outputPdfPath.slice(1))
  : outputPdfPath;

// Check if file exists and remove it to ensure overwrite
if (fs.existsSync(expandedPath)) {
  console.log(`Removing existing file: ${expandedPath}`);
  fs.unlinkSync(expandedPath);
}

console.log("Launching browser...");
const browser = await puppeteer.launch();
const page = await browser.newPage();

console.log("Loading page from http://localhost:5173...");
await page.goto("http://localhost:5173", { waitUntil: "networkidle0" });

console.log("Generating PDF...");
await page.pdf({
  path: expandedPath,
  format: "A4",
  printBackground: true,
  pageRanges: "2",
});

console.log(`✓ PDF exported successfully: ${expandedPath}`);
await browser.close();
