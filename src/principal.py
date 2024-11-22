from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_funcionarios import Constroller_Funcionario
from controller.controller_ponto import Controller_Ponto

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_funcionario = Constroller_Funcionario()
ctrl_ponto = Controller_Ponto()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_funcionario()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_ponto()
    elif opcao_relatorio == 3:
        relatorio.get_relatorio_funcionario_ponto()
    elif opcao_relatorio == 4:
        relatorio.get_relatorio_contagem_ponto()


def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_funcionario = ctrl_funcionario.inserir_funcionario()
    elif opcao_inserir == 2:
        novo_ponto = ctrl_ponto.inserir_data_hora()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_funcionario()
        funcionario_atualizado = ctrl_funcionario.atualizar_funcionario()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_ponto()
        ponto_atualizado = ctrl_ponto.atualizar_ponto()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_funcionario()
        ctrl_funcionario.excluir_funcionario()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_ponto()
        ctrl_ponto.excluir_ponto()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [0-4]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-4]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 0:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()