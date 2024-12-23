import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import errors
from psycopg2 import sql
import os
from dotenv import load_dotenv

load_dotenv()


class ConfigDB:

    def __init__(self):
        self.con = psycopg2.connect(
            dbname = os.getenv('NAME_DB'), 
            user = os.getenv('USER_DB'), 
            password = os.getenv('PASSWORD_DB'),
            host = os.getenv('HOST_DB'),
            port = os.getenv('PORT_DB')
            
            )

        self.cursor = self.con.cursor(cursor_factory=RealDictCursor)

    @staticmethod
    def duplicate_table(schema, table_name, dump_table, connection, cursor):

        with connection:
            try:
                queries = [
                    f'CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}" AS SELECT * FROM "{schema}"."{dump_table}"',
                    f'UPDATE "{schema}"."{table_name}" SET classificacao = false',
                    f'UPDATE "{schema}"."{table_name}" SET modalidade = \'Outras modalidades\' WHERE modalidade = \'0\'',
                    f'UPDATE "{schema}"."{table_name}" SET modalidade = \'Pregão eletrônico\' WHERE modalidade = \'5\'',
                    f'UPDATE "{schema}"."{table_name}" SET modalidade = \'Dispensa de licitação\' WHERE modalidade = \'19\'',
                    f'UPDATE "{schema}"."{table_name}" SET modalidade = \'Pregão presencial\' WHERE modalidade = \'6\'',
                    f'UPDATE "{schema}"."{table_name}" SET modalidade = \'Inexigibilidade\' WHERE modalidade = \'28\''
                    ]



                for query in queries:
                    cursor.execute(query)
        

                    connection.commit()
                    print(cursor.statusmessage)

            except Exception as e:
                print(e)


           



    

# def create_table(schema:str ,table_name:str) -> str:
#     try:
#         create_table_query = sql.SQL("""
#         CREATE TABLE IF NOT EXISTS {schema}.{table_name} (
#             id SERIAL PRIMARY KEY,
#             item_id VARCHAR(50) UNIQUE,
#             data DATE,
#             orgao TEXT,
#             uf VARCHAR(2),
#             objeto TEXT,
#             cnpj VARCHAR(30),
#             razao_social TEXT,
#             marca TEXT,
#             modelo TEXT,
#             fabricante TEXT,
#             unidade_de_medida TEXT,
#             modalidade TEXT,
#             valor_total NUMERIC(32, 4),
#             valor_unitario NUMERIC(32, 4),
#             base TEXT,
#             descricao TEXT,
#             termo TEXT,
#             classificacao BOOL,
#             fase INT
#         )
#     """).format(
#         schema=sql.Identifier(schema),
#         table_name=sql.Identifier(table_name)
#     )


#         cur.execute(create_table_query)
        

#         print(cur.statusmessage)
#     except errors.Error as e:
#         print(f"Erro ao criar a tabela {table_name}", e)
#     finally:
#         con.commit()
#         cur.close()
#         con.close()

# def insert_data_table(schema,table_name, **d):
   
#     print(d)
#     with con:
#         cur = con.cursor()
#         try:
#                 query = sql.SQL(
#                      """
#                 INSERT INTO {schema}.{table_name} (
#                     item_id, data, orgao, uf, objeto,
#                     cnpj, razao_social, marca, modelo, fabricante,
#                     unidade_de_medida, modalidade, valor_total, valor_unitario, base,
#                     descricao, termo
#                 ) VALUES (
#                     %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
#                     %s, %s, %s, %s, %s, %s, %s
#                 )
#                 """
#                 ).format(
#                     schema=sql.Identifier(schema),
#                     table_name=sql.Identifier(table_name)
#                 )
            
#                 cur.execute(query, (
#                         str(d['item_id']), d['data'], d['orgao'], d['uf'], d['objeto'],
#                         d['cnpj'], d['razao_social'], d['marca'], d['modelo'], d['fabricante'],
#                         d['unidade_de_medida'], d['modalidade'], round(float(d['valor'].replace('.', '').replace(',', '.').strip()), 4) if len(d['valor']) != 0 else d['valor'],round(float(d['valor_unitario'].replace('.', '').replace(',', '.').strip()), 4) if len(d['valor_unitario']) != 0 else d['valor_unitario'], d['base'],
#                         d['descricao'], d['termo']
#                     ))
                
#                 con.commit()
               
#         except errors.Error as e:
            
#             print('error ao adiconar', e)
