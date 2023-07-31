"""
Projeto final do aluno Luis Felipe Gilisk de Olieira
Módulo Lógida de Programação II
"""
import json
import os


def main():
    try:
        menu_principal()
    except Exception as e:
        print(f"Erro de execução:\n{e}")


def arquivo_usuarios():
    """
    Coleta o endereço onde está localizado o arquivo .json
    """
    return os.path.join(os.getcwd(), 'projetoModuloII.json')


def menu_principal():
    """
    Menu para navegar entre as opções
    """
    opcao = None
    print("Boas vindas ao nosso sistema!\n")
    while opcao != '6':
        print("::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n"\
            ":::::::::::::::: >>> MENU PRINCIPAL <<< ::::::::::::::::\n"\
            "::::::::::::::::::::::::::::::::::::::::::::::::::::::::\n\n"\
            '1 - Inserir usuário\n'\
            '2 - Excluir usuário\n'\
            '3 - Atualizar usuário\n'\
            '4 - Informações de um usuário\n'\
            '5 - Informações de todos os usuários\n'\
            '6 - Sair\n')
        opcao = input("Digite a opcao escolhida: ")
        if opcao not in ('1', '2', '3', '4', '5', '6'):
            print("Opção inválida!")
        else:
            switch_menu = {
                '1': insere_usuario,
                '2': inativa_usuario,
                '3': atualiza_usuario,
                '4': informacoes_usuario,
                '5': exibe_usuarios_formatado,
                '6': finaliza_execucao,
            }
            switch_menu.get(opcao)()
    

def usuarios_json():
    """
    Carrega o arquivo json com as informações em formato dict
    """
    with open(arquivo_usuarios(), 'r', encoding='UTF-8') as json_file:
        conteudo = json_file.read()
        dados = json.loads(conteudo)
    return dados


def atualiza_usuario():
    """
    Menu para solicitar dados do usuário a atualizar
    Outra função é chamada para processar a atualização
    """
    atualiza_id = None
    while atualiza_id is None:
        atualiza_id = input("Insira o ID do usuário (0 para cancelar): ")
        dados = usuarios_json()
        if atualiza_id == '0':
            pass
        elif dados.get(atualiza_id) is None:
            print("Usuário não encontrado!\n")
            atualiza_id = None
        else:
            opcao = 'a'
            while opcao not in ('0', '1', '2', '3'):
                print("Qual informação deseja alterar?\n"\
                      "1 - Nome\n2 - Telefone\n3 - Endereço\n0 - Cancelar")
                opcao = input("Digite a opção desejada: ")

                if opcao == '0':
                    print("Atualização cancelada!")
                elif opcao == '1':
                    print(f"Nome atual: {dados[atualiza_id]['Nome']}")
                    dado_novo = input("Insira o nome atualizado: ")
                    processa_atualizacao_usuario(id=atualiza_id,
                                                 nome=dado_novo)
                    print("Nome atualizado!")
                elif opcao == '2':
                    print(f"Telefone atual: {dados[atualiza_id]['Telefone']}")
                    dado_novo = input("Insira o telefone atualizado: ")
                    processa_atualizacao_usuario(id=atualiza_id,
                                                 telefone=dado_novo)
                    print("Telefone atualizado!")
                elif opcao == '3':
                    print(f"Endereço atual: {dados[atualiza_id]['Endereço']}")
                    dado_novo = input("Insira o endereço atualizado: ")
                    processa_atualizacao_usuario(id=atualiza_id,
                                                 endereco=dado_novo)
                    print("Endereço atualizado!")
                else:
                    print("Opção inválida!\n")
            atualiza_id = None


def busca_usuario(nome: str, telefone: str, endereco: str):
    """
    Verifica se o usuário com determinado nome, telefone e endereço já existe
    Retorna o ID em caso positivo e None caso contrário
    """
    if len(nome) == 0:
        nome = "Não Informado"
    if len(telefone) == 0:
        telefone = "Não Informado"
    if len(endereco) == 0:
        endereco = "Não Informado"
    dict_usuarios = usuarios_json()
    for id, usuario in dict_usuarios.items():
        if all((usuario["Nome"] == nome,
                usuario["Telefone"] == telefone,
                usuario["Endereço"] == endereco)):
            return id
    return None


