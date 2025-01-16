from psycopg2 import sql


def check_column_exists(cursor, schema_name, table_name, column_name) -> bool:
    query = sql.SQL(
        """
        SELECT EXISTS(
            SELECT 1 FROM information_schema.columns
            WHERE 
                table_schema = {schema_name}
                AND table_name = {table_name}
                AND column_name = {column_name}
        );
        """
    ).format(
        schema_name=sql.Literal(schema_name),
        table_name=sql.Literal(table_name),
        column_name=sql.Literal(column_name),
    )
    cursor.execute(query)
    return cursor.fetchone()["exists"]
