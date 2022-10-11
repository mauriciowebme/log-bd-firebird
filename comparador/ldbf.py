import datetime
import os
import subprocess
import sys
from traceback import print_exc
import fdb
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import zipfile
import smtplib

def Cria_tutorial():
    if os.path.exists(f'{path_arq}\\tutorial.txt') == False:
        tutorial = open(f'{path_arq}\\tutorial.txt', 'w', encoding='utf8')
        mensagem = """
email_senha:
Para criar essa senha você vai entrar no seu e-mail, pode acessar as informações da sua conta no canto superior direito e vai clicar em Gerenciar sua Conta do Google
Na próxima página você vai clicar em Segurança e vai descer um pouco até a parte de Como fazer login no Google
Ativando a verificação em duas etapas para habilitar a senha de app
Nessa parte você vai ter que ativar a verificação em duas etapas para poder habilitar a parte de Senhas de app, que é a senha que vamos utilizar dentro do Python
Então quando você clicar em senhas de app, vai aparecer uma janela para que você possa fazer o login no seu e-mail já utilizando a verificação em duas etapas
Depois de fazer o login você vai escolher qual o app do Google você quer gerar sua senha e depois vai dar um nome para esse dispositivo.
        """
        tutorial.write(mensagem)
        tutorial.close()
        print("Tutorial criado!")

