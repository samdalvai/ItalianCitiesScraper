import xlsxwriter
import json
from decimal import Decimal
import os

def run():

    print("Creating provinces xlsx...")
    
    try: 
        os.mkdir('xlsx/') 
    except OSError as error: 
        print("Directory xlsx/ already present") 

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('xlsx/provinces.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '#.##'})


    worksheet.write(row,col,'Sigla',bold)
    worksheet.write(row,col+1,'Nome',bold)
    worksheet.write(row,col+2,'Regione',bold)
    worksheet.write(row,col+3,'Zona Climatica',bold)
    worksheet.write(row,col+3,'Carico base',bold)

    row += 1

        # {
        # 	"name": "Terni",
        # 	"shorthand": "TR",
        # 	"region": "Umbria",
        # 	"climatic-zone": "III",
        # 	"base-load": 0.6
        # },

    with open('json/provinces.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for p in data['provinces']:
            worksheet.write(row,col,p['shorthand'])
            worksheet.write(row,col+1,p['name'])
            worksheet.write(row,col+2,p['region'])
            worksheet.write(row,col+2,p['climatic-zone'])
            worksheet.write_number(row,col+3,p['base-load'])

            row += 1

    workbook.close()