def processa_atualizacao_usuario(id: str, 
                     nome: str=None,
                     telefone: str=None,
                     endereco: str=None,
                     status: bool=None):
    """
    Atualiza o usuário de ID fornecido com as demais informações fornecidas
    """
    dict_usuarios = usuarios_json()
    if nome is not None:
        dict_usuarios[id]['Nome'] = nome
    
    if telefone is not None:
        dict_usuarios[id]['Telefone'] = telefone
    
    if endereco is not None:
        dict_usuarios[id]['Endereço'] = endereco
    
    if status is not None:
        dict_usuarios[id]['Status'] = status

    with open(arquivo_usuarios(), 'w', encoding='UTF-8') as json_file:
        json_file.write(json.dumps(dict_usuarios, indent=4, ensure_ascii=False))


def insere_usuario():
    """
    Insere um usuário novo ou o reativa caso os dados já existam
    """
    dados = usuarios_json()
    continua_cadastro = True

    while continua_cadastro:
        novo_usuario = {
            "Nome": "Não Informado",
            "Telefone": "Não Informado",
            "Endereço": "Não Informado",
            "Status": True
        }
        novo_nome = input("Digite o nome: ")
        novo_telefone = input("Digite o telefone: ")
        novo_endereco = input("Digite o endereço: ")

        busca_id = busca_usuario(novo_nome, novo_telefone, novo_endereco)

        if busca_id is None:
            novo_id = str(max(map(lambda x: int(x), dados.keys())) + 1)
            if len(novo_nome) > 0:
                novo_usuario['Nome'] = novo_nome

            if len(novo_telefone) > 0:
                novo_usuario['Telefone'] = novo_telefone

            if len(novo_endereco) > 0:
                novo_usuario['Endereço'] = novo_endereco
            
            dados[novo_id] = novo_usuario
            with open(arquivo_usuarios(), 'w', encoding='UTF-8') as json_file:
                json_file.write(json.dumps(dados, indent=4, ensure_ascii=False))
            
            print(f"Novo usuário de ID {novo_id} cadastrado com sucesso!")

        else:
            print(f"Usuário já cadastrado!\nID: {busca_id}\nStatus: [Ativo]")
            processa_atualizacao_usuario(busca_id, status=True)
        
        continua_cadastro = '1' == input("\nDigite 1 para continuar cadastrando: ")

    

def informacoes_usuario():
    """
    Exibe informações de um usuário com base em um ID a ser informado
    """
    usuario = None
    dict_usuarios = usuarios_json()
    while usuario is None:
        id = input("Digite o ID do usuario que deseja informações: ")
        usuario = dict_usuarios.get(id)
        texto = "--------------------------------------------------------------\n"\
                f"---------------- Informações do usuário ID {id} ----------------\n"\
                "--------------------------------------------------------------\n"
        if id == '0':
            pass
        elif usuario is None:
            texto = "Usuário não encontrado!"
        else:
            texto += f"ID:\t\t\t{id}\n"\
                    f"Status:\t\t\t{'Ativo' if usuario['Status'] else 'Inativo'}\n"\
                    f"Nome:\t\t\t{usuario['Nome']}\n"\
                    f"Telefone:\t\t{usuario['Telefone']}\n"\
                    f"Endereço:\t\t{usuario['Endereço']}\n"
        print(texto)


def inativa_usuario():
    """
    Inativa um usuário com base no ID a ser informado
    """
    inativar_id = None
    while inativar_id != '0':
        inativar_id = input("Insira o ID do usuário a inativar (digite 0 para cancelar): ")
        with open(arquivo_usuarios(), 'r', encoding='UTF-8') as json_file:
            conteudo = json_file.read()
            dados = json.loads(conteudo)
        if inativar_id == '0':
            pass
        elif dados.get(inativar_id) is None:
            print("Usuário não encontrado!")
        else:
            processa_atualizacao_usuario(inativar_id, status=False)
            print(f"⚠️  Usuário de ID {inativar_id} Inativado! ⚠️")


def exibe_usuarios_formatado():
    """
    Lista todos os usuarios com informações formatadas na tela
    """
    texto = "--------------------------------------------------------------\n"\
            "------- Abaixo informações dos usuários já cadastrados -------\n"\
            "--------------------------------------------------------------\n"
    for id, dados in usuarios_json().items():
        texto += f"ID:\t\t\t{id}\n"\
                f"Status:\t\t\t{'Ativo' if dados['Status'] else 'Inativo'}\n"\
                f"Nome:\t\t\t{dados['Nome']}\n"\
                f"Telefone:\t\t{dados['Telefone']}\n"\
                f"Endereço:\t\t{dados['Endereço']}\n"
        texto += "= "*32+"\n"
    print(texto)


def finaliza_execucao():
    """
    Dados para exibir ao final da execução do programa
    """
    print("--------------------------------\n"\
          "----- Execução finalizada! -----\n"\
          "--------------------------------")


if __name__ == '__main__':
    main()