def Pega_conf():
    while True:
        try:
            arq_conf = {
                'TABLE_NAME':'',
                'FIELD_NAME':'',
                'ip':'',
                'caminho':'',
                'email_destinatario':[],
                'email_remetente':'',
                'email_senha':'',
                'verificacao_segundos':'',
            }
            open(f'{path_arq}\\start.ini', 'a')
            start = open(f'{path_arq}\\start.ini', 'r')
            recriar_l = [True, True, True, True, True, True, True, True,]
            vazio = [True, True]
            confi_vazio = ""
            for l in start.readlines():
                if 'ip' in l:
                    arq_conf['ip'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[0] = False
                    if arq_conf['ip'] == '':
                        confi_vazio += "ip, "
                elif 'caminho' in l:
                    arq_conf['caminho'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[1] = False
                    if arq_conf['caminho'] == '':
                        confi_vazio += "caminho, "
                elif 'email_destinatario' in l:
                    destinatarios = l.split('=')[1].split(',')
                    for destinatario in destinatarios:
                        arq_conf['email_destinatario'] += [destinatario.replace('\n','').replace(' ','')]
                    recriar_l[2] = False
                    if arq_conf['email_destinatario'] == ['']:
                        confi_vazio += "email_destinatario, "
                elif 'email_remetente' in l:
                    arq_conf['email_remetente'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[3] = False
                    if arq_conf['email_remetente'] == '':
                        confi_vazio += "email_remetente, "
                elif 'email_senha' in l:
                    arq_conf['email_senha'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[4] = False
                    if arq_conf['email_senha'] == '':
                        confi_vazio += "email_senha, "
                elif 'verificacao_segundos' in l:
                    arq_conf['verificacao_segundos'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[5] = False
                    if arq_conf['verificacao_segundos'] == '':
                        confi_vazio += "verificacao_segundos, "
                elif 'TABLE_NAME' in l:
                    arq_conf['TABLE_NAME'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[6] = False
                    if arq_conf['TABLE_NAME'] != '':
                        vazio[0] = False
                elif 'FIELD_NAME' in l:
                    arq_conf['FIELD_NAME'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[7] = False
                    if arq_conf['FIELD_NAME'] != '':
                        vazio[1] = False
                
            start.close()
            start = open(f'{path_arq}\\start.ini', 'a')
            index_recriar = -1
            for recriar in  recriar_l:
                index_recriar += 1
                if recriar == True:
                    if index_recriar == 0:
                        start.write('\nip=')
                    if index_recriar == 1:
                        start.write('\ncaminho=')
                    if index_recriar == 2:
                        start.write('\nemail_destinatario=')
                    if index_recriar == 3:
                        start.write('\nemail_remetente=')
                    if index_recriar == 4:
                        start.write('\nemail_senha=')
                    if index_recriar == 5:
                        start.write('\nverificacao_segundos=')
                    if index_recriar == 6:
                        start.write('\nTABLE_NAME=')
                    if index_recriar == 7:
                        start.write('\nFIELD_NAME=')
                    
            start.close()
            if True not in recriar_l:
                concluir = "\nFeche e abra o aplicativo para pegar as novas configurações!"
                if confi_vazio != "":
                    print('O(s) campo(s) de configuração deve ser preenchido(s):',confi_vazio, concluir)
                    input()
                    break
                elif False in vazio:
                    print(f'Aquivo de configuração carregado.')
                    return arq_conf
                else:
                    print(f'Pelo menos um dos campos de pesquisa deve ser preenchido!', concluir)
                    input()
                    break
        except Exception as ex:
            print('Erro ao verificar aquivo de configuração', ' '*50, end='\r')
            time.sleep(1)

def Enviaemail(assunto, html, anexos, destinatarios=[], arq_zip=True):
    while True:
        try:
            for destinatario in destinatarios:
                username = dados_config["email_remetente"]
                password = dados_config["email_senha"]
                mail_from = dados_config["email_remetente"]
                if assunto == None or assunto == '':
                    assunto = "IAGO ERRO"
                if html == None or html == '':
                    html = """
                    Erro no envio do email
                    """
                if anexos == None or anexos == '':
                    anexos = []
                mimemsg = MIMEMultipart()
                mimemsg['From']=mail_from
                mimemsg['To']=destinatario
                mimemsg['Subject']=assunto
                mimemsg.attach(MIMEText(html, 'html'))
                limpa_anexo = []
                if anexos != []:
                    for anexo in anexos:
                        nome_anexo_cExt = os.path.split(anexo['caminho'])[1]
                        caminho_nome_anexo_sExt = os.path.splitext(anexo['caminho'])[0]
                        ext_anexo = os.path.splitext(anexo['caminho'])[1]
                        if arq_zip == True:
                            ext_anexo = '.zip'
                            with zipfile.ZipFile(caminho_nome_anexo_sExt+'.zip', 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                                z.write(anexo['caminho'], nome_anexo_cExt)
                        limpa_anexo += [caminho_nome_anexo_sExt+ext_anexo]
                        attachment =open(caminho_nome_anexo_sExt+ext_anexo,'rb')
                        addanexo = MIMEBase('application', 'octet-stream')
                        addanexo.set_payload(attachment.read())
                        encoders.encode_base64(addanexo)
                        nome = anexo['nome']
                        addanexo.add_header('Content-Disposition', f'attachment; filename= {nome}{ext_anexo}')
                        attachment.close
                        mimemsg.attach(addanexo)
                conexao = smtplib.SMTP_SSL(host='smtp.gmail.com', port=465)
                conexao.login(username,password)
                conexao.send_message(mimemsg)
                conexao.quit()
                print('E-mail enviado!')
        except Exception as ex:
            print(str(datetime.datetime.today()).split('.')[0])
            print('\nErro: Enviaemail()')
            print_exc()
            print('Tentando novamente em 1 minuto...')
            time.sleep(60)
        else:
            return limpa_anexo

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

def Monta_Estrutura_pasta(caminho):
    print('Corrigindo estrutura de pastas...')
    subprocess.run([
        "mkdir"
        ,caminho
        ]
        , stderr = subprocess.PIPE
        , shell=True)
    print('Correção de estrutura completa!')
    return caminho

def main():
    dados = []
    print('iniciando analise de tabelas...')
    while True:
        try:
            
            data_atual = str(datetime.datetime.today()).split(' ')[0].split('-')
            data_atual = data_atual[2]+"."+data_atual[1]+"."+data_atual[0]

            sql = f"""
                SELECT
                --FIRST(200) 
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
            sql += "ORDER BY ilt.ID "#DESC

            conn = Conecta_banco_pavani(dados_config['ip'], dados_config['caminho'])
            cur = conn.cursor()
            cur.execute(sql)
            resultados = cur.fetchall()
            conn.close()

            if dados == []:
                for x in resultados:
                    dados += [x[0]]
            else:
                mensagem_log_cabecalho = "TABLE_NAME ;OPERATION ;DATE_TIME ;IDUSRALTEROU ;KEY_FIELD ;KEY_VALUE ;FIELD_NAME ;OLD_VALUE  ;NEW_VALUE ;\n"
                mensagem_log = ""
                for x in resultados:
                    if x[0] not in dados:
                        print('Modificação encontrtada!')
                        dados += [x[0]]
                        mensagem = f"{x[1]} ;{x[2]} ;{str(x[3]).split('.')[0]} ;{x[4]} ;{x[5]} ;{x[6]} ;{x[7]} ;{x[8]} ;{x[9]} ;"
                        print(mensagem)
                        mensagem_log += mensagem+'\n'
                if mensagem_log != "":
                    existe = os.path.lexists(f'{path_arq}\\logs')
                    if existe == False:
                        Monta_Estrutura_pasta(f'{path_arq}\\logs')
                    data_hora_atual = str(datetime.datetime.today()).split('.')[0].replace(' ','_').replace(':', '-')
                    caminho_log = f'{path_arq}\\logs\\log_{data_hora_atual}.txt'
                    log = open(caminho_log, 'a')
                    mensagem_completa = mensagem_log_cabecalho + mensagem_log
                    print(mensagem_completa, file=log)
                    log.close()
                    assunto = 'Modificação encontrada'
                    destinatarios = dados_config['email_destinatario']
                    html = 'Segue o log em anexo.'
                    limpa_anexo = Enviaemail(assunto, destinatarios=destinatarios, html=html, anexos=[{'caminho':caminho_log, 'nome':'log'}], arq_zip=True)
                    for limpar in limpa_anexo:
                        try:
                            os.remove(limpar)
                        except:
                            pass
            time.sleep(int(dados_config["verificacao_segundos"]))
        except Exception as ex:
            print("Erro ao executar!\nTentando novamente em 1 min...")
            print_exc()
            time.sleep(60)

if "__main__" in __name__:
    global path_arq
    if getattr(sys, 'frozen', False):
        path_arq = os.path.dirname(sys.executable)
    elif __file__:
        path_arq = os.path.dirname(__file__)
    Cria_tutorial()
    global dados_config
    dados_config = Pega_conf()
    #Enviaemail(assunto='teste', destinatarios=dados_config['email_destinatario'], anexos=[], html='teste')
    main()