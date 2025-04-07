import csv 
from src.db.config import ConfigDB
from psycopg2 import errors
from psycopg2 import sql
import datetime
import re
config = ConfigDB()




def copy_table():
    query = "CREATE TABLE propostas"


def insert_data_table(schema, table_name, **d):
    with config.connection:
        cur = config.connection.cursor()  # Usando o cursor corretamente a partir da conexão
        try:
            # Preparando a consulta SQL com 17 marcadores de posição
            query = sql.SQL("""
                    INSERT INTO {schema}.{table_name} (
                    item_id, data, orgao, uf, objeto,
                    cnpj, razao_social, marca, modelo, fabricante,
                    unidade_de_medida, modalidade, valor_total, valor_unitario, base,
                    descricao, termo, classificado, fase
                    ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                    %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT (item_id) DO NOTHING;
            """).format(
                schema=sql.Identifier(schema),
                table_name=sql.Identifier(table_name)
            )
            valor_total = d['valor_total'].replace(".", "").replace(",",".")
            valor_unitario = d['valor_unitario'].replace(".", "").replace(",",".")
            # Extraindo e tratando os dados
            item_id = f"{d['base']} - {d['id']}"
            data = datetime.datetime.strptime(d['data'], "%d/%m/%Y")
            orgao = d['orgao']
            objeto = d['objeto']
            cnpj_vencedor =  str(d['cnpj'])
            forn_vencedor = d['razao_social']
            marca = 'não informado'
            modelo = 'não informado'
            unidade = d['unidade_de_medida']
            modalidade =str(d['modalidade'])
            valor_total = float(valor_total)
            valor_unitario = float(valor_unitario)
            desc_reduzido = d['descricao']
            termo =  d['termo']
            uf = d['uf']
            base = d['base']
            
            
            classificacao = None
            fase = None
            fabricante = 'não informado'
            
            # Imprimindo os parâmetros antes de executar a query
            print("Parâmetros a serem passados para a query:", (
                 item_id, data, orgao, uf, objeto,
                cnpj_vencedor, forn_vencedor, marca, modelo, fabricante,
                unidade, modalidade, valor_total, valor_unitario, base,
                desc_reduzido, termo, classificacao, fase
            ))

            # Executando a query com todos os parâmetros
            cur.execute(query, (
                item_id, data, orgao, uf, objeto,
                cnpj_vencedor, forn_vencedor, marca, modelo, fabricante,
                unidade, modalidade, valor_total, valor_unitario, base,
                desc_reduzido, termo , classificacao, fase
            ))
            
            # Confirmando a transação
          
            config.connection.commit()
        
        except errors.Error as e:
            print(f"Erro ao adicionar item: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def update_item_values(schema, table_name, item_id, url_ata, url_edital):
   
    """
    Atualiza apenas os valores unitário e total de um item na tabela.
    
    Args:
        schema: Nome do schema no banco de dados
        table_name: Nome da tabela
        item_id: ID do item a ser atualizado (sem o prefixo 'PNCP-')
        valor_unitario: Novo valor unitário
        valor_total: Novo valor total
        
    Returns:
        Mensagem com o resultado da operação
    """
    with config.connection:
        cur = config.connection.cursor()
        try:
            
            # Preparando a query de atualização
            query = sql.SQL("""
                UPDATE {schema}.{table_name} 
                SET url_ata = %s,
                    url_edital = %s
                WHERE item_id = %s
            """).format(
                schema=sql.Identifier(schema),
                table_name=sql.Identifier(table_name)
            )
            
            # Formatando o item_id com o prefixo PNCP se necessário
            # item_id_formatted = 'PNCP' +"-"+ str(item_id) 
            
            # Convertendo valores para float
            # valor_unitario_float = float(valor_unitario)
            # valor_total_float = float(valor_total)
            
            # Executando a query
            cur.execute(query, (url_ata, url_edital, item_id))
            
            # Contando o número de linhas afetadas
            rows_affected = cur.rowcount
            
            # Confirmando a transação
            config.connection.commit()
            print(f"{cur.statusmessage} item {item_id}")
            
            return f"Atualizado {rows_affected} registro(s). Item: {item_id}"
            
        except errors.Error as e:
            config.connection.rollback()
            return f"Erro do banco de dados ao atualizar item: {e}"
        except Exception as e:
            config.connection.rollback()
            return f"Erro inesperado ao atualizar item: {e}"
        
# with open('src/db/utils/results/totvs_itens.csv', 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter=',')
#     index = 0
#     data_dump = []
#     data_formated = []
    
    
#     for row in csv_reader:
        # print(row)
        
        # print(datetime.datetime.date(datetime.datetime.strptime(row['data'], r"%d/%m/%Y")))
        # if row['valor_total'] == '' or row['valor_unitario'] == '':
        #     continue
        # print(row)
        # insert_data_table('04_04_2025', 'dados_nao_tratados', **row)
        # item_id = f"{row['base']} - {row['id']}"
        
        # update_item_values('02_04_2025', 'dados_tratados', item_id, row['url_ata'], row['url_edital'])


with open('src/db/utils/results_07_04_2025/totvs_itens.csv', 'rb') as csv_file:
    cleaned_lines = (line.replace(b'\x00', b'') for line in csv_file)
    decoded_lines = (line.decode('utf-8') for line in cleaned_lines)
    csv_reader = csv.DictReader(decoded_lines, delimiter=',')

    index = 0
    data_dump = []
    data_formated = []

    for row in csv_reader:
        insert_data_table('07_04_2025', 'dados_nao_tratados', **row)


def insert_data_forn(schema, table_name, **d):
    with config.connection:
        cur = config.connection.cursor()

        try:
            # Preparando a consulta SQL com 17 marcadores de posição
            query = sql.SQL("""
                INSERT INTO {schema}.{table_name} (
                    item_id, fornecedor, cnpj, valor_unitario, valor_total
                ) VALUES (
                    %s, %s, %s, %s, %s
                )
            """).format(
                schema=sql.Identifier(schema),
                table_name=sql.Identifier(table_name)
            )

            cur.execute(query, ('00000000049528110000110100000220251', d['nome'], d['identificacao'], 
            d['valorUnitario'], d['valorTotal']))

            print(f"{cur.statusmessage} fornecedor {d['nome']}")
            config.connection.commit()
        
        except errors.Error as e:
            print(f"Erro ao adicionar proposta: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
     

historico =   [
            {
                "identificacao": "20491731000194",
                "nome": "PONTOREALL COMÉRCIO E SERVIÇOS DE RELÓGIO DE ",
                "valorUnitario": 4380,
                "valorTotal": 4380
            },
            {
                "identificacao": "28175080000135",
                "nome": "SISTEMPONTO EIRELI ",
                "valorUnitario": 7164,
                "valorTotal": 7164
            },
            {
                "identificacao": "17206739000157",
                "nome": "DIGIMATEC RELÓGIOS DE PONTO",
                "valorUnitario": 5222,
                "valorTotal": 5222,
            },
            {
                "identificacao": "17262425000171",
                "nome": "SC PONTO CONTROLE DE PONTO E ACESSO",
                "valorUnitario": 7740,
                "valorTotal": 7740
            },
            
        ]
# for d in historico:
#     insert_data_forn('31_01_2025', 'fornecedores', **d)


def update_values_table(schema, table_name, **d):
    with config.connection:
       
        cur = config.connection.cursor()  # Usando o cursor corretamente a partir da conexão
        try:
            item_id = str(d['item_id'])
            valor_total = float(d['valor_total'])
            valor_unitario = float(d['valor_unitario'])
            # Preparando a consulta SQL com 17 marcadores de posição
            query = sql.SQL("""
                UPDATE {schema}.{table_name} SET 
                valor_unitario = %s, 
                valor_total = %s
                WHERE item_id = %s
            """).format(
                schema=sql.Identifier(schema),
                table_name=sql.Identifier(table_name)
            )
            cur.execute(query, (valor_unitario, valor_total, item_id))
            print(f"{cur.statusmessage} item {item_id}")
            config.connection.commit()
        except errors.Error as e:
            print(f"Erro ao adicionar item: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# with open('src/db/utils/pncp_item_202503101615.csv', 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file, delimiter=',')
#     index = 0
#     data_dump = []
#     data_formated = []
#     print
    
#     for row in csv_reader:
#         # if row['valor_total'] == '' or row['valor_unitario'] == '':
#         #     continue

#         update_values_table('fevereiro2', 'dados_nao_tratados', **row)