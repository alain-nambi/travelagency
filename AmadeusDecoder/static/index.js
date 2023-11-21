const axios = require("axios");
const express = require("express");
const cheerio = require("cheerio");
const { v4 } = require("uuid");

// Create an instance of the express application
const app = express();

// Define the URL for the job portal
const portalJobUrl = "https://www.portaljob-madagascar.com/emploi/liste/secteur/informatique-web/page/";

// Function to scrape job listings from the portal
const scrapeJobListings = async (portalJobUrl) => {
  try {
    // Make a GET request to the job portal URL
    const response = await axios.get(portalJobUrl);

    if (response.data) {
      // Parse the HTML content using Cheerio
      const $ = cheerio.load(response.data);

      // Initialize an array to store job listings
      const jobListings = [];

      const pageList = $(".pagination").find("ul").find("li").last().text()

      $(".item_annonce").each((_index, annonce) => {
        // Extract job details
        const title = $(annonce).find(".contenu_annonce > h3 > a > strong").text();
        const company = $(annonce).find(".contenu_annonce > h4").text();
        const contractType = $(annonce).find(".contenu_annonce > h5").text();

        // Check if all required details are available
        if (title && company && contractType) {
          jobListings.push({
            uuid: v4(),
            title: title,
            company: company,
            contractType: contractType,
          });
        }
      });

      return { jobListings, pageList } ;
    }
  } catch (error) {
    throw error;
  }
};

const getPageList = async () => {
    const { pageList } = await scrapeJobListings(portalJobUrl)
    return pageList;
}


// Route to get and display job listings
app.get("/job-listings", async (req, res) => {
  try {
    const jobListings = await scrapeJobListings(portalJobUrl);
    res.json(jobListings);
  } catch (error) {
    res.status(500).json({
      error: "An error occurred while scraping job listings",
      message: error.message,
    });
  }
});

// Run the application on port 5000
app.listen("5000", () => console.log("App running on port 5000"));
