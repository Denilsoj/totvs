from db.config import ConfigDB


config = ConfigDB()


config.cursor.execute(
    "SELECT item_id, valor_unitario, valor_total FROM final.dados_limpos"
)
prices = config.cursor.fetchall()

for wrong_price in prices:
    config.cursor.execute(
        'SELECT item_id, valor_unitario, valor_total FROM "23_12_2024".dados_nao_tratados WHERE item_id = %s',
        [wrong_price["item_id"]],
    )
    correct_price = config.cursor.fetchone()
    if (
        correct_price
        and correct_price["valor_unitario"] != wrong_price["valor_unitario"]
    ):
        config.cursor.execute(
            "UPDATE final.dados_limpos SET valor_unitario = %s, valor_total = %s WHERE item_id = %s",
            [
                correct_price["valor_unitario"],
                correct_price["valor_total"],
                wrong_price["item_id"],
            ],
        )
        config.connection.commit()
        print(config.cursor.statusmessage)
