# Purpose

This is result of the challenge presented at https://at.boc-group.com/wad/challenge/advanced/

# Application

The base application was built using Python (Flask). The used files are:

* main.py —> contains all the api calls to fetch the information and all the classes to aggregate the returned information

* /templates/base.html —> contains the main html structure

* /templates/index.html -> contains all the html and javascript code to present the map, the location pins and the tables with the information

* /static/css/myStyles.css —> contains all the styling for the webpage

## Application functioning

* Upon the first access to the endpoint, all the information regarding the Applications, Servers and locations are fetched and displayed. 

* The map goes directly to Portugal and points to Unbabel (Portuguese startup)

* When a detail button is pressed, the server gets the details of the specified “object” and presents the results in a popup window.

* In case the asked details refer to a location, not only the popup shows up, but also the map gets re-centered and the pin will point to the specified location