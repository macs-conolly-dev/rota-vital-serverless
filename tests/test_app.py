import json
import pytest
from hello_world import app


@pytest.fixture(autouse=True)
def zerar_contador():
    app.contador = 0


def chamar(corpo):
    return app.lambda_handler({"body": json.dumps(corpo)}, None)


def test_cria_guia():
    resposta = chamar({"requisicaoId": "R-001", "hospital": "H-Recife", "bolsas": ["O-NEG-0142"]})
    assert resposta["statusCode"] == 201
    assert json.loads(resposta["body"])["guia"] == "G-R-001"


def test_sem_requisicao_id_retorna_400():
    assert chamar({"hospital": "H-Recife"})["statusCode"] == 400


def test_contador_cresce_no_mesmo_ambiente():
    chamar({"requisicaoId": "R-1"})
    resposta = chamar({"requisicaoId": "R-2"})
    assert json.loads(resposta["body"])["invocacaoNesteAmbiente"] == 2
