import os
import time

def Pega_conf():
    while True:
        try:
            path_arq = os.path.dirname(__file__)
            arq_conf = {
                'TABLE_NAME':'',
                'FIELD_NAME':'',
                'ip':'',
                'caminho':'',
            }
            open(f'{path_arq}\\start.ini', 'a')
            start = open(f'{path_arq}\\start.ini', 'r')
            recriar_l = [True, True, True, True,]
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
                elif 'TABLE_NAME' in l:
                    arq_conf['TABLE_NAME'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[2] = False
                    if arq_conf['TABLE_NAME'] != '':
                        vazio[0] = False
                elif 'FIELD_NAME' in l:
                    arq_conf['FIELD_NAME'] = l.split('=')[1].replace('\n','').replace(' ','')
                    recriar_l[3] = False
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
                        start.write('\nTABLE_NAME=')
                    if index_recriar == 3:
                        start.write('\nFIELD_NAME=')
                    
            start.close()
            if True not in recriar_l:
                if confi_vazio != "":
                    print(f'O(s) campo(s) de configuração deve ser preenchido(s): {confi_vazio}', ' '*50, end='\r')
                    time.sleep(1)
                elif False in vazio:
                    print(f'Aquivo de configuração carregado.', ' '*60)
                    return arq_conf
                else:
                    print(f'Pelo menos um dos campos de pesquisa deve ser preenchido!', ' '*50, end='\r')
                    time.sleep(1)
        except Exception as ex:
            print('Erro ao verificar aquivo de configuração', ' '*50, end='\r')
            time.sleep(1)
if __name__ == '__main__':
    os.system('cls')
    Pega_conf()
