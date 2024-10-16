Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

Project Overview
----------------
This project involves scraping data from the Redbus website using Selenium and creating a dynamic filtering system using Streamlit. The goal is to extract bus travel data, such as available routes, timings, prices, and operator details, and present this information in a user-friendly interface where users can filter and explore the data according to their preferences.

Objective
---------
The primary objectives of this project are:
- To scrape bus travel data from the Redbus website efficiently.
- To store the scraped data in a structured format for easy access and analysis.
- To create a Streamlit application that allows users to dynamically filter and explore the scraped data.

Data Description
----------------
The project focuses on extracting the following data points from the Redbus website:
- Bus Operator: The name of the bus service provider.
- Route: The starting and ending locations of the bus service.
- Departure and Arrival Times: Scheduled times for departure and arrival.
- Ticket Prices: The cost of tickets for the journey.
- Bus Type: Information about the type of bus (e.g., AC, Non-AC, Sleeper).

Tools and Technologies
----------------------
The project utilizes the following tools and technologies:
- Web Scraping: Selenium (for automating browser actions and extracting data)
- Data Storage: Pandas (for storing data in a structured format, e.g., CSV)
- Web Application: Streamlit (for creating an interactive data filtering interface)
- Programming Language: Python

Data Scraping
-------------
Steps Involved:
1. Set Up Selenium:
   - Configure Selenium WebDriver to interact with the Redbus website.
   - Use browser automation to navigate through the website and load the necessary data.

2. Data Extraction:
   - Extract key data points such as bus operator, route, timings, prices, and bus type.
   - Handle dynamic content loading by automating scrolling and clicks to reveal hidden data.

3. Data Storage:
   - Store the scraped data in a Pandas DataFrame.
   - Save the DataFrame to a CSV file for easy access and further analysis.

Streamlit Application
---------------------
Features:
- Dynamic Filtering: Users can filter bus travel data based on parameters such as route, operator, departure time, and price range.
- User-Friendly Interface: The application provides an easy-to-use interface for exploring the data.
- Real-Time Updates: As users adjust the filters, the displayed data updates in real-time.

Challenges and Solutions
------------------------
1. Web Scraping:
   - Challenge: Dynamic Content Loading
   - Solution: Use Selenium’s explicit waits and automate scrolling to ensure all data is captured.

2. Data Storage:
   - Challenge: Data Accuracy
   - Solution: Implement data validation checks before saving to ensure completeness and accuracy.

Conclusion
----------
This project successfully demonstrates how to scrape data from a dynamic website like Redbus and present it in an interactive format using Streamlit. The resulting application allows users to easily explore and filter bus travel options, providing a practical tool for analyzing bus travel data.
