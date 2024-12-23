import os, time

from dotenv import load_dotenv
import google.generativeai as genai
from psycopg2 import sql


load_dotenv()

genai.configure(api_key=os.environ.get("GOOGLE_GENERATIVEAI_API_KEY", ""))


class ClassifyContextWithAI:
    initial_prompt = """
    <tarefa>
    Voce é um especialista em análise de processos licitatórios da empresa TOTVS. Eu lhe fornecerei uma <descricao> e gostaria de saber se a <descricao> se encaixa no contexto dos diversos termos que você costuma analisar ao avaliar processos licitatórios nos quais a empresa pode participar. 

    Esta relação de produtos e serviços que a empresa TOTVS oferece e que você costuma analisar:

    1. ERP
    2. Enterprise Resource Planning;
    3. Sistema de gestão;
    4. Sistema de gestão empresarial;
    5. Software de gestão integrada;
    6. Solução ERP;
    7. Solução Integrada de Software;
    8. Solução Integrada de Gestão Empresarial;
    9. Aquisição de ERP;
    10. Software de gestão integrada;
    11. ERP;
    12. Backoffice;
    13. Suporte ao ERP;
    14. Protheus; 
    15. RM;
    16. RH
    17. Sistema de Recursos Humanos;
    18. Solução para Gestão de RH;
    19. Sistema para Gestão de pessoas.
    20. Folha de pagamento;
    21. Sistema de Gestão de talentos;
    22. Sistema de Recrutamento e seleção;
    23. Sistema de Desenvolvimento de pessoal;
    24. Sistema de Avaliação de desempenho;
    25. Sistema para controle e gestão de batidas de ponto;
    26. Controle de ponto;
    27. Ponto eletrônico; 
    28. Gestão de pessoas;  
    29. Sistema educacional;
    30. Software educacional;
    31. Gestão educacional;
    32. Plataforma educacional;
    33. Sistema de gestão escolar;
    34. Sistema de gestão jurídica;
    35. Software de gestão jurídica;
    36. Sistema jurídico;
    37. Software jurídico;
    38. Gestão de departamento jurídico; 
    39. Controle de processos judiciais; 
    40. Controle de processos ou procedimentos administrativos; 
    41. Controle de processos disciplinares
    42. Sistema de gestão hospitalar;
    43. Software de gestão hospitalar;
    44. Sistema hospitalar;
    45. Software hospitalar;
    46. Gestão de hospitais;
    47. Gestão de planos de saúde;
    48. Gestão de unidades de saúde;
    49. Gestão de postos de atendimento;
    50. SaaS;
    51. Software as a Service;
    52. Cloud;
    53. Cloud Computing;
    54. Computação em nuvem;
    55. Solução em nuvem;
    56. Data Center;
    57. Gestão de Documentos;
    58. Omnichannel;

    Verifique também a ocorrência de termos relacionados aos concorrentes da empresa TOTVS, como:

    1. MXM;
    2. Sydle;
    3. Benner;
    4. Alfa Sistemas;
    5. Sankhya;
    6. Senior Sistemas;
    7. SoftPlan;
    8. Beta Sistemas;
    9. Sonda;
    10. SAP;
    11. Microsoft;
    12. Techne;
    13. Philips Medical;
    14. MV Sistemas;
    15. LG Informática;
    16. TIVIT;
    17. Edusoft;
    18. Solutis;
    19. Totvs;
    20. Oracle;
    21. SEIDOR
    22. DELAWARE
    23. MIGNOW TECHNOLOGY
    24. NUMEN
    25. NTT DATA
    26. EXED
    27. ACCENTURE
    28. CAST GROUP
    29. EPI-USE
    30. SPRO
    31. GYANSYS
    32. EY
    33. T-SYSTEMS
    34. DELOITTE
    35. PWC
    36. CONVISTA
    37. MSG
    38. CAPGEMINI
    39. AVVALE
    40. ATOS
    41. MINSAIT
    42. IBM
    43. DXC
    44. KPMG
    45. SNP
    46. SOFTTEK
    47. COGNIZANT
    48. ACCENTURE
    49. THOMSON REUTERS
    50. KORBER
    51. CLOUD 4C
    52. ADIANTA
    53. BOAVISTA TECNOLOGIA
    54. EDUSOFT
    55. FLEXY
    56. HDANDIT
    57. ILOG
    58. LOBTEC
    59. LINTER
    60. LOGUS SISTEMAS
    61. QLIK
    62. QUIRIUS
    63. NARWAL
    64. MGP
    65. TEIKO
    66. NEXERA
    67. ANALIZE
    68. APIPASS
    69. CCM
    70. NUVEM DATACOM
    71. ARTURIA
    72. FUSION
    73. LANDIX
    74. SOVIS
    75. MEGGAZ TECNOLOGIA
    76. KABEVI
    77. ITFOURBS
    78. Corpore Soluções
    79. SENSUS

    E gostaria que voce me retornase apenas, "sim" se a <descricao> se encaixar com o contexto dos termos ou "nao" caso contrário. Se nao souber responder, por padrao responda "nao". Note que a resposta deve ser baseada no contexto da <descricao> e nao apenas na presença dos termos e sempre escreva a resposta em letras minusculas e sem acentos.
    </tarefa>
    <exemplos>
    1. descricao:  "AQUISIÇÃO DE MOBILIÁRIOS E EQUIPAMENTOS ELETRÔNICOS DESTINADOS A SUPRIR A DEMANDA DA CASA LAR E SECRETÁRIA DE ASSISTÊNCIA SOCIAL DO MUNICÍPIO DE CAFELÂNDIA. ATRAVÉS DE RECURSOS DA EMENDA PARLAMENTAR BANCADA DO PARANÁ N°202371170013, REQUERIDO ATRAVÉS DA PROGRAMAÇÃO SISTEMA DE GESTÃO DE TRANSFERÊNCIA VOLUNTARIAS- SIGTV" resultado: "nao" justificativa: "apesar do texto conter a palavra, nao se encaixa com o contexto da palavra"
    </exemplos>
    """

    template_message = "Verifique a descrição a seguir e valide se ela se aplica ao contexto de licitações favoráveis à empresa TOTVS: <descricao>{descricao}</descricao>"

    def __init__(self, schema_name, table_name):
        self.schema_name = schema_name
        self.table_name = table_name

        gemini = genai.GenerativeModel("gemini-1.5-flash")
        self.chat = gemini.start_chat()
        self.chat.send_message(self.initial_prompt)

    def _classify_row(self, row):
        descricao = row["objeto"]
        if len(descricao) < len(row["descricao"]):
            descricao = row["descricao"]

        result = self.chat.send_message(
            self.template_message.format(descricao=descricao)
        )

        return True if str.strip(result.text) == "sim" else False

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
                time.sleep(10)
                print(f"- Classifying row {row['id']}")

                if not self._classify_row(row):
                    continue

                try:
                    update_query = sql.SQL(
                        "UPDATE {schema_name}.{table_name} SET classificado = true, fase = 4 WHERE id = {id};"
                    ).format(
                        schema_name=sql.Identifier(self.schema_name),
                        table_name=sql.Identifier(self.table_name),
                        id=sql.Literal(row["id"]),
                    )
                    cursor.execute(update_query)
                    cursor.connection.commit()
                    print(cursor.statusmessage)
                except Exception as e:
                    print(f"Erro ao tentar classificar on row {row['id']} (IA): {e}")
                    cursor.connection.rollback()
                    exit(1)
