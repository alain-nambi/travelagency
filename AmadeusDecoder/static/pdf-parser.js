const fs = require('fs').promises;
const PDFParser = require('pdf-parse');

// Fonction asynchrone pour convertir un fichier PDF en texte
async function pdfToText(pdfPath) {
  try {
    const dataBuffer = await fs.readFile(pdfPath);
    const data = await PDFParser(dataBuffer);
    return data.text;
  } catch (error) {
    throw error;
  }
}

function separateTextPerLine(text) {
  return text.split("\n");
}

function extractZenithPNRNumber(dataArray) {
  const startIndex = dataArray.indexOf('PNR Number/Numéro de dossierDate');

  if (startIndex !== -1) {
    const findPnrNumber = dataArray[startIndex + 2]
    if (findPnrNumber.length === 6 && String(findPnrNumber).startsWith("00")) {
      return {pnrNumber : findPnrNumber}
    }
  }
}

function extractTicketNumber(dataArray) {
  const startIndex = dataArray.findIndex((data) => data.startsWith("https://"))
  if (startIndex !== -1) {
    return dataArray[startIndex]
  }
}

async function main() {
  const pdfPath = "C:/Users/alain/Downloads/Ingénieur logiciel (3).pdf";

  try {
    console.time("Testing performance of separateTextPerLine function");

    const text = await pdfToText(pdfPath);
    const listOfSeparatedLines = separateTextPerLine(text);

    // console.log(listOfSeparatedLines.filter(list => list.trim() !== ""));

    console.log(extractTicketNumber(listOfSeparatedLines));

    const result = extractZenithPNRNumber(listOfSeparatedLines);

    if (result) {
      console.log(result);
    } else {
      console.log("> PNR Number not found.");
    }

    console.timeEnd("Testing performance of separateTextPerLine function");
  } catch (error) {
    console.error(error);
  }
}

main();
