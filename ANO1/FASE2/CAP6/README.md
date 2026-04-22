# Sistema de Gestão de Produção e Perdas — Cana-de-Açúcar

> **FIAP — Fase 2 — Capítulo 6**
> Domínio escolhido: **agronegócio sucroalcooleiro** (produção e perdas na colheita de cana-de-açúcar).

---

## 1. A "dor" do agronegócio tratada

O Brasil é líder mundial na produção de cana-de-açúcar, colhendo mais de **620 milhões de toneladas** por safra. Apesar do recorde, a colheita mecanizada perde até **15%** da produção — contra apenas **~5%** da colheita manual. Segundo estudos do setor, considerando uma produtividade média de 100 t/ha em aproximadamente 3 milhões de hectares em São Paulo, essa diferença representa cerca de **R$ 20 milhões/ano** em prejuízo só no estado.

Esse projeto ataca exatamente essa dor: **dar ao produtor rural uma ferramenta simples para registrar cada lote colhido, calcular o prejuízo em reais, comparar com o benchmark do setor e identificar em quais fazendas ou tipos de colheita ele está perdendo mais dinheiro**.

---

## 2. Funcionalidades

| # | Opção | O que faz |
|---|---|---|
| 1 | Cadastrar produção | Registra um lote (fazenda, toneladas, % perda, tipo de colheita) com validação de entrada |
| 2 | Listar produções | Mostra todos os registros em tabela formatada com prejuízo em R$ e totais agregados |
| 3 | Apagar registro | Remove um lote pelo ID |
| 4 | Exportar JSON | Salva todos os registros em `producao.json` |
| 5 | Exportar relatório TXT | Gera `relatorio.txt` com tabela legível |
| 6 | Resumo por tipo de colheita | Compara perda média com o benchmark do setor (5% manual / 15% mecanizada) e emite alerta quando está acima |

---

## 3. Como rodar

> **Nota sobre a infraestrutura de banco.** A proposta inicial desta atividade previa o uso do **Oracle institucional da FIAP** (`oracle.fiap.com.br:1521/ORCL`). Contudo, o usuário e a senha fornecidos para o grupo **não autenticaram** — todas as tentativas de conexão retornaram falha de credencial. Para não bloquear a entrega, optamos por disponibilizar uma **estrutura opcional via Docker**, que sobe um `Oracle Database Free` local funcionalmente equivalente. O código em `main.py` é agnóstico: roda igual nos dois ambientes, bastando ajustar as variáveis de ambiente. Caso as credenciais institucionais sejam regularizadas, veja a seção **"Alternativa — Oracle da FIAP"** no final deste capítulo.

### Pré-requisitos

