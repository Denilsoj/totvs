from psycopg2 import errors, sql


class ApplyFilterByOrgan:
    ufs = {
        "AC": [],
        "AL": [],
        "AM": ["Manaus"],
        "AP": [],
        "BA": ["Salvador", "Feira de Santana"],
        "CE": ["Fortaleza"],
        "DF": ["Brasília", "Brasilia"],
        "ES": ["Serra", "Vila Velha"],
        "GO": ["Goiânia", "Aparecida de Goiânia", "Goiania", "Aparecida de Goiania"],
        "MA": ["São Luís", "Sao Luis"],
        "MG": ["Belo Horizonte", "Uberlândia", "Uberlandia", "Contagem", "Juiz de Fora"],
        "MS": [],
        "MT": [],
        "PA": ["Belém", "Belem"],
        "PB": [],
        "PE": ["Recife", "Jaboatão dos Guararapes", "Jaboatao dos Guararapes"],
        "PI": [],
        "PR": ["Curitiba", "Londrina"],
        "RJ": ["Rio de Janeiro", "São Gonçalo", "Sao Goncalo", "Duque de Caxias", "Nova Iguaçu", "Nova Iguacu"],
        "RN": [],
        "RO": [],
        "RR": [],
        "RS": ["Porto Alegre"],
        "SC": ["Joinville"],
        "SE": [],
        "SP": [
            "Campinas",
            "Guarulhos",
            "Osasco",
            "Ribeirão Preto",
            "Ribeirao Preto",
            "Santo André",
            "Santo Andre",
            "São Bernardo do Campo",
            "Sao Bernardo do Campo",
            "São José dos Campos",
            "Sao Jose dos Campos",
            "São Paulo",
            "Sao Paulo",
            "Sorocaba",
        ],
        "TO": [],
    }

    query = sql.SQL(
        """
        UPDATE {schema_name}.{table_name}
        SET classificado = true, fase = 3
        WHERE {where_statement}
        """
    )

    def __init__(self, schema_name, table_name):
        self.schema_name = schema_name
        self.table_name = table_name

    def execute(self, cursor):
        for uf, cities in self.ufs.items():
            where_statement = sql.SQL(
                """
                uf = {uf}
                AND (
                    orgao ILIKE '%prefeitura%'
                    or orgao ILIKE '%municip%'
                    or orgao ILIKE '%municíp%'
                    or orgao ILIKE '%pref.mun.%'
                )
                """
            ).format(uf=sql.Literal(uf))

            if len(cities) > 0:
                for city in cities:
                    where_statement += sql.SQL(
                        "AND orgao NOT ILIKE {city} "
                    ).format(city=sql.Literal(f"%{city}%"))
            where_statement += sql.SQL(";")

            try:
                formatted_query = self.query.format(
                    schema_name=sql.Identifier(self.schema_name),
                    table_name=sql.Identifier(self.table_name),
                    where_statement=where_statement
                )
                
                print(formatted_query.as_string(cursor))

                cursor.execute(formatted_query)
                print(cursor.statusmessage)
            except errors.Error as e:
                print(f"Erro ao atualizar itens por órgão ({uf}):", e)

