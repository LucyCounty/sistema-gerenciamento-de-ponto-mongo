from conexion.mongo_queries import MongoQueries
import pandas as pd
from pymongo import ASCENDING, DESCENDING

class Relatorio:
    def __init__(self):
        pass

    def get_relatorio_funcionario(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["funcionarios"].find({},
                                                    {"cpf": 1,
                                                    "nome": 1,
                                                    "cargo": 1,
                                                    "_id": 0
                                                    }).sort("nome", ASCENDING)
        df_funcionarios = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_funcionarios)
        input('Pressione "Enter" para sair do relatório de funcionários.')

        """select f.cpf
        ,  f.nome
        ,  f.cargo
        from funcionarios f
        order by f.nome"""


    def get_relatorio_ponto(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db["ponto"].aggregate([{
                                                    '$lookup':{'from':'funcionarios',
                                                            'localField':'cpf',
                                                            'foreignField':'cpf',
                                                            'as':'funcionario'
                                                            }
                                                },
                                                {
                                                    '$unwind':{"path": "$funcionario"}
                                                },
                                                {'$project':{'codigo_ponto': 1,
                                                            'data_hora': {'$dateToString': {'format': '%d/%m/%Y %H:%M', 'date': {'$toDate': '$data_hora'}}},
                                                            'funcionario': '$funcionario.nome',
                                                            '_id': 0}}, {
                                                                '$sort': {
                                                                    'codigo_ponto': 1
                                                                }
                                                            }
                                                    ])
        df_ponto = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_ponto)
        input('Pressione "Enter" para sair do relatório de ponto.')

        """select p.codigo_ponto
            ,  TO_CHAR(p.data_hora, 'DD/MM/YYYY HH24:MI') as data_hora
            ,  f.nome as funcionarios
            from ponto p
            inner join funcionarios f
            on p.cpf = f.cpf
            order by p.codigo_ponto
        """


    def get_relatorio_funcionario_ponto(self):
        mongo = MongoQueries()
        mongo.connect()

        query_result = mongo.db["ponto"].aggregate([{
            '$lookup': {
                'from': 'funcionarios',
                'localField': 'cpf',
                'foreignField': 'cpf',
                'as': 'funcionario'
            }
        },
        {
            '$unwind': '$funcionario'
        },
        {
            '$project': {
                'codigo_ponto': 1,
                'cpf': '$cpf',
                'nome': '$funcionario.nome',
                'cargo': '$funcionario.cargo',
                'data_hora': {'$dateToString': {'format': '%d/%m/%Y %H:%M', 'date': {'$toDate': '$data_hora'}}},
                '_id': 0}}, {
                    '$sort': {
                        'codigo_ponto': 1
            }
        }])
        df_funcionario_ponto = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_funcionario_ponto)
        input('Pressione "Enter" para sair do relatório de funcionários com ponto.')

    """with sumariza_funcionarios as (
        select f.cpf
            ,  f.nome
            ,  f.cargo
            from funcionarios f
            order by f.nome
    )

    select p.codigo_ponto as codigo_ponto
        ,  sf.cpf
        ,  sf.nome
        ,  sf.cargo
        ,  TO_CHAR(p.data_hora, 'DD/MM/YYYY HH24:MI') as data_hora
        from ponto p
        inner join sumariza_funcionarios sf
        on p.cpf = sf.cpf
        order by p.codigo_ponto"""


    def get_relatorio_contagem_ponto(self):
        mongo = MongoQueries()
        mongo.connect()
        query_result = mongo.db['ponto'].aggregate([{
            '$lookup': {
                'from': 'funcionarios',
                'localField': 'cpf',
                'foreignField': 'cpf',
                'as': 'funcionario'
            }
        }, {
            '$unwind': {
                'path': '$funcionario'
            }
        }, {
            '$project': {
                'codigo_ponto': 1,
                'data_hora': {'$dateToString': {'format': '%d/%m/%Y %H:%M', 'date': {'$toDate': '$data_hora'}}},
                'cpf': 1,
                'nome': '$funcionario.nome',
                'cargo': '$funcionario.cargo',
                '_id': 0
            }
        }, {
            '$group': {
                '_id': {'nome': '$nome', 'cargo': '$cargo'},
                'contagem': {'$sum': 1}
            }
        }, {
            '$project': {
                'nome': '$_id.nome',
                'cargo': '$_id.cargo',
                'contagem': 1,
                '_id': 0
            }
        }, {
            '$sort': {'nome': 1}
        }])
        df_contagem_ponto = pd.DataFrame(list(query_result))
        mongo.close()
        print(df_contagem_ponto[['nome', 'cargo', 'contagem']])
        input('Pressione "Enter" para sair do relatório de contagem de ponto.')

    """WITH sumariza_funcionarios AS (
        SELECT p.codigo_ponto,
            TO_CHAR(p.data_hora, 'DD/MM/YYYY HH24:MI') AS data_hora,
            f.cpf
        FROM ponto p
        INNER JOIN funcionarios f ON p.cpf = f.cpf
        ORDER BY p.codigo_ponto
    )

    SELECT f.nome AS funcionarios,
        COUNT(1) AS contagem,
        f.cargo AS cargo
    FROM funcionarios f
    INNER JOIN sumariza_funcionarios sp ON f.cpf = sp.cpf
    GROUP BY f.nome, f.cargo
    ORDER BY f.nome"""