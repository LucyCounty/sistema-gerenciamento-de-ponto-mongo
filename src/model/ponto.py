from model.funcionarios import Funcionarios
from datetime import datetime

class Ponto:
    def __init__(self, 
                 codigo_ponto:int=None, 
                 data_hora:datetime=None,
                 funcionarios:Funcionarios=None
                ):
        self.set_codigo_ponto(codigo_ponto)
        self.set_data_hora(data_hora)
        self.set_funcionarios(funcionarios)

    def set_codigo_ponto(self, codigo_ponto:int):
        self.codigo_ponto = codigo_ponto

    def set_data_hora(self, data_hora:datetime):
        self.data_hora = data_hora

    def set_funcionarios(self, funcionarios:Funcionarios):
        self.funcionarios = funcionarios

    def get_codigo_ponto(self) -> int:
        return self.codigo_ponto
    
    def get_data_hora(self) -> datetime:
        return self.data_hora.strftime("%d/%m/%Y %H:%M")
    
    def get_funcionarios(self) -> Funcionarios:
        return self.funcionarios

    def to_string(self) -> str:
        return f"Codigo_ponto: {self.get_codigo_ponto()} | Data_hora: {self.get_data_hora()} | Funcionarios: {self.get_funcionarios().get_nome()}"