- Python 3.10 ou superior
- [Docker Desktop](https://www.docker.com/products/docker-desktop)
- ~15 GB livres em disco (imagem Oracle + volume de dados)
- ~2 GB de RAM alocados ao Docker

### Passo 1 — Instalar dependência Python

```bash
pip install -r requirements.txt
```

### Passo 2 — Subir o banco Oracle local

```bash
docker compose up -d
```

A **primeira inicialização demora 5–10 minutos** (download da imagem + criação do banco). Acompanhe com:

```bash
docker compose logs -f oracle
```

Quando aparecer **`DATABASE IS READY TO USE!`**, está pronto. O script `setup_db.sql` já criou automaticamente o usuário dedicado `fiap`.

### Passo 3 — Configurar variáveis de ambiente

O projeto traz um **`.env.example`** com as duas opções já pré-configuradas (Docker local e Oracle da FIAP). Basta copiar para `.env` e ajustar:

```bash
cp .env.example .env
```

O `main.py` carrega o `.env` automaticamente na inicialização via `python-dotenv` (instalado pelo `requirements.txt`). O arquivo `.env` está no `.gitignore` da raiz do repositório, então **suas credenciais reais nunca são commitadas**.

Se preferir exportar as variáveis diretamente no shell em vez de usar `.env`, também funciona:

```bash
export ORACLE_USER=fiap
export ORACLE_PASSWORD=fiap123
export ORACLE_DSN=localhost:1521/FREEPDB1
```

### Passo 4 — Executar o programa

```bash
python main.py
```

Na primeira execução o programa cria automaticamente a tabela `producao`. A partir daí, o menu está pronto para uso.

### Comandos úteis do Docker

```bash
docker compose stop       # pausar (mantém os dados)
docker compose start      # religar
docker compose down       # parar e remover container (mantém o volume)
docker compose down -v    # zerar tudo, inclusive os dados
```

### Alternativa — Oracle da FIAP (plano original)

Esta era a infraestrutura **originalmente planejada** para a atividade. Como registrado na nota no início desta seção, as credenciais fornecidas pelo portal não autenticaram no servidor `oracle.fiap.com.br:1521/ORCL` no momento da entrega. Assim que a liberação for regularizada, basta ajustar o `.env` — **sem qualquer alteração no código**:

```env
# .env
ORACLE_USER=rmXXXXXX
ORACLE_PASSWORD=sua_senha
ORACLE_DSN=oracle.fiap.com.br:1521/ORCL
```

O próprio `.env.example` já traz essas três linhas comentadas para facilitar a troca.

O `python-oracledb` em modo thin funciona igualmente nos dois ambientes (Docker local ou Oracle da FIAP), portanto a solução permanece 100% aderente ao requisito acadêmico de "Conexão com banco de dados: Oracle".

---

## 4. Estrutura do projeto

```
project-6/
├── main.py              # aplicação completa (menu + banco + regras + I/O)
├── requirements.txt     # dependência oracledb
├── docker-compose.yml   # sobe o Oracle Database Free local
├── setup_db.sql         # provisiona o usuário fiap na PDB FREEPDB1
└── README.md            # este arquivo
```

O `main.py` está organizado em seções explícitas, na ordem em que a aplicação executa:

1. Constantes do domínio (preço da tonelada, benchmarks do setor)
2. Camada de banco Oracle (`connect`, `create_table`, `insert_record`, `fetch_all_records`, `delete_record`)
3. Tabela de memória (cache em RAM dos registros lidos)
4. Regras de negócio (`calculate_loss`, `benchmark_message`)
5. Validação de entrada (`read_text`, `read_float`, `read_int`, `read_choice`)
6. Manipulação de arquivos (`export_json`, `export_txt`)
7. Apresentação (`print_records_table`)
8. Ações do menu
9. Loop principal

---

## 5. Requisitos acadêmicos atendidos

Mapeamento direto dos conteúdos exigidos pelos capítulos 3 a 6 da disciplina para o código entregue:

| Requisito | Onde está no código |
|---|---|
| **Subalgoritmos — função com parâmetros** | `calculate_loss(tons, loss_pct)`, `read_float(prompt, *, minimum, maximum)`, `benchmark_for(harvest_type)` |
| **Subalgoritmos — procedimento** (sem retorno) | `create_table()`, `insert_record(...)`, `print_records_table(records)` |
| **Estrutura: lista** | `_memory_table: list[dict]`, `lines` em `export_txt` |
| **Estrutura: tupla** | `HARVEST_TYPES = ("manual", "mecanizada")`, retorno de `cursor.fetchall()` |
| **Estrutura: dicionário** | cada registro (`{"id": ..., "farm": ..., ...}`), dicionário `actions` mapeando opções do menu → funções |
| **Tabela de memória** | `_memory_table` — cache em RAM populado por `refresh_memory_table()`, usado pelo resumo e pela exportação |
| **Manipulação de arquivo texto** | `export_txt()` → gera `relatorio.txt` |
| **Manipulação de arquivo JSON** | `export_json()` → gera `producao.json` |
| **Conexão com banco de dados Oracle** | `connect()` usando `python-oracledb` em modo thin + `docker-compose.yml` com Oracle Database Free 23ai |

### Critérios de avaliação cobertos

- **Linha lógica clara**: escopo único (perdas na colheita de cana), fluxo linear de menu, arquivo com seções comentadas.
- **Relevância com o enunciado**: agronegócio, cana-de-açúcar, perdas na colheita mecanizada — tema central do capítulo.
- **Inovação**:
  - Conversão automática de perda em **R$** usando preço-referência da tonelada.
  - **Comparação automática** da perda registrada com o benchmark do setor (5% manual / 15% mecanizada) e alerta quando ultrapassado.
  - **Resumo agregado** por tipo de colheita mostrando prejuízo total, perda média e status vs. benchmark.
- **Consistência de entrada**: toda leitura passa por `read_text`, `read_float`, `read_int` ou `read_choice`, que rejeitam tipos inválidos, valores fora do intervalo e strings vazias — o usuário fica preso no loop até digitar algo válido.
- **Apresentação limpa**: tabelas alinhadas com larguras fixas, totais agregados no rodapé, formatação `R$ 11,234.56` para moeda, alertas com prefixo `OK:` / `ALERTA:`.

---

## 6. Exemplo de uso

### Cadastro com validação rejeitando entrada inválida

```
--- Cadastrar producao ---
  Nome da fazenda: Sao Martinho
  Producao (toneladas): abc
  Erro: digite apenas numeros (ex.: 1234.56).
  Producao (toneladas): 15000
  Perda (%): 150
  Erro: o valor deve estar entre 0.0 e 100.0.
  Perda (%): 18.5
  Tipo de colheita (manual/mecanizada): mec
  Erro: escolha uma das opcoes: manual/mecanizada.
  Tipo de colheita (manual/mecanizada): mecanizada

  Registro salvo. Perda calculada: 2775.00 t (R$ 333,000.00)
  ALERTA: perda 3.5 p.p. acima do benchmark (15.0%) para colheita mecanizada.
```

### Listagem formatada

```
   ID | Fazenda                   |       Tons |  Perda% |  Perda(t) |     Perda(R$) | Tipo
  ------------------------------------------------------------------------------------------------
    1 | Sao Martinho              |   15000.00 |  18.50% |   2775.00 | R$  333,000.00 | mecanizada
    2 | Usina Iracema             |    8000.00 |   4.20% |    336.00 | R$   40,320.00 | manual
    3 | Fazenda Boa Vista         |   22000.00 |  12.00% |   2640.00 | R$  316,800.00 | mecanizada
  ------------------------------------------------------------------------------------------------
  TOTAIS:   45000.00 t produzidas  |    5751.00 t perdidas  |  R$  690,120.00 de prejuizo
```

### Resumo por tipo de colheita

```
--- Resumo por tipo de colheita ---

  Colheita manual:
    Registros:      1
    Perda media:    4.20%  (benchmark do setor: 5.0% -> DENTRO)
    Prejuizo total: R$ 40,320.00

  Colheita mecanizada:
    Registros:      2
    Perda media:    15.25%  (benchmark do setor: 15.0% -> ACIMA)
    Prejuizo total: R$ 649,800.00
```

---

## 7. Integrantes do grupo

- _(preencher com os nomes e RMs do grupo)_

---

## 8. Referências

- SOCICANA — perdas de até 15% na colheita mecanizada da cana-de-açúcar.
- CONAB — preços de referência de produtos agrícolas.
- EMBRAPA. _Agricultura digital: pesquisa, desenvolvimento e inovação nas cadeias produtivas._ 2020. https://www.alice.cnptia.embrapa.br/handle/doc/1126213
- TOTVS. _O que é agronegócio._ https://www.totvs.com/blog/gestao-agricola/o-que-e-agronegocio/
- AEVO Blog. _Agrotech._ https://blog.aevo.com.br/agrotech/
- CHB Agro. _Perdas na colheita de cana._ https://blog.chbagro.com.br/perdas-na-colheita-de-cana
- Documentação oficial `python-oracledb`. https://python-oracledb.readthedocs.io/
- Oracle Database Free. https://www.oracle.com/database/free/
