import pandas as pd
from model.funcionarios import Funcionarios
from conexion.mongo_queries import MongoQueries

class Constroller_Funcionario:
    def __init__(self):
        self.mongo = MongoQueries()

    def inserir_funcionario(self) -> Funcionarios:
        self.mongo.connect()
        responder_novamente = 's'

        while(responder_novamente.lower() == 's'):
            cpf = str(input("CPF (Novo): "))
            if self.verifica_existencia_funcionario(cpf):
                nome = input("Nome: ")
                cargo = input("Cargo: ")

                self.mongo.db["funcionarios"].insert_one({"cpf": cpf, "nome": nome, "cargo": cargo})
                df_funcionarios = self.recupera_funcionario(cpf)
                novo_funcionario = Funcionarios(df_funcionarios.cpf.values[0], df_funcionarios.nome.values[0], df_funcionarios.cargo.values[0])
                print(novo_funcionario.to_string())

                responder_novamente = input('Você deseja adicionar mais um funcionário? [S ou N]: ')
                while(responder_novamente.lower() != 's' and responder_novamente.lower() != 'n'):
                    responder_novamente = input('A opção "'+ responder_novamente +'" não existe. Você deseja adicionar mais um funcionário? [S ou N]: ')
                if (responder_novamente.lower() == 'n'):
                    self.mongo.close()
                    return novo_funcionario

            else:
                self.mongo.close()
                print(f'O CPF "{cpf}" já está cadastrada.')
                return None

    def atualizar_funcionario(self) -> Funcionarios:
        self.mongo.connect() 
        responder_novamente = 's'

        while(responder_novamente.lower() == 's'):
            cpf = str(input("Digite a CPF do funcionario no qual deseja alterar algo: "))

            if not self.verifica_existencia_funcionario(cpf):
                escolher_opcao = input('Escolha o que você deseja alterar [N = Nome ou C = Cargo]: ')
                while(escolher_opcao.lower() != 'n' and escolher_opcao.lower() != 'c'):
                    escolher_opcao = input('A opção "' + escolher_opcao  + '" não existe. Escolha o que você deseja alterar [N = Nome ou C = Cargo]: ')
                if (escolher_opcao.lower() == 'n'):
                    novo_nome = input("Nome: ")
                    self.mongo.db["funcionarios"].update_one({"cpf": f"{cpf}"}, {"$set": {"nome": novo_nome}})
                elif (escolher_opcao.lower() == 'c'):
                    novo_cargo = input("Cargo: ")
                    self.mongo.db["funcionarios"].update_one({"cpf": f"{cpf}"}, {"$set": {"cargo": novo_cargo}})

                df_funcionarios = self.recupera_funcionario(cpf)
                funcionario_atualizado = Funcionarios(df_funcionarios.cpf.values[0], df_funcionarios.nome.values[0], df_funcionarios.cargo.values[0])
                print(funcionario_atualizado.to_string())

                responder_novamente = input('Deseja realizar atualizar mais algum funcionario? [S ou N]: ')
                while (responder_novamente.lower() != 's' and responder_novamente.lower() != 'n'):
                    responder_novamente = input('A opção "'+ responder_novamente +'" não existe. Deseja realizar atualizar mais algum funcionario? [S ou N]: ')
                if (responder_novamente.lower() == 'n'):
                    self.mongo.close()
                    return funcionario_atualizado
            else:
                self.mongo.close()
                print(f'O CPF "{cpf}" não existe.')
                return None

    def excluir_funcionario(self):
        self.mongo.connect()
        responder_novamente = 's'

        while(responder_novamente.lower() == 's'):
            cpf = str(input("CPF do funcionario que irá remover: "))

            if not self.verifica_existencia_funcionario(cpf):
                opcao_excluir = input(f"Tem certeza que deseja remover o funcionário com o CPF {cpf} [S ou N]: ")

                while (opcao_excluir.lower() != 's' and opcao_excluir.lower() != 'n'):
                    opcao_excluir = input(f'A opção "{opcao_excluir}" não existe. Tem certeza que deseja remover o funcionário com o CPF {cpf} [S ou N]: ')
                if (opcao_excluir.lower() == 's'):
                    print(f"Atenção, caso possua horários de ponto, também serão excluídos!")
                    opcao_excluir = input(f"Tem certeza que deseja remover o funcionário com o CPF {cpf} [S ou N]: ")
                    
                    while (opcao_excluir.lower() != 's' and opcao_excluir.lower() != 'n'):
                        opcao_excluir = input(f'A opção "{opcao_excluir}" não existe. Tem certeza que deseja remover o funcionário com o CPF {cpf} [S ou N]: ')
                    if (opcao_excluir.lower() == 's'):
                        df_funcionarios = self.recupera_funcionario(cpf)

                        self.mongo.db["ponto"].delete_many({"cpf": f"{cpf}"})

                        print('Ponto removido com sucesso!')
                        self.mongo.db["funcionarios"].delete_one({"cpf": f"{cpf}"})
                        funcionario_excluido = Funcionarios(df_funcionarios.cpf.values[0], df_funcionarios.nome.values[0], df_funcionarios.cargo.values[0])

                        print("Funcionario removido com sucesso!")
                        print(funcionario_excluido.to_string())

                        responder_novamente = input('Deseja remover mais um funcionário? [S ou N]: ')
                        while(responder_novamente.lower() != 's' and responder_novamente.lower() != 'n'):
                            responder_novamente = input('A opção "'+ responder_novamente +'" não existe. Você deseja remover mais um funcionário? [S ou N]: ')
                        if(responder_novamente.lower() == 'n'):
                            self.mongo.close()
                    elif (opcao_excluir.lower() == 'n'):
                        responder_novamente = opcao_excluir
                        self.mongo.close()
                        print('Remoção do funcionário: "' + cpf + '" cancelada.')
                elif (opcao_excluir.lower() == 'n'):
                    responder_novamente = opcao_excluir
                    self.mongo.close()
                    print('Remoção do funcionário: "' + cpf + '" cancelada.')
            else:
                self.mongo.close()
                print(f'O CPF "{cpf}" não existe.')
                return None

    def verifica_existencia_funcionario(self, cpf:str=None, external:bool=False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo cliente criado transformando em um DataFrame
        df_cliente = pd.DataFrame(self.mongo.db["funcionarios"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "cargo": 1, "_id": 0}))

        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente.empty

    def recupera_funcionario(self, cpf:str=None, external:bool=False) -> pd.DataFrame:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()

        # Recupera os dados do novo funcionario criado transformando em um DataFrame
        df_cliente = pd.DataFrame(list(self.mongo.db["funcionarios"].find({"cpf":f"{cpf}"}, {"cpf": 1, "nome": 1, "cargo": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_cliente