# Flask-Api-Python-web-Scrapping

This code is a Flask application, which is a Python framework for creating web applications. The application has a single route, which is the main '/' route. When a POST request is made to this route, the function xd() is executed.

The application() function does the following:

1-. Initializes an empty dictionary called "company", which will be used to store information about a given company.

2-. Declares a list called "iterator" that contains a series of information elements that will be searched for about the company.

3-. Gets the name of the company from the HTML form and uses it to make a request to Yahoo Finance to get information about the company.

4-. Uses Beautiful Soup, a Python library for parsing and extracting data from HTML and XML, to process the request response and extract information about the company.

5-. Stores the extracted information in the "company" dictionary.

6-. Returns the information about the company to the user's web browser.

# EXAMPLE

https://user-images.githubusercontent.com/104428151/208218857-bbac2567-4a3d-4c39-859f-9096ebb18b1b.mp4
