[tecnica_escolha_codigo.md](https://github.com/user-attachments/files/32521801/tecnica_escolha_codigo.md)

# Técnica Rápida — Qual código usar?

*Guia de bolso pra decidir, em segundos, qual código do "Códigos Prontos" usar em cada questão da prova.*

## Índice

1. [O método: 2 perguntas antes de qualquer código](#o-método-2-perguntas-antes-de-qualquer-código)
2. [Cada tema × o que o enunciado vai pedir](#cada-tema--o-que-o-enunciado-vai-pedir)
3. [Na hora H](#na-hora-h)

---

## O método: 2 perguntas antes de qualquer código

Toda vez que ler uma questão, pare e responda:

**Pergunta 1: Quantas variáveis a questão está analisando?**
- **1 variável** → é unidimensional
- **2 variáveis, relacionadas entre si** → é bidimensional

**Pergunta 2: Qual o tipo dessa(s) variável(is)?**
- **Qualitativa** (categoria, palavra) ou **Quantitativa** (número)?

Com essas duas respostas, você já reduz bastante as opções. A tabela abaixo fecha a escolha.

---

## Cada tema × o que o enunciado vai pedir

| # (Códigos Prontos) | Tema | Palavra/frase que aparece no enunciado |
|---|---|---|
| 4 | Verificar consistência dos dados | "verifique a consistência", "os dados fazem sentido?", percentuais que deveriam somar 100% |
| 5 | Percentual de "outros" | "quais formatos/categorias **não estão listados**", pede pra achar o que falta pra completar 100% |
| 6 | Gráfico de barras (sem categoria nova) | 1 variável **qualitativa**, tabela já vem completa — "faça um gráfico", "apresente esses dados" |
| 7 | Gráfico de barras + categoria "Outros" | pede pra **incluir uma categoria "Outro"** que não vem pronta na tabela |
| 8 | Gráfico de linha / temporal | "**ao longo do tempo**", "evolução", "por ano/mês", "gráfico temporal", "que padrão geral..." |
| 9 | Histograma | "faça um **histograma**", "descreva a **distribuição**", "forma, centro e dispersão" |
| 10 | Resumo dos 5 números / describe | "**resumo dos 5 números**", "média", "desvio padrão", "quartis" |
| 11 | Regra 1,5×AIQ (valor atípico, 1 variável) | "**valor atípico**" falando de 1 variável só (sem gráfico de dispersão envolvido) |
| 12 | Moda | "qual a **moda**" |
| 13 | Boxplot | "**boxplot**", "quartis e valores atípicos", "faça uma análise completa" (média/moda/mediana/quartis) |
| 14 | Boxplot lado a lado | pede pra **comparar 2 grupos/bases** da mesma variável (ex: 2 arquivos diferentes) — "análises comparativas" |
| 15 | Tabela de dupla entrada | 2 variáveis **qualitativas** + "**associação**", "**depende de**", "isso influencia aquilo?" |
| 16 | Diagrama de dispersão | 2 variáveis **quantitativas** + "associação geral positiva ou negativa", "diagrama de dispersão" |
| 17 | Correlação de Pearson | "**correlação**", "**análise bidimensional**", "ajuda a explicar", "quão forte é a relação" |

---

## Na hora H

1. Lê a questão.
2. Marca mentalmente: "1 ou 2 variáveis?" e "quali ou quanti?".
3. Procura na tabela acima a palavra-chave que bateu com o enunciado.
4. Vai direto no número da seção no índice do doc de Códigos Prontos, copia, cola, ajusta os nomes das colunas (`df.head()` sempre primeiro).

Não precisa reler o documento inteiro — só usar essa tabela como bússola.
