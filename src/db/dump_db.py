import csv 
from config import create_table, insert_data_table 





with open('totvs_itens_full.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    index = 0
    data_dump = []
    data_formated = []
    
    for row in csv_reader:
             insert_data_table('20_12_2024','dados_nao_tratados', **row)

   