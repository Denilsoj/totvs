from psycopg2 import sql

from src.db.queries.ai_models.strategy import ContextClassifier
from src.utils import check_column_exists


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

        self.classifier.model.initialize()

        descricao_comp_column_exists = check_column_exists(
            cursor, self.schema_name, self.table_name, "descricao_comp"
        )

        columns = ["id", "objeto", "descricao"]
        if descricao_comp_column_exists:
            columns.append("descricao_comp")

        query = sql.SQL(
            """
            SELECT {column_names} FROM {schema_name}.{table_name}
            WHERE classificado = false AND fase = 0
            ORDER BY id;
            """
        ).format(
            schema_name=sql.Identifier(self.schema_name),
            table_name=sql.Identifier(self.table_name),
            column_names=sql.SQL(",").join(map(sql.Identifier, columns)),
        )
        cursor.execute(query)
        rows = cursor.fetchall()

        for row in rows:
            print(f"- Classifying row {row['id']}")

            approved = self.classifier.execute(
                row["objeto"], row["descricao"], row.get("descricao_comp")
            )
            if approved:
                continue

            try:
                update_query = sql.SQL(
                    "UPDATE {schema_name}.{table_name} SET classificado = true, fase = {fase} WHERE id = {id};"
                ).format(
                    schema_name=sql.Identifier(self.schema_name),
                    table_name=sql.Identifier(self.table_name),
                    fase=sql.Literal(4),
                    id=sql.Literal(row["id"]),
                )
                cursor.execute(update_query)
                cursor.connection.commit()
                print(cursor.statusmessage)
            except Exception as e:
                print(f"Erro ao tentar classificar on row {row['id']} (IA): {e}")
                cursor.connection.rollback()
                exit(1)

        cursor.execute(
            count_query.format(
                schema_name=sql.Identifier(self.schema_name),
                table_name=sql.Identifier(self.table_name),
            )
        )
        total_rows = cursor.fetchone()["count"]
