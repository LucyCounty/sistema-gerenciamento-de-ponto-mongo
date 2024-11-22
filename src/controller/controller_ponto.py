from bson import ObjectId
from reports.relatorios import Relatorio
from model.ponto import Ponto
from model.funcionarios import Funcionarios
from controller.controller_funcionarios import Constroller_Funcionario
from conexion.mongo_queries import MongoQueries
from datetime import date
from datetime import datetime
import pandas as pd

class Controller_Ponto:
    def __init__(self):
        self.ctrl_funcionario = Constroller_Funcionario()
        self.ctrl_ponto = Controller_Ponto
        self.mongo = MongoQueries()
        self.relatorio = Relatorio()

    def inserir_data_hora(self) -> Ponto:
        self.mongo.connect()
        responder_novamente = 's'

        while(responder_novamente.lower() == 's'):
            self.relatorio.get_relatorio_funcionario()
            cpf = str(input("Digite o CPF do funcionario: "))
            funcionarios = self.valida_funcionario(cpf)
            if funcionarios == None:
                return None
            
            data_hoje = datetime.today().strftime("%d-%m-%Y %H:%M")
            proximo_ponto = self.mongo.db["ponto"].aggregate([{
                '$group': {
                    '_id': '$ponto',
                    'proximo_ponto': {
                        '$max': '$codigo_ponto'
                    }
                }
            }, {
                '$project': {
                    'proximo_ponto': {
                        '$sum': [
                            '$proximo_ponto', 1
                        ]
                    },
                    '_id': 0
                }
            }])

            proximo_ponto = int(list(proximo_ponto)[0]['proximo_ponto'])
            data = dict(codigo_ponto=proximo_ponto, data_hora=data_hoje, cpf=funcionarios.get_CPF())
            id_ponto = self.mongo.db["ponto"].insert_one(data)
            df_ponto = self.recupera_ponto(id_ponto.inserted_id)
            novo_ponto = Ponto(df_ponto.codigo_ponto.values[0], pd.to_datetime(str(df_ponto.data_hora.values[0])), funcionarios)
            print(novo_ponto.to_string())

            responder_novamente = input('Você deseja adicionar mais um ponto? [S ou N]: ')
            while(responder_novamente.lower() != 's' and responder_novamente.lower() != 'n'):
                responder_novamente = input('A opção "'+ responder_novamente +'" não existe. Você deseja adicionar mais um ponto? [S ou N]: ')
            if (responder_novamente.lower() == 'n'):
                self.mongo.close()
                return novo_ponto
    
    def atualizar_ponto(self) -> Ponto:
        self.mongo.connect()
        responder_novamente = 's'

        while(responder_novamente.lower() == 's'):
            codigo_ponto = int(input("Código do horário do ponto que irá alterar: "))

            if not self.verifica_existencia_ponto(codigo_ponto):
                data_str = input("Digite uma data (DD/MM/YYYY hh:mm): ")
                nova_data_hora = datetime.strptime(data_str,"%d/%m/%Y %H:%M")

                self.mongo.db["ponto"].update_one({"codigo_ponto": codigo_ponto},
                                                  {"$set": {"data_hora": nova_data_hora}})

                df_ponto = self.recupera_ponto_codigo(codigo_ponto)
                funcionario = self.valida_funcionario(df_ponto.cpf.values[0])
                data_atualizada = Ponto(df_ponto.codigo_ponto.values[0], pd.to_datetime(str(df_ponto.data_hora.values[0])), funcionario)

                print(data_atualizada.to_string())
                responder_novamente = input('Deseja atualizar mais algum ponto? [S ou N]: ')
                while(responder_novamente.lower() != 's' and responder_novamente.lower() != 'n'):
                    responder_novamente = input('A opção "'+ responder_novamente +'" não existe. Deseja realizar atualizar mais algum ponto? [S ou N]: ')
                if (responder_novamente.lower() == 'n'):
                    self.mongo.close()
                    return data_atualizada
            else:
                self.mongo.close()
                print(f'O código {codigo_ponto} não existe.')
                return None

    def excluir_ponto(self):
        self.mongo.connect()
        responder_novamente = 's'

        while(responder_novamente.lower() == 's'):
            codigo_ponto = int(input("Digite o código do ponto que irá excluir: "))

            if not self.verifica_existencia_ponto(codigo_ponto):
                df_ponto = self.recupera_ponto_codigo(codigo_ponto)
                funcionario = self.valida_funcionario(df_ponto.cpf.values[0])
                opcao_excluir = input(f"Tem certeza que deseja excluir o ponto {codigo_ponto} [S ou N]: ")

                while(opcao_excluir.lower() != 's' and opcao_excluir.lower() != 'n'):
                    opcao_excluir = input(f'A opção "{opcao_excluir}" não existe. Tem certeza que deseja excluir o ponto {codigo_ponto} [S ou N]: ')
                if (opcao_excluir.lower() == "s"):
                    self.mongo.db["ponto"].delete_one({"codigo_ponto": codigo_ponto})
                    # Cria um novo objeto Produto para informar que foi removido
                    ponto_excluido = Ponto(df_ponto.codigo_ponto.values[0], pd.to_datetime(str(df_ponto.data_hora.values[0])), funcionario)
                    # Exibe os atributos do produto excluído
                    print("Ponto removido com sucesso!")
                    print(ponto_excluido.to_string())

                    responder_novamente = input('Deseja remover mais um ponto? [S ou N]: ')
                    while(responder_novamente.lower() != 's' and responder_novamente.lower() != 'n'):
                        responder_novamente = input('A opção "'+ responder_novamente +'" não existe. Você deseja remover mais um ponto? [S ou N]: ')
                    if(responder_novamente.lower() == 'n'):
                        self.mongo.close()

                elif (opcao_excluir.lower() == 'n'):
                    responder_novamente = opcao_excluir
                    self.mongo.close()
                    print('Remoção do ponto do funcionário "' + str(codigo_ponto) + '" cancelada.')
            else:
                self.mongo.close()
                print(f'O código "{codigo_ponto}" não existe.')
                return None

    def verifica_existencia_ponto(self, codigo:int=None, external: bool = False) -> bool:
        df_ponto = self.recupera_ponto_codigo(codigo=codigo, external=external)
        return df_ponto.empty

    def recupera_ponto(self, _id:ObjectId=None) -> bool:
        df_ponto = pd.DataFrame(list(self.mongo.db["ponto"].find({"_id": _id}, {"codigo_ponto": 1, "data_hora": 1, "cpf": 1, "_id": 0})))
        return df_ponto

    def recupera_ponto_codigo(self, codigo:int=None, external: bool = False) -> bool:
        if external:
            # Cria uma nova conexão com o banco que permite alteração
            self.mongo.connect()
        
        df_ponto = pd.DataFrame(list(self.mongo.db["ponto"].find({"codigo_ponto": codigo}, {"codigo_ponto": 1, "data_hora": 1, "cpf": 1, "_id": 0})))
        
        if external:
            # Fecha a conexão com o Mongo
            self.mongo.close()

        return df_ponto

    def valida_funcionario(self, cpf:str=None) -> Funcionarios:
        if self.ctrl_funcionario.verifica_existencia_funcionario(cpf, external=True):
            print(f'O CPF "{cpf}" informada não existe')
            return None
        else:
            df_funcionario = self.ctrl_funcionario.recupera_funcionario(cpf, external=True)
            funcionarios = Funcionarios(df_funcionario.cpf.values[0], df_funcionario.nome.values[0], df_funcionario.cargo.values[0])
            return funcionarios
        
    def valida_ponto(self, codigo_ponto:int=None) -> Ponto:
        if self.ctrl_ponto.verifica_existencia_ponto(codigo_ponto, external=True):
            print(f"O código do ponto {codigo_ponto} informado não existe.")
        else:
            df_ponto = self.ctrl_ponto.recupera_ponto_codigo(codigo_ponto, external=True)
            funcionario = self.valida_funcionario(df_ponto.cpf.values[0])
            ponto = Ponto(df_ponto.codigo_ponto.values[0], df_ponto.data_hora.values[0], funcionario)
            return ponto