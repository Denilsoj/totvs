from psycopg2 import errors, sql

from src.utils import check_column_exists


class UpdatedNegativeWords:
    query = sql.SQL(
        """
        UPDATE {schema_name}.{table_name} 
        SET classificado = true, fase = 1 
        WHERE {conditions};
        """
    )

    def __init__(self, schema_name, table_name):
        self.schema_name = schema_name
        self.table_name = table_name

    def execute(self, cursor):
        try:
            negative_words = [
                "Office 365",
                "Adobe",
                "Autocad",
                "CorelDraw",
                "Power",
                "VMware",
                "vSphere",
                "Copilot",
                "Autodesk",
                "Acrobat",
                "Revit",
                "Acquia",
                "ARCHITECTURE",
                "DYNAMICS",
                "Creative",
                "E-Mobility",
                "BPO",
                "Jira",
                "Kaspersky",
                "Dynatrace",
            ]

            conditions = sql.SQL(" OR ").join(
                [
                    sql.SQL("descricao ILIKE {word}").format(
                        word=sql.Literal(f"%{word}%")
                    )
                    for word in negative_words
                ]
            )

            conditions += sql.SQL(" OR ") + sql.SQL(" OR ").join(
                [
                    sql.SQL("objeto ILIKE {word}").format(word=sql.Literal(f"%{word}%"))
                    for word in negative_words
                ]
            )

            descricao_comp_column_exists = check_column_exists(
                cursor, self.schema_name, self.table_name, "descricao_comp"
            )
            
            if descricao_comp_column_exists:
                conditions += sql.SQL(" OR ") + sql.SQL(" OR ").join(
                    [
                        sql.SQL("descricao_comp ILIKE {word}").format(word=sql.Literal(f"%{word}%"))
                        for word in negative_words
                    ]
                )

            final_query = self.query.format(
                schema_name=sql.Identifier(self.schema_name),
                table_name=sql.Identifier(self.table_name),
                conditions=conditions,
            )

            cursor.execute(final_query)
            cursor.connection.commit()
            print(cursor.statusmessage)
        except errors.Error as e:
            print("Erro ao tentar atualizar palavras negativas:", e)
            cursor.connection.rollback()
            exit(1)
