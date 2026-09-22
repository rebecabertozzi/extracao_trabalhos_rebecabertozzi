# Técnica Rápida — Qual código usar?

*Guia de bolso pra decidir, em segundos, qual código do "Códigos Prontos" usar em cada questão da prova.*

---

## O método: 2 perguntas antes de qualquer código

Toda vez que ler uma questão, pare e responda:

**Pergunta 1: Quantas variáveis a questão está analisando?**
- **1 variável** → é unidimensional
- **2 variáveis, relacionadas entre si** → é bidimensional

**Pergunta 2: Qual o tipo dessa(s) variável(is)?**
- **Qualitativa** (categoria, palavra) ou **Quantitativa** (número)?

Com essas duas respostas, você já sabe exatamente qual seção do doc de Códigos usar.

---

## Tabela de decisão

| Tem... | E é... | Vai em... (seção do Códigos Prontos) |
|---|---|---|
| 1 variável | Qualitativa | Gráfico de barras/pizza (seções 6-7) |
| 1 variável | Quantitativa, quer distribuição | Histograma (9) ou describe/5 números (10) |
| 1 variável | Quantitativa, quer "valor repetido" | Moda (12) |
| 1 variável | Quantitativa, quer "valor estranho" | Boxplot (13) ou regra AIQ (11) |
| 1 variável quanti, mas **2 grupos/arquivos** pra comparar | — | Boxplot lado a lado (14) |
| 1 variável quanti **ao longo do tempo** | — | Gráfico de linha (8) |
| 2 variáveis | As 2 qualitativas | Tabela de dupla entrada (15) |
| 2 variáveis | As 2 quantitativas | Dispersão (16) + Pearson (17) |

---

## Palavras-chave do enunciado que já entregam a resposta

- **"distribuição", "resumo dos 5 números", "forma da distribuição"** → histograma/describe
- **"valor atípico"** (1 variável só) → AIQ/boxplot
- **"compare os grupos"** / dois arquivos de uma vez → boxplot lado a lado
- **"associação", "depende de"** + 2 categorias → tabela de dupla entrada
- **"correlação", "análise bidimensional"** + 2 números → dispersão + Pearson
- **"ao longo do tempo/anos"** → gráfico de linha

---

## Na hora H

1. Lê a questão.
2. Marca mentalmente: "1 ou 2 variáveis?" e "quali ou quanti?".
3. Vai direto no número da seção no índice do doc de Códigos Prontos.
4. Copia, cola, ajusta os nomes das colunas (`df.head()` sempre primeiro).

Não precisa reler o documento inteiro — só usar essa tabela como bússola.
