import csv 
from src.db.config import ConfigDB
from psycopg2 import errors
from psycopg2 import sql
import datetime

config = ConfigDB()




def copy_table():
    query = "CREATE TABLE propostas"




def insert_data_table(schema,table_name, **d):
   
    
    with config.connection:
        cur = config.cursor
        try:
                query = sql.SQL(
                     """
                INSERT INTO {schema}.{table_name} (
                    item_id, data, orgao, uf, objeto,
                    cnpj, razao_social, marca, modelo, fabricante,
                    unidade_de_medida, modalidade, valor_total, valor_unitario, base,
                    descricao, termo
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s
                )
                """
                ).format(
                    schema=sql.Identifier(schema),
                    table_name=sql.Identifier(table_name)
                )
                
                cur.execute(query, (
                        str(d['id']), datetime.datetime.strptime(d['data'], r'%d/%m/%Y'), d['entidade'], d['uf'], d['objeto'],
                        d['cnpj'], d['razao_social'], d['marca'], d['modelo'], d['fabricante'],
                        d['unidade_de_medida'], d['modalidade'], round(float(d['valor_total'].replace('.', '').replace(',', '.').strip()), 4) if len(d['valor_total']) != 0 else float(d['valor_total'].replace('.', '').replace(',', '.').strip()) * int(d['quantidade']),round(float(d['valor_unitario'].replace('.', '').replace(',', '.').strip()), 4) if len(d['valor_unitario']) != 0 else float(d['valor_total'].replace('.', '').replace(',', '.').strip()) / int(d['quantidade']), d['base'],
                        d['descricao'], d['termo'], d['quantidade']
                    ))
                print(f"{cur.statusmessage} item {d['id']}")
                config.connection.commit()
               
        except errors.Error as e:
            
            print('error ao adiconar', e)


with open('/home/denilson/Documents/promaxima/entrega_totvs/totvs/src/db/utils/entrega_sistemaS.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter=',')
    index = 0
    data_dump = []
    data_formated = []
    print
    
    for row in csv_reader:
        # if row['valor_total'] == '' or row['valor_unitario'] == '':
        #     continue
        
        insert_data_table('final','dados_limpos_com_sistema_s', **row)





     

