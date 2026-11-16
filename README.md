# Atividade individual 1 · Serverless (Rota Vital)

Infraestrutura de Software · ADS · CESAR School · 2026.2
Aluno: Conolly (preencher nome completo)

## Caminho escolhido
Caminho A: AWS SAM CLI local (Docker Desktop + SAM CLI 1.172.1 + Python 3.12 dentro do container).

O PC tem Python 3.13, então o `sam build` local falhou ("Binary validation failed for python... runtime python3.12"). Resolvi usando `sam build --use-container`, que faz o build dentro do container com Python 3.12.

## Estrutura
```
template.yaml          # API POST /guias, Timeout em Globals
hello_world/app.py     # handler que gera a guia de transporte
events/pedido.json     # evento da API Gateway (POST /guias)
tests/test_app.py      # testes do handler (pytest)
evidencias/            # prints dos comandos e saídas
```

## Como rodar
Pré-requisitos: Docker Desktop aberto (Engine running), SAM CLI e Git.

```powershell
sam build --use-container

sam local invoke -e events/pedido.json
sam local invoke -e events/pedido.json

sam local start-api
curl.exe -X POST http://127.0.0.1:3000/guias -H "Content-Type: application/json" -d "@r2.json"

sam local start-api --warm-containers LAZY

curl.exe -i -X POST http://127.0.0.1:3000/guias -H "Content-Type: application/json" -d "@r3.json"
```
Corpos usados nos `curl.exe` (arquivos criados com `Set-Content`):
- `r2.json`: `{"requisicaoId":"R-002","hospital":"H-Caruaru"}`
- `r3.json`: `{"requisicaoId":"R-003","demorar":true}`

Testes do handler sem Docker: `pip install pytest && python -m pytest`.

## Resultados dos experimentos

### Invocação com evento (Passo 3)
| Invocação | Duration | Billed | invocacaoNesteAmbiente |
|---|---|---|---|
| 1ª | 406,02 ms | 407 ms | 1 |
| 2ª | 77,49 ms | 78 ms | 1 |

O `Init Duration` ficou em 0,06 ms e 0,03 ms. O emulador local não reproduz o Init real da nuvem, então esses valores não representam um cold start de verdade.

Evidência: `evidencias/01-invoke-evento-duas-vezes.jpeg`

### Chamada HTTP (Passo 4)
| Modo | Chamada 1 | Chamada 2 | Chamada 3 | Container |
|---|---|---|---|---|
| `start-api` padrão | contador 1 (1173,55 ms) | contador 1 (91,12 ms) | contador 1 (128,62 ms) | um novo a cada chamada |
| `--warm-containers LAZY` | contador 1 (651,15 ms) | contador 2 (4,63 ms) | contador 3 (2,91 ms) | o mesmo |

Repetindo mais 3 chamadas com `LAZY`, o contador seguiu 4, 5 e 6 (2 a 5 ms cada).

Evidências:
- `evidencias/02-start-api-log.jpeg`
- `evidencias/03-start-api-curl.jpeg`
- `evidencias/04-warm-containers-curl.jpeg`
- `evidencias/05-warm-containers-log.jpeg`

### Limite de tempo (Passo 5)
- Timeout 3 s: o servidor registrou `Function 'GuiaFunction' timed out after 3 seconds` (Duration 3000 ms). O cliente recebeu `HTTP/1.1 502 BAD GATEWAY` com `{"message":"Internal server error"}`.
- Timeout 10 s (ajuste no `template.yaml`, depois `sam build --use-container`): a mesma chamada retornou `HTTP/1.1 201 CREATED` com a guia `G-R-003`, Duration 5314,19 ms (Billed 5315 ms).

Evidências:
- `evidencias/06-timeout-3s-curl.jpeg`
- `evidencias/07-timeout-3s-log.jpeg`
- `evidencias/08-timeout-10s-curl.jpeg`
- `evidencias/09-timeout-10s-log.jpeg`

## Respostas

> Escrever com as suas palavras. Os dados medidos estão listados em cada pergunta; as dicas e esta frase devem ser apagadas antes de entregar.

### 1. Por que a primeira invocação demorou mais que a segunda? O que acontece na fase de Init?
Dados: 1ª invocação 406,02 ms; 2ª 77,49 ms. No `start-api`, a 1ª chamada levou 1173,55 ms.

_Dica: pense no que precisa existir antes do handler rodar pela primeira vez (ambiente, código, runtime) e no que o ambiente guarda depois._

Minha resposta: ___

### 2. O que o campo invocacaoNesteAmbiente mostrou com e sem --warm-containers? O que isso diz sobre estado em variável global?
Dados: sem `--warm-containers` o campo foi 1, 1, 1 (container novo a cada chamada). Com `LAZY` foi 1, 2, 3, 4, 5, 6 (mesmo container).

_Dica: o que decide se o contador continua ou volta para 1? Dá para confiar nisso na nuvem?_

Minha resposta: ___

### 3. O que aconteceu com demorar = true? Qual o tempo máximo de uma execução no Lambda e o que fazer com um trabalho mais longo?
Dados: com Timeout 3 s, erro `timed out after 3 seconds` e HTTP 502. Com Timeout 10 s, HTTP 201 em 5314,19 ms.

_Dica: confira o limite na página de cotas do Lambda (link no PDF) e pense em alternativas para trabalho longo (fila, divisão do trabalho, outro serviço)._

Minha resposta: ___

### 4. Custo de 1 milhão de execuções (128 MB, 100 ms, us-east-1)
_Dica: separe em duas parcelas, requisições e computação. Converta MB para GB e ms para s antes de multiplicar pelo número de execuções, e some no final. Mostre a conta passo a passo._

- Requisições: ___
- Computação (GB-s): ___
- Total: ___

### 5. Onde uma função assim faria sentido no Rota Vital e onde não faria?
_Dica: pense em carga que aparece em picos, curta e sem estado, versus tarefas contínuas, longas ou que dependem de estado ou conexão aberta._

Minha resposta: ___

## Uso de IA
(PO-CESAR-021)

- **Ferramenta:** Claude (Anthropic)
- **Finalidade:** montar a estrutura do repositório, o modelo de README e os testes do handler; orientar a configuração do ambiente (Docker/WSL, SAM) e a leitura das saídas dos comandos.
- **Como validei:** executei todos os comandos no meu computador, conferi as saídas e os tempos, anexei os prints em `evidencias/`, rodei os testes com `pytest` e escrevi as respostas com minhas palavras. (ajustar se algo for diferente)
