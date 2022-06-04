# ItalianCitiesScraper
A simple python tool to gather data on Italian cities and create an xml file. The data gathered is of interest to performing snow load computations, for example the altitude, the province and the climatic zones are parsed. The data is scraped from the Wikipedia.

## Requirements

* You need to have `Python` installed on your machine.

## How to run

* Run `python provinces/provincesScripts.py`
* Run `python cities/citiesScripts.py`
* The scripts will first create a json file with all the required data, and then convert it into an xlsx file which can be used with an arbitraty xlsx editor, like Microsoft Excel.
