from bs4 import BeautifulSoup
import requests
import re
import time
import os
# coding: latin1


def get_zone(province):
    province = province.strip()

    if province in ("Aosta","Belluno","Bergamo","Biella","Bolzano","Brescia","Como","Cuneo","Lecco","Pordenone","Sondrio","Torino","Trento","Udine","Verbania","Vercelli","Vicenza","Verbano-Cusio-Ossola"):
        return "I-A"
    elif province in ("Alessandria","Ancona","Asti","Bologna","Cremona","Forlì-Cesena","Lodi","Milano","Modena","Monza e Brianza","Novara","Parma","Pavia","Pesaro e Urbino","Piacenza","Ravenna","Reggio Emilia","Rimini","Treviso","Varese","Modena"):
        return "I-M"
    elif province in ("Arezzo","Ascoli Piceno","Bari","Campobasso","Chieti","Ferrara","Firenze","Fermo","Foggia","Genova","Gorizia","Imperia","Isernia","La Spezia","Lucca","Macerata","Mantova","Massa-Carrara","Padova","Perugia","Pescara","Pistoia","Prato","Rovigo","Savona","Teramo","Trieste","Venezia","Verona","Barletta-Andria-Trani"):
        return "II"
    elif province in ("Agrigento","Avellino","Benevento","Brindisi","Cagliari","Caltanisetta","Sud Sardegna","Carbonia-Iglesias","Caltanissetta","Caserta","Catania","Catanzaro","Cosenza","Crotone","Enna","Frosinone","Grosseto","L'Aquila","Latina","Lecce","Livorno","Matera","Medio Campidano","Messina","Napoli","Nuoro","Ogliastra","Olbia Tempio","Oristano","Palermo","Pisa","Potenza","Ragusa","Reggio Calabria","Rieti","Roma","Salerno","Sassari","Siena","Siracusa","Taranto","Terni","Trapani","Vibo Valentia","Viterbo"):
        return "III"
    else:
        return ""

def get_load(zone):
    if zone == "I-A":
        return 1.5
    elif zone == "I-M":
        return 1.5
    if zone == "II":
        return 1
    if zone == "III":
        return 0.6
    else:
        return -1

def run():

    print("Scraping provinces data...")

    page = requests.get("https://it.wikipedia.org/wiki/Province_d%27Italia")
    soup = BeautifulSoup(page.content, 'html.parser')
    #print (soup.prettify())

    items = soup.find_all("table")

    try: 
        os.mkdir('json/') 
    except OSError as error: 
        print("Directory json/ already present")   

    out = open('json/provinces.json', 'w', encoding='utf-8')
    out.write('{' + "\n" + "\t" + "\"provinces\": [" + "\n")

    rows = items[1].find_all('tr')

    for x in range(1,len(rows)):
        province = rows[x].find_all('td')

        name = province[0].get_text()
        name = re.sub("[[0-9]+]", "", name)
        match = re.search(r'^[A-Z]', name)
        if not match:
            name = name[1:(len(name) - 1)]


        shorthand = province[1].get_text()

        region = province[2].get_text()
        region = region[1:(len(region) - 1)]

        print ("name: " + name + " shorthand: " + shorthand + " region: " + region)

        out.write("\t" + "{" + "\n")

        out.write("\t\t" + "\"name\": " + "\"" + name.replace("\n","") + "\"" + "," + "\n")
        out.write("\t\t" + "\"shorthand\": " + "\"" + shorthand.replace("\n","") + "\"" + ","+ "\n")
        out.write("\t\t" + "\"region\": " + "\"" + region.replace("\n","") + "\"" + ","+ "\n")
        out.write("\t\t" + "\"climatic-zone\": " + "\"" + get_zone(name) + "\"" + "," + "\n")
        out.write("\t\t" + "\"base-load\": " + str(get_load(get_zone(name))) + "\n")

        if x == len(rows) - 1:
            out.write("\t}" + "\n")
        else:
            out.write("\t}," + "\n")

    out.write("\t" + "]" + "\n")
    out.write("}")
    out.close


run()