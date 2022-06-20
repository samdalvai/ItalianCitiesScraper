import json
import os

def run():

    print("Creating provinces sql...")

    try: 
        os.mkdir('sql/') 
    except OSError as error: 
        print("Directory sql/ already present")

    # create sql for provinces
    with open('json/provinces.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        out = open('sql/province.sql', 'w', encoding='utf-8')
        out.write("BEGIN;" + "\n\n")
        out.write("INSERT INTO Province VALUES" + "\n")

        index = 0

        for p in data['provinces']:
            name = p['name'].replace("'","''")  

            out.write("(")
            out.write("'" + p['shorthand'] + "'" + ",")
            out.write("'" + name + "'" + ",")
            out.write("'" + p['climatic-zone'] + "'" +  ",")
            out.write(str(p['base-load']))

            index += 1

            if index < len(data['provinces']):
                out.write(")," + "\n")
            else:
                    out.write(");" + "\n\n")

    out.write("END;")
    print(out.name + " created")
    out.close