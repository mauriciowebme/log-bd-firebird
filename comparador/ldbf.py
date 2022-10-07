import datetime
from traceback import print_exc
import fdb
import time
import validador_configuracao

def Conecta_banco_pavani(ip, caminho):
    while True:
        try:
            con = fdb.connect(host=ip, database=caminho, user='SYSDBA', password='masterkey', charset='WIN1252')
        except Exception as ex:
            print(datetime.datetime.today())
            print('\nErro na conexão com o banco de dados!')
            print_exc()
            print('Aguardando 1 min para tentar novamente!')
            time.sleep(60)
        else:
            return con

dados_config = validador_configuracao.Pega_conf()
dados = {}

while True:
    try:
        data_atual = str(datetime.datetime.today()).split(' ')[0].split('-')
        data_atual = data_atual[2]+"."+data_atual[1]+"."+data_atual[0]

        sql = f"""
            SELECT
            FIRST(200) 
            ilt.ID 
            ,ilt.TABLE_NAME 
            ,ilt.OPERATION 
            ,ilt.DATE_TIME 
            ,ilt.IDUSRALTEROU 
            ,ilk.KEY_FIELD 
            ,ilk.KEY_VALUE 
            ,ilf.FIELD_NAME 
            ,ilf.OLD_VALUE  
            ,ilf.NEW_VALUE 
            FROM IBE$LOG_TABLES ilt
            INNER JOIN IBE$LOG_KEYS ilk ON ilt.ID = ilk.LOG_TABLES_ID
            INNER JOIN IBE$LOG_FIELDS ilf ON ilt.ID = ilf.LOG_TABLES_ID
            WHERE
            ilt.DATE_TIME >= '{data_atual} 00:00:01'
            """
        wheres = {
                "TABLE_NAME":dados_config['TABLE_NAME']
                ,"FIELD_NAME":dados_config['FIELD_NAME']
                ,"KEY_VALUE":""
                ,"OLD_VALUE":""
                ,"NEW_VALUE":""
            }
        for campo in wheres:
            if wheres[campo] != "":
                sql += f"and {campo} = '{wheres[campo]}'\n"
        sql += "ORDER BY ilt.ID"#DESC

        conn = Conecta_banco_pavani(dados_config['ip'], dados_config['caminho'])
        cur = conn.cursor()
        cur.execute(sql)
        resultados = cur.fetchall()
        conn.close()

        if dados == {}:
            for x in resultados:
                dados[x[0]] = x
        else:
            for x in resultados:
                if x[0] not in dados:
                    print(f"Modificação encontrada: {x}")
                    dados[x[0]] = x
        time.sleep(60)
    except Exception as ex:
        print("Erro ao executar!\nTentando novamente em 1 min...")
        print_exc()
        time.sleep(60)