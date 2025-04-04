from psycopg2 import sql

from src.db.config import ConfigDB


def clean_cnpj(cnpj):
    return (
        cnpj.replace(".", "")
        .replace("/", "")
        .replace("-", "")
        .replace(" ", "")
        .zfill(14)
    )


db = ConfigDB()

db.cursor.execute(sql.SQL("SELECT distinct cnpj FROM final.dados_limpos"))
cnpjs = db.cursor.fetchall()


with open("cnpjs.txt", "w") as file:
    for cnpj in cnpjs:
        cleaned_cnpj = clean_cnpj(cnpj["cnpj"])
        # print(cnpj["cnpj"], "->", cleaned_cnpj)
        # print(f"{cnpj['cnpj']:15} -> {cleaned_cnpj:14}")
        # file.write(f"{cleaned_cnpj:14}\n")

        db.cursor.execute(
            sql.SQL("UPDATE final.dados_limpos SET cnpj = %s WHERE cnpj = %s"),
            [cleaned_cnpj, cnpj["cnpj"]],
        )

        db.connection.commit()
        print(db.cursor.statusmessage)
