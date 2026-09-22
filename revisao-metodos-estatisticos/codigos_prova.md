[codigos_prova (2).md](https://github.com/user-attachments/files/32495516/codigos_prova.2.md)

# Códigos Prontos — Consulta Rápida

*Comandos testados. Cada um mostra o que trocar (varia por questão) e o que não muda (sempre igual).*

## Índice

1. [Sempre no início](#1-sempre-no-início-uma-vez-só-por-sessão)
2. [Abrir um arquivo de dados](#2-abrir-um-arquivo-de-dados)
3. [Outras olhadas nos dados](#3-outras-olhadas-nos-dados-além-do-head)
4. [Verificar consistência dos dados](#4-verificar-consistência-dos-dados-percentuais-somam-100)
5. [Percentual de "outros"](#5-calcular-o-percentual-de-outros-quando-a-soma-não-bate-100)
6. [Gráfico de barras — sem categoria nova](#6-gráfico-de-barras-1-variável-qualitativa--sem-precisar-criar-categoria-nova)
7. [Gráfico de barras — com categoria "Outros"](#7-gráfico-de-barras--com-criação-de-uma-categoria-outros-antes)
8. [Gráfico de linha / temporal](#8-gráfico-de-linha--temporal-1-variável-quantitativa-ao-longo-do-tempo)
9. [Histograma](#9-histograma-1-variável-quantitativa)
10. [Resumo dos 5 números / describe](#10-resumo-dos-5-números--describe-1-variável-quantitativa)
11. [Regra 1,5×AIQ (valor atípico)](#11-regra-15aiq-valor-atípico)
12. [Moda](#12-moda-1-variável-quantitativa)
13. [Boxplot](#13-boxplot-1-variável-quantitativa)
14. [Boxplots lado a lado](#14-boxplots-lado-a-lado-comparar-2-grupos-ex-2-bases-diferentes)
15. [Tabela de dupla entrada](#15-tabela-de-dupla-entrada-associação-entre-2-variáveis-qualitativas)
16. [Diagrama de dispersão](#16-diagrama-de-dispersão-2-variáveis-quantitativas)
17. [Correlação de Pearson](#17-correlação-de-pearson-2-variáveis-quantitativas)

*(Se algum link do índice não pular certinho, usa Ctrl+F e busca o número ou o nome do tema.)*

---

## 1. Sempre no início (uma vez só por sessão)

```python
import pandas as pd
import matplotlib.pyplot as plt
```
**O que trocar:** nada, esse bloco é sempre idêntico.
**Quando usar:** uma vez, no começo do notebook. Só repetir se der erro `name 'pd' is not defined` (sinal de que o ambiente reiniciou).

---

## 2. Abrir um arquivo de dados + primeira olhada (pronto pra copiar e colar)

**Se o arquivo for `.xls` ou `.xlsx`:**
```python
df = pd.read_excel('NOME_DO_ARQUIVO.xls')
df.head()
```

**Se o arquivo for `.csv`:**
```python
df = pd.read_csv('NOME_DO_ARQUIVO.csv')
df.head()
```

**O que trocar:** `NOME_DO_ARQUIVO.xls` (ou `.csv`) → pelo nome exato do arquivo que o enunciado da questão menciona (copiar certinho, com maiúsculas e a extensão certa).
**O que NÃO muda:** `pd.read_excel(...)` / `pd.read_csv(...)` (escolhe o bloco certo conforme a extensão do arquivo) e o `df.head()` embaixo.
**Pra que serve o `df.head()`:** mostra as 5 primeiras linhas da tabela — é assim que você descobre os nomes reais das colunas, que vai usar nos códigos seguintes.

---

## 3. Outras olhadas nos dados (além do `head()`)

```python
df.shape       # mostra (nº de linhas, nº de colunas)
df.columns     # lista os nomes das colunas
df.dtypes      # mostra o tipo de cada coluna (número, texto, data...)
```
**O que trocar:** nada.
**Quando usar:** rodar quando precisar confirmar quantas linhas/colunas tem a tabela, ver todos os nomes de coluna de uma vez, ou checar se uma coluna está sendo lida como número ou como texto.

---

## 4. Verificar consistência dos dados (percentuais somam 100%?)

```python
df['NOME_DA_COLUNA'].sum()
```
**O que faz, em palavras simples:** soma **todos os valores** de uma coluna, um por um, e devolve o total. Ex: se a coluna tem 3,8 / 6,3 / 12,5 / ..., esse código soma tudo isso e diz o resultado final.

**O que trocar:** `NOME_DA_COLUNA` → pelo nome da coluna de valores/percentuais (visto no `df.head()`).
**O que NÃO muda:** `df[...].sum()`.
**Quando usar:** dados são percentuais que deveriam somar ~100% (cada observação só entra numa categoria) — é o teste de "os dados fazem sentido?".
**Exemplo real:** na Questão 3, `df['NivelAudiencia'].sum()` deu **67,3** — a soma da audiência dos 12 formatos listados na tabela.

---

## 5. Calcular o percentual de "outros" (quando a soma não bate 100%)

```python
100 - df['NOME_DA_COLUNA'].sum()
```
**O que faz, em palavras simples:** pega **100** (o total que "deveria" existir) e subtrai a soma que você acabou de calcular. O resultado é **o pedaço que falta** — ou seja, o que não está listado na tabela.

**O que trocar:** `NOME_DA_COLUNA` → mesmo nome usado no passo anterior.
**Quando usar:** o enunciado avisa que existem mais categorias do que as listadas na tabela (ex: "esses são só os formatos mais populares").
**Exemplo real:** na Questão 3, a soma deu 67,3, então `100 - 67,3` = **32,7** — o percentual de audiência que ouve formatos "não listados" (outros).

---

## 6. Gráfico de barras (1 variável qualitativa) — SEM precisar criar categoria nova

Usar quando a tabela **já tem** todas as categorias que você quer mostrar (não precisa adicionar nenhuma linha extra).

```python
df.sort_values('NOME_COLUNA_VALOR', ascending=False).plot(x='NOME_COLUNA_CATEGORIA', y='NOME_COLUNA_VALOR', kind='bar')
plt.show()
```
**O que trocar:** `NOME_COLUNA_VALOR` e `NOME_COLUNA_CATEGORIA` → pelos nomes reais das colunas (visto no `df.head()`). Aparecem 2 vezes cada um — trocar as duas ocorrências.
**O que NÃO muda:** `sort_values(..., ascending=False)`, `.plot(...)`, `kind='bar'`, `plt.show()`.
**Exemplo:** Questão 2 (Disciplina/Percentual) — a tabela já vinha completa, só plotar direto.

---

## 7. Gráfico de barras — COM criação de uma categoria "Outros" antes

Usar quando o enunciado pede pra incluir uma categoria que **não vem pronta** na tabela (tipo "Outro formato", "Outra área") — normalmente o valor dela é o resultado do `100 - sum()` acima. Tem um passo a mais: **primeiro criar a linha, depois plotar**.

**Passo 1 — criar a linha nova:**
```python
df = df._append({'NOME_COLUNA_CATEGORIA': 'Outro formato', 'NOME_COLUNA_VALOR': VALOR_CALCULADO}, ignore_index=True)
```
**O que faz, em palavras simples:** adiciona uma linha nova no final da tabela, com o texto que você escolher na coluna de categoria e o número que você já calculou na coluna de valor.

**O que trocar:**
- `NOME_COLUNA_CATEGORIA` → nome da coluna de categoria
- `'Outro formato'` → o texto que você quer que apareça (ex: "Outra área", "Não listado"...)
- `NOME_COLUNA_VALOR` → nome da coluna de valor
- `VALOR_CALCULADO` → o número que você já calculou (ex: resultado do `100 - sum()`)

**Passo 2 — plotar (mesmo código de sempre, agora com a linha já incluída):**
```python
df.sort_values('NOME_COLUNA_VALOR', ascending=False).plot(x='NOME_COLUNA_CATEGORIA', y='NOME_COLUNA_VALOR', kind='bar')
plt.show()
```

**Exemplo real:** Questão 3 — calculamos 32,7 (item a) → criamos a linha "Outro formato" com esse valor → só depois plotamos o gráfico, e ele já apareceu incluído.

---

## 8. Gráfico de linha / temporal (1 variável quantitativa ao longo do tempo)

```python
df.plot(x='NOME_COLUNA_TEMPO', y='NOME_COLUNA_VALOR', kind='line')
plt.show()
```
**O que trocar:** `NOME_COLUNA_TEMPO` → nome da coluna de tempo (ano, mês, data). `NOME_COLUNA_VALOR` → nome da coluna quantitativa que você quer ver evoluindo.
**O que NÃO muda:** `kind='line'`, `plt.show()`.
**Quando usar:** a pergunta menciona "gráfico temporal", "evolução", "ao longo dos anos/meses" — qualquer coisa que peça pra ver como um valor mudou com o tempo.

---

## 9. Histograma (1 variável quantitativa)

```python
df['NOME_DA_COLUNA'].plot(kind='hist', bins=range(0, 35, 5), edgecolor='black')
plt.show()
```
**O que trocar:** `NOME_DA_COLUNA` → nome da coluna quantitativa. `bins=range(INÍCIO, FIM, LARGURA)` → ajustar conforme o enunciado pedir (ex: "classes de largura 5% começando em 0%" → `range(0, 35, 5)`; o FIM só precisa passar um pouco do valor máximo dos dados).
**O que NÃO muda:** `kind='hist'`, `edgecolor='black'`, `plt.show()`.

---

## 10. Resumo dos 5 números / describe (1 variável quantitativa)

```python
df['NOME_DA_COLUNA'].describe()
```
**O que trocar:** `NOME_DA_COLUNA` → nome da coluna quantitativa.
**O que NÃO muda:** `.describe()`.
**Sempre que a questão pedir "resumo dos 5 números"**, é esse comando. A resposta é só copiar 5 das 8 linhas que aparecem: `min`, `25%` (Q1), `50%` (mediana), `75%` (Q3), `max`. Ignorar `count`, `mean` e `std` (não fazem parte do resumo dos 5 números).

---

## 11. Regra 1,5×AIQ (valor atípico)

Primeiro, sempre calcular Q1, Q3 e AIQ (base pros dois limites):

```python
Q1 = 3.8
Q3 = 12.5
AIQ = Q3 - Q1
limite_superior = Q3 + 1.5 * AIQ
print(AIQ, limite_superior)
```

```python
Q1 = df['NOME_DA_COLUNA'].quantile(0.25)
Q3 = df['NOME_DA_COLUNA'].quantile(0.75)
AIQ = Q3 - Q1
```
**O que trocar:** `NOME_DA_COLUNA` → nome da coluna quantitativa (Q1/Q3 também podem ser digitados direto, copiando do `describe()` já rodado, em vez de usar `.quantile()`).

### Limite inferior — detecta valores anormalmente BAIXOS

```python
limite_inferior = Q1 - 1.5 * AIQ
print(limite_inferior)
```
**Quando usar:** a pergunta é sobre um valor muito **menor** que o resto (ex: "algum estado tem percentual anormalmente baixo?"). Qualquer valor **menor** que `limite_inferior` é atípico.

### Limite superior — detecta valores anormalmente ALTOS

```python
limite_superior = Q3 + 1.5 * AIQ
print(limite_superior)
```
**Quando usar:** a pergunta é sobre um valor muito **maior** que o resto (ex: "a Califórnia é atípica?"). Qualquer valor **maior** que `limite_superior` é atípico.

Na dúvida de qual vai cair, calcular os dois é rápido — não custa nada ter ambos prontos.

**Pra listar automaticamente quem são os atípicos** (em vez de comparar na mão):
```python
df[(df['NOME_DA_COLUNA'] < limite_inferior) | (df['NOME_DA_COLUNA'] > limite_superior)]
```
Mostra só as linhas da tabela que são atípicas (pra baixo ou pra cima).

---

## 12. Moda (1 variável quantitativa)

```python
df['NOME_DA_COLUNA'].mode()
```
**O que trocar:** `NOME_DA_COLUNA` → nome da coluna quantitativa.
**O que NÃO muda:** `.mode()`.
**Quando usar:** a questão pede "moda" — é o valor que mais se repete. Se aparecer só 1 valor na resposta, é a única moda. Se aparecer mais de 1, é porque empataram.

---

## 13. Boxplot (1 variável quantitativa)

```python
df['NOME_DA_COLUNA'].plot(kind='box')
plt.show()
```
**O que trocar:** `NOME_DA_COLUNA` → nome da coluna quantitativa.
**O que NÃO muda:** `kind='box'`, `plt.show()`.
**Como ler:** caixa = Q1 até Q3, linha no meio = mediana, bigodes = até o menor/maior valor que NÃO é atípico. Se tiver bolinha separada fora do bigode, é valor atípico (mesma regra do 1,5×AIQ).

---

## 14. Boxplots lado a lado (comparar 2 grupos, ex: 2 bases diferentes)

Usar quando a questão pede pra comparar a mesma variável entre dois grupos/bases (ex: tempo de viagem em 2 estados diferentes, cada um num arquivo separado).

```python
comparar = pd.DataFrame({'GRUPO_A': df_a['NOME_DA_COLUNA'], 'GRUPO_B': df_b['NOME_DA_COLUNA']})
comparar.plot(kind='box')
plt.show()
```
**O que faz, em palavras simples:** junta as duas colunas (vindas de duas tabelas diferentes) num "quadro" novo, lado a lado, e desenha os dois boxplots juntos no mesmo gráfico, pra dar pra comparar visualmente.

**O que trocar:**
- `GRUPO_A` / `GRUPO_B` → nomes que você quer que apareçam no gráfico (ex: `'Carolina do Norte'`, `'Nova York'`)
- `df_a`, `df_b` → nomes dos dois DataFrames (um de cada arquivo já aberto)
- `NOME_DA_COLUNA` → nome da coluna quantitativa (pode ter nome diferente em cada arquivo — ajustar cada ocorrência)

**O que NÃO muda:** `pd.DataFrame({...})`, `.plot(kind='box')`, `plt.show()`.

---

## 15. Tabela de dupla entrada (associação entre 2 variáveis qualitativas)

Usar quando a questão pergunta algo tipo "como [variável A] depende de [variável B]?" — precisa de 2 variáveis qualitativas.

**Passo 1 — montar a tabela cruzada** (transforma dados "empilhados" numa tabela de verdade, linhas x colunas):
```python
tabela = df.pivot_table(index='COLUNA_QUE_EXPLICA', columns='COLUNA_RESULTADO', values='COLUNA_CONTAGEM')
tabela
```
**Pra que serve:** os dados chegam "empilhados" (uma linha por combinação, tipo Chantix+Não, Chantix+Sim...). Esse código só **reorganiza visualmente** numa tabela cruzada de verdade — não calcula nada novo, só reorganiza o que já existe.
**Quando usar:** sempre que os dados de 2 variáveis qualitativas vierem nesse formato empilhado (uma linha por combinação + uma coluna de contagem) e você precisar ver a tabela cruzada.
**O que trocar:** `COLUNA_QUE_EXPLICA` → a variável que "causa"/explica (vai nas linhas). `COLUNA_RESULTADO` → a variável que é o resultado/efeito (vai nas colunas). `COLUNA_CONTAGEM` → a coluna com os números/contagens.
**O que NÃO muda:** `pivot_table(index=..., columns=..., values=...)`.

**Passo 2 — calcular o percentual condicional** (dentro de cada linha, qual % foi pra cada resultado):
```python
percentual = tabela.div(tabela.sum(axis=1), axis=0) * 100
percentual
```
**Pra que serve:** esse é o código que **de fato calcula** os percentuais — quanto % de cada grupo (linha) foi pra cada resultado. É ele que responde a pergunta "como um depende do outro".
**Quando usar:** sempre que a pergunta for do tipo "como [resultado] depende de [grupo/tratamento/categoria]" — ou seja, sempre que for percentual condicional. Só funciona depois de já ter a `tabela` pronta do Passo 1.
**O que faz, em palavras simples:** `tabela.sum(axis=1)` soma cada linha (total daquele grupo). `tabela.div(..., axis=0)` divide cada célula pelo total da **própria linha**. `* 100` transforma em percentual.
**O que NÃO muda:** essa linha de código é sempre igual, não precisa trocar nada nela.
**Exemplo real:** Questão 9 (CESSAFUMO) — tratamento nas linhas, fumou/não fumou nas colunas → percentual condicional mostrou Chantix com 44,03% de sucesso (não fumou), Bupropion 29,48%, Placebo 17,73%.

---

## 16. Diagrama de dispersão (2 variáveis quantitativas)

```python
df.plot(x='COLUNA_EXPLICATIVA', y='COLUNA_RESPOSTA', kind='scatter')
plt.show()
```
**Pra que serve:** desenha um gráfico de pontos, um ponto por observação — mostra visualmente se as duas variáveis "andam juntas" (associação positiva, negativa, ou sem padrão), e se tem algum ponto isolado (valor atípico).
**Quando usar:** a questão tem 2 variáveis quantitativas e pergunta sobre associação/relação entre elas.
**O que trocar:** `COLUNA_EXPLICATIVA` → nome da variável explicativa (a que "causa"; vai no eixo X). `COLUNA_RESPOSTA` → nome da variável resposta (o efeito; vai no eixo Y).
**O que NÃO muda:** `kind='scatter'`, `plt.show()`.

**Pra achar o valor exato de um ponto atípico visto no gráfico** (não tem regra numérica pra dispersão, então localizar pelo valor mais alto/baixo ajuda):
```python
df.sort_values('COLUNA_RESPOSTA', ascending=False).head()
```
**O que trocar:** `COLUNA_RESPOSTA` → mesma coluna do eixo Y. Trocar `ascending=False` por `True` se o atípico for um valor muito **baixo** em vez de muito alto.
**O que NÃO muda:** `sort_values(...)`, `.head()`.
**Exemplo real:** Questão 8 (FELICIDADE) — `df.plot(x='CompDif', y='BRFSS', kind='scatter')` mostrou associação negativa; `df.sort_values('BRFSS', ascending=False).head()` identificou Louisiana (BRFSS=0,033) como valor atípico.

---

## 17. Correlação de Pearson (2 variáveis quantitativas)

```python
df['COLUNA_1'].corr(df['COLUNA_2'])
```
**Pra que serve:** dá um número (entre -1 e +1) que resume ao mesmo tempo a direção e a força da associação entre 2 variáveis quantitativas — complementa o diagrama de dispersão com algo mais preciso que "olhar a nuvem de pontos".
**Quando usar:** a questão pede "correlação", "análise bidimensional" ou pergunta o quão forte é a relação entre 2 variáveis quantitativas.
**O que trocar:** `COLUNA_1` e `COLUNA_2` → nomes das duas colunas quantitativas (a ordem não importa, dá o mesmo resultado nos dois sentidos).
**O que NÃO muda:** `.corr(...)`.
**Como ler o resultado:** perto de +1 = positiva forte; perto de 0 = fraca/quase nenhuma; perto de -1 = negativa forte.
**Exemplo real:** Questão 10 (SATMAT) — `df['PctSAT'].corr(df['SAT-Mat'])` deu **-0,87** → correlação negativa forte entre % de alunos que fazem o SAT e a média do escore de matemática.
