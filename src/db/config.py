import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()


class ConfigDB:

    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("NAME_DB"),
            user=os.getenv("USER_DB"),
            password=os.getenv("PASSWORD_DB"),
            host=os.getenv("HOST_DB"),
            port=os.getenv("PORT_DB"),
        )

        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def duplicate_table(self, schema, table_name, dump_table):

        try:
            queries = [
                f'CREATE TABLE IF NOT EXISTS "{schema}"."{table_name}" AS SELECT * FROM "{schema}"."{dump_table}"',
                f'UPDATE "{schema}"."{table_name}" SET classificado = false, fase = 0',
                f"UPDATE \"{schema}\".\"{table_name}\" SET modalidade = 'Outras modalidades' WHERE modalidade = '0'",
                f"UPDATE \"{schema}\".\"{table_name}\" SET modalidade = 'Pregão eletrônico' WHERE modalidade = '5'",
                f"UPDATE \"{schema}\".\"{table_name}\" SET modalidade = 'Dispensa de licitação' WHERE modalidade = '19'",
                f"UPDATE \"{schema}\".\"{table_name}\" SET modalidade = 'Pregão presencial' WHERE modalidade = '6'",
                f"UPDATE \"{schema}\".\"{table_name}\" SET modalidade = 'Inexigibilidade' WHERE modalidade = '28'",
            ]

            for query in queries:
                self.cursor.execute(query)

                self.connection.commit()
                print(self.cursor.statusmessage)

        except Exception as e:
            print(e)

    def __del__(self):
        self.cursor.close()
        self.connection.close()
