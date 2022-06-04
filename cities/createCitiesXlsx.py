import xlsxwriter
import json
from decimal import Decimal
import os

def run():

    print("Creating cities xlsx...")

    try: 
        os.mkdir('xlsx/') 
    except OSError as error: 
        print("Directory xlsx/ already present")

    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook('xlsx/cities.xlsx')
    worksheet = workbook.add_worksheet()

    # Start from the first cell. Rows and columns are zero indexed.
    row = 0
    col = 0

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    # Add a number format for cells with money.
    money = workbook.add_format({'num_format': '#.##'})


    worksheet.write(row,col,'CAP',bold)
    worksheet.write(row,col+1,'Nome',bold)
    worksheet.write(row,col+2,'Provincia',bold)
    worksheet.write(row,col+3,'Altitudine',bold)

    row += 1

        # {
        # 	"name": "Zungoli",
        # 	"cap": "83030",
        # 	"province": "AV",
        # 	"altitude": 657
        # },


    with open('json/cities.json', encoding='utf-8') as json_file:
        data = json.load(json_file)

        for p in data['cities']:
            worksheet.write(row,col,p['cap'])
            worksheet.write(row,col+1,p['name'])
            worksheet.write(row,col+2,p['province'])
            worksheet.write_number(row,col+3,p['altitude'])

            row += 1

    workbook.close()