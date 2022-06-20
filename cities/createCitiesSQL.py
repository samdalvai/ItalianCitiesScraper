import json
import os
# coding: latin1

def run():
    
    print("Creating cities sql...")

    try: 
        os.mkdir('sql/') 
    except OSError as error: 
        print("Directory sql/ already present")

    # create sql for cities
    with open('json/cities.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        out = open('sql/city.sql', 'w', encoding='utf-8')
        out.write("BEGIN;" + "\n\n")
        out.write("INSERT INTO City VALUES" + "\n\n")

        index = 0

        for p in data['cities']:
            # SKIP CITIES WITH NULL CAP AND PROVINCE
            if p['cap'] != "NULL" and p['province'] != "NULL":  
                name = p['name'].replace("'","''").replace("à","a").replace("ò","o").replace("è","e").replace("ù","u").replace("ì","i").replace("a''","a").replace("o''","o").replace("e''","e").replace("u''","u").replace("i''","i")

                out.write("(")
                out.write("'" + p['cap'] + "'" + ",")
                out.write("'" + name + "'" + ",")
                out.write("'" + p['province'] + "'" +  ",")
                if p['altitude'] == -1:
                    out.write(str(0))
                else:
                    out.write(str(p['altitude']))

                index += 1

                if index < len(data['cities']):
                    out.write(")," + "\n")
                else:
                    out.write(");" + "\n\n")

    out.write("END;")
    print(out.name + " created")
    out.close