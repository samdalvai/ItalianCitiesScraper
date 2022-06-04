from bs4 import BeautifulSoup
import requests
import re
import time
import os

# return content of type specified for a search parameter
def scrapeWikiPage(searchParam,elementType,index):
    search = searchParam.replace("\n","")

    url = ("https://it.wikipedia.org/wiki/" + search)

    print("Scraping: " + url)

    # query website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # find all elements of table and return
    try:
        nodes = soup.find_all(elementType)[index].getText()
        return nodes
    except IndexError as error:
        return ""

# return content of type specified for a search parameter
def scrapeWikiPageEN(searchParam,elementType):
    # replace whitespaces with underscore
    search = searchParam.replace(" ","_")

    url = ("https://en.wikipedia.org/wiki/" + search).replace("\n","")

    print("Scraping: " + url)

    # query website
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # find all elements of table and return
    try:
        nodes = soup.find_all(elementType)[0].getText()
        return nodes
    except IndexError as error:
        return ""

# extract string corresponding to regex from text
def extractRegexFromText(text,regex,default):
    match = re.search(regex, text)
    if match:
        string = match.group()
        #print(string)
    else:
        #print("not found")
        string = default ## default value in case not found
    return string

# format the string representing the municipality according to Wikipedia standards
def formatMunicipalities():
    municipalities = open ("comuni.txt", "r", encoding='utf-8')
    out = open("comuniFormatted.txt","w",encoding='utf-8')

    cities = municipalities.readlines()

    cities.sort()

    for x in range(0,len(cities)):
        output = cities[x].replace(" ","_").replace("\n","")
        if x < len(cities) - 1:
            out.write(output + "\n")
        else:
            out.write(output)
    
    out.close

def run():

    print("Scraping cities data...")

    try: 
        os.mkdir('json/') 
    except OSError as error: 
        print("Directory json/ already present") 

    formatMunicipalities()

    # get all the names of municipalities (open file with right encoding)
    municipalities = open ("comuniFormatted.txt", "r", encoding='utf-8')

    cities = municipalities.readlines()

    out = open('json/cities.json', 'w', encoding='utf-8')
    out.write('{' + "\n" + "\t" + "\"cities\": [" + "\n")
    out.close

    for x in range(0,len(cities)):

        nodes = scrapeWikiPage(cities[x],'table',0)
        if "Altitudine" not in nodes and "Targa" not in nodes:
            nodes = scrapeWikiPage(cities[x],'table',1)
            if "Altitudine" not in nodes and "Targa" not in nodes:
                nodes = scrapeWikiPage(cities[x],'table',2)
                if "Altitudine" not in nodes and "Targa" not in nodes:
                    nodes = scrapeWikiPage((cities[x] + "_(Italia)"),'table',0)
                    if "Altitudine" not in nodes and "Targa" not in nodes:
                        nodes = scrapeWikiPage((cities[x] + "_(Italia)"),'table',1)
                        if "Altitudine" not in nodes and "Targa" not in nodes:
                                nodes = scrapeWikiPage((cities[x] + "_(Italia)"),'table',2)
                                if "Altitudine" not in nodes and "Targa" not in nodes:
                                    nodes = scrapeWikiPage((cities[x] + "_(comune)"),'table',0)
                                    if "Altitudine" not in nodes and "Targa" not in nodes:
                                        print("Nothing found for: " + cities[x].replace("\n",""))

        # find elevation in elements
        altitudeRaw = extractRegexFromText(nodes,r'Altitudine[0-9]+\s?([0-9]+)?',"")
        capRaw = extractRegexFromText(nodes,r'postale[0-9]{5}',"")
        if capRaw == "":
            capRaw = extractRegexFromText(nodes,r'postaleda [0-9]{5}',"")

        provinceRaw = extractRegexFromText(nodes,r'Targa[A-Z][A-Z]',"")

        # extract altitude
        altitude = re.sub("[^0-9]", "", altitudeRaw)

        # extract CAP (postal code)
        cap = re.sub("[^0-9]", "", capRaw)

        # extract province
        province = provinceRaw.replace("Targa","")

        # if some information is missing, try with english wikipedia
        if altitude == "" or cap == "" or province == "":
            print("searching enlish wiki for: " + cities[x].replace("\n",""))
            englishNodes = scrapeWikiPageEN(cities[x],'tbody')

        if altitude == "":
            altitudeRaw = extractRegexFromText(englishNodes,r'Elevation[0-9]+(,)?([0-9]+)?',"")
            altitude = re.sub("[^0-9]", "", altitudeRaw)
            if altitude == "":
                altitudeRaw = extractRegexFromText(englishNodes,r'elevation[0-9]+(,)?([0-9]+)?',"")
                altitude = re.sub("[^0-9]", "", altitudeRaw)

        if cap == "":
            capRaw = extractRegexFromText(englishNodes,r'Postal code[0-9]{5}',"")
            cap = re.sub("[^0-9]", "", capRaw)
        
        if province == "":
            provinceRaw = extractRegexFromText(englishNodes,r'(()[A-Z][A-Z]())',"")
            province = provinceRaw.replace("(","").replace(")","")

        if altitude != "" and cap != "" and province != "": 
            # write to file
            out = open('json/cities.json', 'a', encoding='utf-8')
            out.write("\t" + "{" + "\n")

            out.write("\t\t" + "\"name\": " + "\"" + cities[x].replace("\n","").replace("_"," ") + "\"" + "," + "\n")
            out.write("\t\t" + "\"cap\": " + "\"" + cap + "\"" + "," + "\n")
            out.write("\t\t" + "\"province\": " + "\"" + province + "\"" + "," + "\n")
            if altitude != "NULL":
                out.write("\t\t" + "\"altitude\": " +  altitude + "\n")
            else:
                out.write("\t\t" + "\"altitude\": " + "\"" +  altitude + "\"" + "\n")

            if x < len(cities) - 1:
                out.write("\t}," + "\n")
            else:
                out.write("\t}" + "\n")

            out.close

            time.sleep(0.01)
        else:
            if altitude == "":
                print("missing altitude from: " + cities[x].replace("\n",""))
            if cap == "":
                print("missing cap from: " + cities[x].replace("\n",""))
            if province == "":
                print("missing province from: " + cities[x].replace("\n",""))

    municipalities.close()

    out = open('json/cities.json', 'a', encoding='utf-8')
    out.write("\t" + "]" + "\n")
    out.write("}")
    out.close
