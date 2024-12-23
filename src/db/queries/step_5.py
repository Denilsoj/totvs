from psycopg2 import errors, sql


class SetUnclassifiedAsApproved:
    query = sql.SQL(
        """
        UPDATE {schema_name}.{table_name}
        SET fase = 5, classificado = true
        WHERE fase = 0 AND classificado = false;
        """
    )

    def __init__(self, schema_name, table_name):
        self.schema_name = schema_name
        self.table_name = table_name

    def execute(self, cursor):
        try:
            formatted_query = self.query.format(
                schema_name=sql.Identifier(self.schema_name),
                table_name=sql.Identifier(self.table_name),
            )

            cursor.execute(formatted_query)
            cursor.connection.commit()
            print(cursor.statusmessage)
        except errors.Error as e:
            print(f"Erro ao aprovar itens não classificados ({self.table_name}):", e)
            cursor.connection.rollback()
            exit(1)
