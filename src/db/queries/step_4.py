import os

from dotenv import load_dotenv
import google.generativeai as genai
from psycopg2 import sql

from db.queries.ai_models.strategy import ContextClassifier


load_dotenv()

genai.configure(api_key=os.environ.get("GOOGLE_GENERATIVEAI_API_KEY", ""))


class ClassifyContextWithAI:
    def __init__(self, schema_name, table_name, ai_model):
        self.schema_name = schema_name
        self.table_name = table_name

        self.classifier = ContextClassifier(ai_model)

    def execute(self, cursor):
        count_query = sql.SQL(
            "SELECT count(id) FROM {schema_name}.{table_name} WHERE classificado = false AND fase = 0;"
        )
        cursor.execute(
            count_query.format(
                schema_name=sql.Identifier(self.schema_name),
                table_name=sql.Identifier(self.table_name),
            )
        )
        total_rows = cursor.fetchone()["count"]
        print(f"Total rows to classify: {total_rows}")

        for offset in range(0, total_rows, 100):
            query = sql.SQL(
                """
                SELECT * FROM {schema_name}.{table_name}
                WHERE classificado = false AND fase = 0
                ORDER BY id LIMIT 100 OFFSET {offset};
                """
            ).format(
                schema_name=sql.Identifier(self.schema_name),
                table_name=sql.Identifier(self.table_name),
                offset=sql.Literal(offset),
            )
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                print(f"- Classifying row {row['id']}")

                fase = (
                    5 if self.classifier.execute(row["objeto"], row["descricao"]) else 4
                )

                try:
                    update_query = sql.SQL(
                        "UPDATE {schema_name}.{table_name} SET classificado = true, fase = {fase} WHERE id = {id};"
                    ).format(
                        schema_name=sql.Identifier(self.schema_name),
                        table_name=sql.Identifier(self.table_name),
                        fase=sql.Literal(fase),
                        id=sql.Literal(row["id"]),
                    )
                    cursor.execute(update_query)
                    cursor.connection.commit()
                    print(cursor.statusmessage)
                except Exception as e:
                    print(f"Erro ao tentar classificar on row {row['id']} (IA): {e}")
                    cursor.connection.rollback()
                    exit(1)
