[cola (1).md](https://github.com/user-attachments/files/32540783/cola.1.md)
# Cola — Extração e Análise de Dados

22/09/2026

Guia de consulta para a prova prática, feito a partir das aulas 5, 6, 10, 11, 12 e 13 e do simulado Festival ViraBairro. Pra achar um tema, clique no mapa abaixo ou use Ctrl+F com as palavras da linha **Ctrl+F** de cada seção. `# TROQUE:` marca a linha que você adapta.

## Mapa rápido

| Se a questão pede | Vá para | Simulado |
| --- | --- | --- |
| carregar, primeiras linhas, linhas e colunas | [00](#00-começo-da-prova), [01](#01-olhar-a-base) | Q1 |
| ausentes, só colunas com ausência | [02](#02-valores-ausentes) | Q1 |
| duplicidade, registro repetido, por id | [03](#03-duplicatas) | Q2 |
| criar taxa, percentual, fórmula | [04](#04-coluna-calculada-taxa) | Q2, Q3 |
| média, mediana, resumo estatístico | [05](#05-média-mediana-e-describe) | Q3 |
| recorte, filtrar, só reel, a partir das 18h | [06](#06-filtrar-linhas) | Q4 |
| cinco maiores, ranking, ordenar | [07](#07-os-n-maiores-ranking) | Q4 |
| tabela por tema, nº de publicações e mediana | [08](#08-tabela-por-uma-coluna) | Q2, Q3, Q4 |
| combinação de tema e formato | [09](#09-tabela-por-duas-colunas) | Q5 |
| hashtags separadas por vírgula | [10](#10-hashtags-explode) | aula 5 |

| Gráficos e limpeza | Vá para | Simulado |
| --- | --- | --- |
| gráfico de barras, comparar temas | [11](#11-barras-verticais) | Q3 |
| barras horizontais, muitas categorias | [12](#12-barras-horizontais) | Q5, Q6 |
| dia, hora, linhas ao longo dos dias | [13](#13-datas-e-gráfico-de-linha) | Q4 |
| dispersão, real x previsto, linha de referência | [14](#14-dispersão-e-linha-de-referência) | Q7 |
| título, eixos, fonte no gráfico | [15](#15-checklist-do-gráfico) | Q3, Q4, Q5 |
| padronizar tema, grafias diferentes | [16](#16-padronizar-texto) | Q2 |
| converter data, formatos diferentes | [17](#17-converter-data) | Q2 |
| converter colunas numéricas | [18](#18-número-que-veio-como-texto) | Q2 |
| tratar ausências ou valores inválidos | [19](#19-ausentes-e-inválidos) | Q2 |
| validar colunas, log, try/except | [20](#20-validação-tryexcept-e-log) | aula 10 |
| **limpeza completa, pronta** | [Questão 2](#questão-2-do-simulado) | **Q2** |

| Modelos e respostas | Vá para | Simulado |
| --- | --- | --- |
| regressão, classificação ou clusterização? | [21](#21-qual-modelo-usar) | Q7, Q8 |
| características, categorias em números | [22](#22-x-y-e-get_dummies) | Q6, Q7, Q8 |
| 75% treino, 25% teste, preservar proporção | [23](#23-treino-e-teste) | Q6, Q7, Q8 |
| estimar número, MAE, R², linear x árvore | [24](#24-regressão-mae-e-r2) | Q7 |
| coeficientes, cauda longa | [25](#25-coeficientes-e-log1p) | aula 11 |
| percentil 75, criar o rótulo | [26](#26-rótulo-por-percentil) | Q6, Q8 |
| comparar três classificadores | [27](#27-comparar-classificadores) | Q8 |
| precisão, recall, F1, matriz de confusão | [28](#28-matriz-de-confusão-e-métricas) | Q8 |
| cortes 0,50 e 0,30 | [29](#29-ajustar-o-corte-threshold) | Q8 |
| características mais importantes | [30](#30-importâncias) | Q6 |
| agrupar sem rótulo, segmentar | [31](#31-kmeans) | aula 13 |
| deu erro ou número estranho | [32](#32-deu-erro) | todas |
| escrever a resposta em Markdown | [33](#33-frases-prontas) | todas |

## 00. Começo da prova

**Ctrl+F:** imports, importar, carregar, abrir arquivo, read\_csv, início

O ambiente já vem com tudo instalado e os arquivos ficam em `dados/`. Não instale nada. Cada questão recarrega o arquivo numa variável nova.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

q1 = pd.read_csv("dados/publicacoes_brutas.csv")   # TROQUE: nome da variável e do arquivo
# se o arquivo for separado por ponto e vírgula: pd.read_csv("...", sep=";")
```

Pra a tabela aparecer como texto na plataforma: `print(tabela.to_string(index=False))`. Avisos amarelos `FigureCanvasAgg is non-interactive` e `ConvergenceWarning` não são erro.

## Aula 5: pandas e métricas

Carregar, conferir, calcular taxa, filtrar e agrupar. Cai em Q1 a Q5.

### 01. Olhar a base

**Ctrl+F:** cinco primeiras linhas, dimensões, linhas e colunas, shape, head, tipos, dtypes, diagnóstico

```python
print(q1.head())                    # 5 primeiras linhas
linhas, colunas = q1.shape          # (nº de linhas, nº de colunas)
print(f"A base tem {linhas} linhas e {colunas} colunas.")
print(q1.dtypes)                    # tipo de cada coluna: int64/float64 = número, object/str = texto
print(q1.columns)                   # nomes exatos das colunas
```

### 02. Valores ausentes

**Ctrl+F:** ausentes, ausência, NaN, faltando, vazio, isna, somente colunas com ausência

Se pedir "somente as colunas que têm ausência", filtre o resultado: `isna().sum()` puro mostra também as que têm zero.

```python
ausentes = q1.isna().sum()
print(ausentes[ausentes > 0])       # só as colunas com pelo menos 1 ausente
```

### 03. Duplicatas

**Ctrl+F:** duplicidade, duplicata, registro repetido, drop\_duplicates, por id, subset

`drop_duplicates()` sem argumento só apaga linhas iguais em **todas** as colunas. Se pedir "por id\_publicacao", use `subset`. Olhe as cópias **antes** de apagar.

```python
repetidas = limpo[limpo.duplicated(subset="id_publicacao", keep=False)]  # TROQUE: coluna id
print(repetidas.to_string(index=False))     # mostra TODAS as cópias lado a lado
print("duplicadas:", limpo.duplicated(subset="id_publicacao").sum())
limpo = limpo.drop_duplicates(subset="id_publicacao", keep="first").copy()
# linha inteira repetida: limpo = limpo.drop_duplicates()
```

### 04. Coluna calculada (taxa)

**Ctrl+F:** criar taxa, taxa\_utilidade\_pct, taxa de engajamento, percentual, fórmula, dividir, × 100

Antes de dividir, tire alcance zero ou ausente (divisão por zero dá infinito). Engajamento é taxa (divisão), nunca número bruto.

```python
limpo = limpo[limpo["alcance"] > 0].copy()
limpo["taxa_utilidade_pct"] = (
    (limpo["compartilhamentos"] + limpo["salvamentos"]) / limpo["alcance"] * 100   # TROQUE: fórmula
)
# aula 5: df["taxa_engajamento"] = (df["likes"] + df["comments"] + df["shares"]) / df["plays"]
```

### 05. Média, mediana e describe

**Ctrl+F:** média, mediana, describe, estatística descritiva, quartis, desvio padrão, resumo

Média bem maior que mediana = poucos posts virais puxando pra cima. Mediana mostra o post típico.

```python
print(df["taxa_engajamento_pct"].describe())   # count, mean, std, min, 25%, 50%, 75%, max
print(df["taxa_engajamento_pct"].mean())       # média
print(df["taxa_engajamento_pct"].median())     # mediana
```

### 06. Filtrar linhas

**Ctrl+F:** recorte, filtrar, apenas, somente, a partir das 18h, condição, reel noturno, contains

Duas condições: cada uma entre parênteses, ligadas por `&` (e) ou `|` (ou). Nunca `and`/`or`.

```python
recorte = df[(df["formato"] == "reel") & (df["hora"] >= 18)]   # TROQUE: condições
print(len(recorte))
# uma condição só (aula 5): df[df["author"] == "g1"]  |  df[df["likes"] >= 5000]
# texto dentro (aula 5): df[df["hashtags"].str.contains("ia", na=False)]
```

### 07. Os N maiores (ranking)

**Ctrl+F:** cinco maiores, top 5, maior taxa, ranking, ordenar, sort\_values, nlargest

```python
top5 = recorte.nlargest(5, "taxa_engajamento_pct")[
    ["id_publicacao", "dia_publicacao", "hora", "tema", "taxa_engajamento_pct"]   # TROQUE: colunas pedidas
]
# igual: recorte.sort_values("taxa_engajamento_pct", ascending=False).head(5)
```

### 08. Tabela por uma coluna

**Ctrl+F:** tabela por tema, agrupar, groupby, agg, número de publicações, mediana por tema, resumo por

`median` = mediana, `mean` = média, `sum` = total, `count` = quantidade. Leia no enunciado qual pede.

```python
tabela = (
    df.groupby("tema")                                             # TROQUE: coluna do grupo
      .agg(publicacoes=("id_publicacao", "count"),
           mediana_pct=("taxa_utilidade_pct", "median"))           # TROQUE: coluna e função
      .reset_index()
      .sort_values("mediana_pct", ascending=False)
      .round(2)
)
print(tabela.to_string(index=False))
```

### 09. Tabela por duas colunas

**Ctrl+F:** combinação, tema e formato, duas variáveis, cruzamento, groupby lista

Passe uma **lista** no `groupby`. Olhe a coluna de contagem: grupo com poucas publicações não sustenta ranking.

```python
tabela2 = (
    df.groupby(["tema", "formato"])
      .agg(publicacoes=("id_publicacao", "count"),
           mediana_engajamento_pct=("taxa_engajamento_pct", "median"))
      .reset_index()
      .sort_values("mediana_engajamento_pct", ascending=False)
      .round(2)
)
tabela2["combinacao"] = tabela2["tema"] + " / " + tabela2["formato"]   # rótulo pro gráfico
```

### 10. Hashtags: explode

**Ctrl+F:** hashtag, explodir, explode, split, vírgula, value\_counts, mais frequentes

Sem o `split` antes, o `explode` não separa nada.

```python
df_h = df.dropna(subset=["hashtags"]).copy()
df_h["hashtags"] = df_h["hashtags"].str.split(",")               # "a,b" vira ["a", "b"]
df_h = df_h.explode("hashtags")                                   # uma linha por hashtag
df_h["hashtags"] = df_h["hashtags"].str.strip().str.lower()
print(df_h["hashtags"].value_counts().head(10))
```

## Aula 6: gráficos

Barras compara categorias, linha mostra tempo, dispersão relaciona duas variáveis numéricas. Cai em Q3, Q4, Q5, Q6 e Q7.

### 11. Barras verticais

**Ctrl+F:** gráfico de barras, comparar temas, bar, comparar categorias

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tabela["tema"], tabela["mediana_pct"], color="#3b6ea5")    # TROQUE: colunas x e y
ax.set_title("Qual tema as pessoas mais salvam e compartilham?")    # TROQUE: título = a pergunta
ax.set_xlabel("Tema da publicação")
ax.set_ylabel("Mediana da taxa de utilidade (%)")                  # sempre com a unidade
ax.tick_params(axis="x", rotation=45)                               # se os nomes sobrepuserem
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

### 12. Barras horizontais

**Ctrl+F:** barras horizontal, barh, muitas categorias, combinações, rótulo comprido, importâncias

No `barh` o valor fica no eixo **X**. O `[::-1]` coloca o maior no topo.

```python
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(tabela2["combinacao"][::-1], tabela2["mediana_engajamento_pct"][::-1], color="#3b6ea5")  # TROQUE
ax.set_title("Quais combinações de tema e formato engajam mais?")
ax.set_xlabel("Mediana da taxa de engajamento (%)")
ax.set_ylabel("Tema / formato")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

### 13. Datas e gráfico de linha

**Ctrl+F:** dia\_publicacao, só a data, hora, dia da semana, mês, ao longo dos dias, acompanhamento diário, gráfico de linhas, série temporal, cronológica

Na base já tratada a data vem num formato só, então `pd.to_datetime` simples funciona. Na base bruta, use a [17](#17-converter-data).

```python
q4["data_publicacao"] = pd.to_datetime(q4["data_publicacao"])
q4["dia_publicacao"] = q4["data_publicacao"].dt.date        # só a data, sem hora
# q4["hora"] = q4["data_publicacao"].dt.hour  |  .dt.dayofweek (0 = segunda)   (aula 11)
diaria = (q4.groupby("dia_publicacao")
            .agg(publicacoes=("id_publicacao", "count"),
                 media_engajamento_pct=("taxa_engajamento_pct", "mean"),
                 alcance_total=("alcance", "sum"))
            .reset_index().sort_values("dia_publicacao").round(2))   # cronológica = crescente

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(diaria["dia_publicacao"], diaria["media_engajamento_pct"], marker="o", markersize=3)
ax.set_title("Como a taxa média de engajamento variou dia a dia")
ax.set_xlabel("Dia da publicação"); ax.set_ylabel("Taxa média de engajamento (%)")
ax.tick_params(axis="x", rotation=45)
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout(); plt.show()
```

Cortar um período (aula 6): `diaria[diaria["dia_publicacao"] >= pd.to_datetime("2026-04-01").date()]`.

### 14. Dispersão e linha de referência

**Ctrl+F:** dispersão, scatter, relação entre duas variáveis, real x previsto, valores reais e previstos, linha de referência, diagonal, escala log

```python
fig, ax = plt.subplots(figsize=(6.5, 6))
ax.scatter(y_teste, previsao, alpha=0.5, color="#3b6ea5")            # TROQUE: x e y
minimo = float(min(y_teste.min(), previsao.min()))
maximo = float(max(y_teste.max(), previsao.max()))
ax.plot([minimo, maximo], [minimo, maximo], color="#c0392b", linestyle="--", label="previsão = valor real")
ax.set_title("Valor real x valor previsto")
ax.set_xlabel("Taxa de engajamento real (%)"); ax.set_ylabel("Taxa de engajamento prevista (%)")
ax.legend(); fig.tight_layout(); plt.show()
# valores muito espalhados (seguidores): ax.set_xscale("log")
```

Ponto acima da linha: o modelo previu mais do que aconteceu. Abaixo: previu menos.

### 15. Checklist do gráfico

**Ctrl+F:** boas práticas, título, eixos nomeados, fonte, indicador, métrica, dashboard

Cada item é ponto na correção:

- [ ] título que comunica a pergunta (não "Gráfico 1")
- [ ] nome no eixo X e no eixo Y, com unidade (%)
- [ ] fonte escrita **dentro** do gráfico com `fig.text(...)`
- [ ] um gráfico, uma pergunta, uma conclusão sem extrapolar a amostra

**Métrica** é qualquer número calculado (curtidas médias, taxa). **Indicador** é a métrica escolhida pra acompanhar porque responde uma decisão. **Dashboard** junta vários gráficos em torno de uma decisão.

## Aula 10: limpeza

Transformar a base bruta numa base confiável, sem inventar dado, e registrar cada decisão. É a Q2, o foco da monitoria. A regra de ouro: **trabalhe numa cópia**, nunca sobrescreva o bruto.

### 16. Padronizar texto

**Ctrl+F:** padronizar tema, grafias diferentes, maiúscula, minúscula, acento, espaço sobrando, strip, lower, title, equivalência, replace, value\_counts

`strip` + `lower` resolvem espaço e maiúscula, mas **não** juntam `saude` e `saúde`. Rode `value_counts` antes: se o enunciado promete 4 temas e aparecem 5, sobra uma grafia pro dicionário.

```python
limpo["tema"] = limpo["tema"].str.strip().str.lower()
print(limpo["tema"].value_counts(dropna=False))          # olhe ANTES de decidir
limpo["tema"] = limpo["tema"].replace({"saúde": "saude"})   # TROQUE: grafia errada -> certa
print(limpo["tema"].value_counts(dropna=False))          # confira: só as categorias esperadas
# aula 10: .str.title() deixa "Historical Fiction"; categorias equivalentes {"Sci-Fi": "Science Fiction"}
```

### 17. Converter data

**Ctrl+F:** converter data, data\_publicacao, datas em formatos distintos, to\_datetime, dayfirst, format, NaT, ISO

**Armadilha principal da prova.** Sem `format`, o pandas adivinha o formato pela primeira linha e transforma em `NaT` o que não encaixa. E `dayfirst=True` na coluna toda troca dia e mês das datas que começam pelo ano. Converta em duas passadas e confira `.min()` e `.max()`.

```python
texto_data = limpo["data_publicacao"].copy()                     # guarda o texto original
ano_primeiro = limpo["data_publicacao"].str[:4].str.isdigit().fillna(False)
iso = pd.to_datetime(limpo["data_publicacao"].where(ano_primeiro),
                     format="ISO8601", errors="coerce")          # 2026-08-01 e 2026/08/04
br = pd.to_datetime(limpo["data_publicacao"].where(~ano_primeiro),
                    format="mixed", dayfirst=True, errors="coerce")   # 05/08/2026
limpo["data_publicacao"] = iso.fillna(br)
print("NaT:", limpo["data_publicacao"].isna().sum())
print("de", limpo["data_publicacao"].min(), "até", limpo["data_publicacao"].max())   # bate com o período?
print(texto_data[limpo["data_publicacao"].isna()])               # quais textos não viraram data
```

Se a coluna tiver um formato só, basta `pd.to_datetime(coluna)`. Mostrar em formato brasileiro: `.dt.strftime("%d/%m/%Y")`.

### 18. Número que veio como texto

**Ctrl+F:** converter colunas numéricas, tipo adequado, to\_numeric, preço com símbolo, object, texto para número

Confira o `dtype` **antes**. Se já vier `float64` ou `int64`, a coluna chegou numérica e você não pode dizer que "converteu texto". Coluna com ausente vira `float64`, não `int64`.

```python
print(limpo[["alcance", "compartilhamentos", "salvamentos"]].dtypes)   # olhe antes
for coluna in ["alcance", "compartilhamentos", "salvamentos"]:         # TROQUE: colunas da fórmula
    limpo[coluna] = pd.to_numeric(limpo[coluna], errors="coerce")     # texto inválido vira NaN
# texto com símbolo (aula 10): df["preco"] = df["preco"].str.replace("£", "", regex=False).str.strip()
```

### 19. Ausentes e inválidos

**Ctrl+F:** tratar ausências, valores inválidos, descartar, preencher, dropna, fillna, alcance zero, negativo, justificar

Três opções: descartar a linha (campo essencial), preencher (só com valor que não se disfarce de dado real) ou manter `NaN` e documentar. Só descarte pelo que entra no cálculo: `comentarios` ausente não derruba a linha se a fórmula não usa comentário. Imprima quantas linhas cada filtro derrubou.

```python
antes = len(limpo)
limpo = limpo.dropna(subset=["tema"]);  print("sem tema:", antes - len(limpo)); antes = len(limpo)
limpo = limpo.dropna(subset=["alcance", "compartilhamentos", "salvamentos"])  # TROQUE: campos da fórmula
print("sem campo da taxa:", antes - len(limpo)); antes = len(limpo)
limpo = limpo[limpo["alcance"] > 0];      print("alcance zero:", antes - len(limpo)); antes = len(limpo)
limpo = limpo[(limpo["compartilhamentos"] >= 0) & (limpo["salvamentos"] >= 0)]
print("negativos:", antes - len(limpo))
# preencher (aula 10): df["avaliacao"] = df["avaliacao"].fillna(0)   # 0 = "sem avaliação", fora da escala 1-5
```

### 20. Validação, try/except e log

**Ctrl+F:** validar, colunas obrigatórias, raise, fora do intervalo, try, except, log, pipeline, raw, processed

`raw/` é o bruto intocado, `processed/` é o resultado limpo com outro nome. No `except`, diga o tipo do erro (`ValueError`), nunca `except:` sozinho.

```python
fora = (df["avaliacao"] < 1) | (df["avaliacao"] > 5)            # TROQUE: regra do domínio
df.loc[fora, "avaliacao"] = float("nan")                        # mantém como ausente, documentado
for coluna in ["titulo", "preco", "data_coleta"]:               # TROQUE: colunas obrigatórias
    if coluna not in df.columns:  raise ValueError(f"Coluna ausente: {coluna}")
    if df[coluna].isna().all():   raise ValueError(f"Coluna vazia: {coluna}")
try:
    numero = float("Grátis")
except ValueError:
    numero = None                                               # registra e segue
log = [f"Linhas no bruto: {linhas_brutas}", f"Linhas no final: {len(df)}"]
```

## Questão 2 do simulado

**Ctrl+F:** tratamento dos registros, limpeza completa, pipeline, prepare os dados, decisões de limpeza, taxa\_utilidade\_pct por tema

O bloco inteiro da limpeza, na ordem certa, pra copiar e adaptar (junta as seções 03, 16, 17, 18, 19, 04 e 08). A resolução comentada está no doc do simulado. Rode, **olhe cada print** e só escreva na resposta o que os prints mostraram.

```python
limpo = pd.read_csv("dados/publicacoes_brutas.csv")      # variável NOVA, do bruto
print("linhas no bruto:", len(limpo))

# 1. duplicidade por id (olhar as cópias antes)
print(limpo[limpo.duplicated(subset="id_publicacao", keep=False)].to_string(index=False))
print("duplicadas:", limpo.duplicated(subset="id_publicacao").sum())
limpo = limpo.drop_duplicates(subset="id_publicacao", keep="first").copy()

# 2. tema
limpo["tema"] = limpo["tema"].str.strip().str.lower()
print(limpo["tema"].value_counts(dropna=False))
limpo["tema"] = limpo["tema"].replace({"saúde": "saude"})   # TROQUE conforme o value_counts
print(limpo["tema"].value_counts(dropna=False))

# 3. data em duas passadas + conferência
texto_data = limpo["data_publicacao"].copy()
ano_primeiro = limpo["data_publicacao"].str[:4].str.isdigit().fillna(False)
iso = pd.to_datetime(limpo["data_publicacao"].where(ano_primeiro), format="ISO8601", errors="coerce")
br = pd.to_datetime(limpo["data_publicacao"].where(~ano_primeiro), format="mixed", dayfirst=True, errors="coerce")
limpo["data_publicacao"] = iso.fillna(br)
print("NaT:", limpo["data_publicacao"].isna().sum())
print("de", limpo["data_publicacao"].min(), "até", limpo["data_publicacao"].max())

# 4. números (olhar dtype antes)
cols = ["alcance", "compartilhamentos", "salvamentos"]
print(limpo[cols].dtypes)
for c in cols:
    limpo[c] = pd.to_numeric(limpo[c], errors="coerce")

# 5. ausências e inválidos, contando o que cada filtro derrubou
antes = len(limpo)
limpo = limpo.dropna(subset=cols);          print("sem campo da taxa:", antes - len(limpo)); antes = len(limpo)
limpo = limpo[limpo["alcance"] > 0];        print("alcance zero:", antes - len(limpo)); antes = len(limpo)
limpo = limpo[(limpo["compartilhamentos"] >= 0) & (limpo["salvamentos"] >= 0)]
print("negativos:", antes - len(limpo), "| restam:", len(limpo))

# 6. taxa e tabela por tema com MEDIANA
limpo["taxa_utilidade_pct"] = (limpo["compartilhamentos"] + limpo["salvamentos"]) / limpo["alcance"] * 100
resumo = (limpo.groupby("tema")
               .agg(publicacoes=("id_publicacao", "count"),
                    mediana_utilidade_pct=("taxa_utilidade_pct", "median"))
               .reset_index().sort_values("mediana_utilidade_pct", ascending=False).round(2))
print(resumo.to_string(index=False))
```

**Modelo de resposta (até 4 frases, sempre "fiz X porque Y"):**

> Removi \_\_\_\_ duplicidade(s) por `id_publicacao`, mantendo a primeira ocorrência, depois de conferir que as cópias eram \_\_\_\_ (idênticas / diferentes em \_\_\_\_). Padronizei `tema` com `strip` e `lower` e, como o `value_counts` mostrou \_\_\_\_ grafias para 4 temas, unifiquei `____` e `____` com uma tabela de equivalência manual. Converti `data_publicacao` em duas passadas, com `format="ISO8601"` nas datas com ano à frente e `dayfirst=True` no resto, porque a coluna mistura formatos e um `dayfirst` em tudo trocaria dia e mês sem avisar; o período ficou entre \_\_\_\_ e \_\_\_\_, com \_\_\_\_ datas perdidas. As colunas da taxa chegaram como \_\_\_\_ (numéricas / texto), e descartei \_\_\_\_ linha(s) sem \_\_\_\_, porque sem esse campo a taxa não existe e preencher seria inventar dado.

Não cite filtro que derrubou 0 linhas como se tivesse tratado algo. Se as colunas já eram `float64`, não diga que converteu texto.

## Aula 11: regressão

O esqueleto é sempre o mesmo: montar X e y, separar treino e teste, `fit`, `predict`, medir o erro. Cai em Q6, Q7 e Q8.

### 21. Qual modelo usar

**Ctrl+F:** tipo de aprendizado, regressão, classificação, clusterização, supervisionado, não supervisionado, por que os outros não servem

| O alvo é | Use | Por que os outros não servem |
| --- | --- | --- |
| um **número contínuo** (taxa, views) | **regressão** | classificação exigiria um corte arbitrário; clusterização não tem alvo |
| uma **categoria** (0/1, viralizou, merece divulgação) | **classificação** | regressão dá número, que ainda precisaria de corte; clusterização não usa resposta conhecida |
| **não existe** (achar grupos parecidos) | **clusterização** | regressão e classificação precisam de um alvo pra aprender |

Regressão e classificação são **supervisionadas** (aprendem com resposta conhecida). Clusterização é **não supervisionada**.

### 22. X, y e get\_dummies

**Ctrl+F:** características, features, alvo, transformar categorias em números, get\_dummies, vazamento, antes da publicação

**Vazamento:** nada que só existe depois de publicar entra no X (alcance, curtidas, comentários, compartilhamentos, salvamentos, a própria taxa). `id_publicacao` também não. `tema` e `formato` são texto: sem `get_dummies` dá `could not convert string to float`.

```python
CARACTERISTICAS = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
                   "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]   # TROQUE: lista do enunciado
X = pd.get_dummies(df[CARACTERISTICAS], columns=["tema", "formato"])   # texto vira colunas 0/1
y = df["taxa_engajamento_pct"]                                          # TROQUE: o alvo
print(X.shape, list(X.columns))
```

### 23. Treino e teste

**Ctrl+F:** 75% treino, 25% teste, reserve, train\_test\_split, random\_state, preservando a proporção, stratify

`stratify=y` **só em classificação** ("preservando a proporção do alvo"). Em regressão o alvo é contínuo e o stratify quebra.

```python
from sklearn.model_selection import train_test_split
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42)          # regressão
# classificação: train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
```

### 24. Regressão: MAE e R2

**Ctrl+F:** estimar, regressão linear, árvore de regressão, profundidade máxima, MAE, R², r2\_score, modelo bobo, baseline, comparar modelos

**MAE** = quanto a previsão erra em média, na unidade do alvo. **R²** = quanto da variação o modelo explica (1 perfeito, 0 = chutar a média, negativo = pior que a média). O modelo bobo não é pedido, mas é a referência. Nenhum modelo é sempre melhor: compare pelo número.

```python
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score
linear = LinearRegression().fit(X_treino, y_treino)
arvore = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_treino, y_treino)   # TROQUE: max_depth
prev_lin, prev_arv = linear.predict(X_teste), arvore.predict(X_teste)
prev_bobo = np.full(len(y_teste), y_treino.mean())            # chuta sempre a média do treino
comparacao = pd.DataFrame({
    "modelo": ["modelo bobo", "regressão linear", "árvore (prof. 4)"],
    "MAE": [mean_absolute_error(y_teste, p) for p in (prev_bobo, prev_lin, prev_arv)],
    "R2":  [r2_score(y_teste, p) for p in (prev_bobo, prev_lin, prev_arv)]}).round(3)
print(comparacao.to_string(index=False))
if mean_absolute_error(y_teste, prev_lin) <= mean_absolute_error(y_teste, prev_arv):
    previsao = prev_lin          # menor MAE: linear
else:
    previsao = prev_arv          # menor MAE: árvore
```

Depois: gráfico real x previsto na [14](#14-dispersão-e-linha-de-referência). R² altíssimo (0,95+) de primeira quase sempre é vazamento.

### 25. Coeficientes e log1p

**Ctrl+F:** coeficiente, peso, coef\_, sinal, cauda longa, assimetria, log1p, expm1, views

Só o **sinal** do coeficiente é comparável entre features (escalas diferentes). Coeficiente é associação, não causa.

```python
coef = pd.DataFrame({"caracteristica": X.columns, "coeficiente": linear.coef_}).sort_values("coeficiente")
print(coef.to_string(index=False))
# alvo com cauda longa (plays): treine em np.log1p(y) e desfaça com np.expm1(previsao)
print(df["plays"].skew(), np.log1p(df["plays"]).skew())      # assimetria antes e depois
```

## Aula 12: classificação

O alvo vira uma categoria (0/1) que **você** cria por um corte. Acurácia engana quando a classe 1 é rara: olhe precisão, recall, F1 e a matriz. Cai em Q6 e Q8.

### 26. Rótulo por percentil

**Ctrl+F:** percentil 75, percentil 90, criar o alvo, mereceu\_divulgacao\_adicional, viralizou, rótulo, corte, quantile

```python
corte = df["taxa_engajamento_pct"].quantile(0.75)                        # TROQUE: coluna e percentil
df["mereceu_divulgacao_adicional"] = (df["taxa_engajamento_pct"] > corte).astype(int)   # 1 acima, 0 resto
print(f"corte: {corte:.2f} | positivos: {df['mereceu_divulgacao_adicional'].sum()} de {len(df)}")
X = pd.get_dummies(df[CARACTERISTICAS], columns=["tema", "formato"])      # a taxa NÃO entra no X
y = df["mereceu_divulgacao_adicional"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
```

### 27. Comparar classificadores

**Ctrl+F:** três classificadores, regressão logística, árvore de classificação, Random Forest, Extra Trees, AdaBoost, Naive Bayes, pesos balanceados, class\_weight

A logística é obrigatória se a questão pedir para mexer no corte. "Pesos balanceados" = `class_weight="balanced"`.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier   # outros: ExtraTreesClassifier, AdaBoostClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix, accuracy_score
modelos = {"regressão logística": LogisticRegression(max_iter=5000),
           "árvore de classificação": DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced"),
           "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")}
linhas = []
for nome, modelo in modelos.items():
    modelo.fit(X_treino, y_treino); d = modelo.predict(X_teste)
    linhas.append({"modelo": nome, "precisão": precision_score(y_teste, d, zero_division=0),
                   "recall": recall_score(y_teste, d, zero_division=0), "F1": f1_score(y_teste, d, zero_division=0)})
comparacao = pd.DataFrame(linhas).sort_values("F1", ascending=False).round(3)
print(comparacao.to_string(index=False))
# Naive Bayes: from sklearn.naive_bayes import GaussianNB  ->  GaussianNB()
```

### 28. Matriz de confusão e métricas

**Ctrl+F:** matriz de confusão, falso positivo, falso negativo, precisão, recall, F1, acurácia, maior F1

|  | modelo disse 0 | modelo disse 1 |
| --- | --- | --- |
| **era 0** | VN (verdadeiro negativo) | **FP** (alarme falso) |
| **era 1** | **FN** (deixou passar) | VP (acertou) |

**Precisão** = dos que o modelo indicou, quantos eram. **Recall** = dos que eram, quantos o modelo achou. **F1** = equilíbrio dos dois. **Acurácia** = acertos / total (engana com classe rara).

```python
melhor = modelos[comparacao.iloc[0]["modelo"]]          # primeira linha = maior F1
cm = confusion_matrix(y_teste, melhor.predict(X_teste))
print(f"VN={cm[0,0]}  FP={cm[0,1]}\nFN={cm[1,0]}  VP={cm[1,1]}")
```

### 29. Ajustar o corte (threshold)

**Ctrl+F:** corte 0,50, corte 0,30, threshold, limiar, predict\_proba, probabilidade, trade-off

`.predict()` já usa corte 0,50. Pra mudar o corte precisa da probabilidade. Corte mais baixo: mais recall, menos precisão.

```python
prob = modelos["regressão logística"].predict_proba(X_teste)[:, 1]   # prob. de ser 1
linhas_corte = []
for corte in [0.50, 0.30]:                                            # TROQUE: cortes pedidos
    d = (prob >= corte).astype(int)
    linhas_corte.append({"corte": corte, "precisão": precision_score(y_teste, d, zero_division=0),
                         "recall": recall_score(y_teste, d, zero_division=0), "F1": f1_score(y_teste, d, zero_division=0),
                         "VP": int(((d == 1) & (y_teste.values == 1)).sum()),
                         "FP": int(((d == 1) & (y_teste.values == 0)).sum()),
                         "FN": int(((d == 0) & (y_teste.values == 1)).sum())})
print(pd.DataFrame(linhas_corte).round(3).to_string(index=False))
```

### 30. Importâncias

**Ctrl+F:** importância, feature\_importances\_, características mais importantes, mais usadas pela árvore, cinco maiores

Importância = o quanto a árvore usou a característica pra separar os dados que viu. Não é causa. Empate na segunda casa decimal = ranking instável.

```python
arvore = DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced").fit(X_treino, y_treino)
importancias = (pd.DataFrame({"caracteristica": X.columns, "importancia": arvore.feature_importances_})
                  .sort_values("importancia", ascending=False).reset_index(drop=True))
top5 = importancias.head(5); print(top5.to_string(index=False))
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(top5["caracteristica"][::-1], top5["importancia"][::-1], color="#3b6ea5")
ax.set_title("O que a árvore mais usou para separar as publicações de destaque")
ax.set_xlabel("Importância na árvore (0 a 1)"); ax.set_ylabel("Característica")
fig.tight_layout(); plt.show()
```

## Aula 13: clusterização

Não caiu no simulado, mas está nas aulas. Não existe alvo: o algoritmo agrupa por semelhança e **você** dá nome aos grupos.

### 31. KMeans

**Ctrl+F:** clusterização, segmentação, agrupar, grupos, KMeans, padronizar, StandardScaler, cotovelo, inércia, silhueta, perfil, PCA

Padronizar não é opcional: sem `StandardScaler`, a coluna de maior escala domina. Escolha `k` pelo cotovelo (inércia para de cair) e pela maior silhueta. Os números 0, 1, 2 dos grupos não têm ordem.

```python
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
colunas_num = clientes.select_dtypes("number").columns.tolist()      # TROQUE: base e colunas
X_pad = StandardScaler().fit_transform(clientes[colunas_num])          # média 0, desvio 1
for k in range(2, 9):
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_pad)
    print(k, round(km.inertia_, 1), round(silhouette_score(X_pad, km.labels_), 3))
clientes["cluster"] = KMeans(n_clusters=4, n_init=10, random_state=42).fit_predict(X_pad)   # TROQUE: k
print(clientes.groupby("cluster")[colunas_num].mean().round(1))       # perfil: leia e dê nome
clientes["segmento"] = clientes["cluster"].map({0: "novos", 1: "fiéis", 2: "promoção", 3: "risco"})  # TROQUE
# ver em 2D: from sklearn.decomposition import PCA; PCA(n_components=2, random_state=42).fit_transform(X_pad)
```

Silhueta baixa em todo k (abaixo de \~0,2) = os dados talvez não tenham grupos. O KMeans sempre devolve k grupos, mesmo quando eles não existem.

## 32. Deu erro

**Ctrl+F:** erro, error, KeyError, NaN, NaT, não converte, número estranho, vazio

As últimas linhas são as mais perigosas: o código roda e entrega número errado, sem aviso vermelho.

| Mensagem ou sintoma | O que é | Seção |
| --- | --- | --- |
| `KeyError: 'coluna'` | nome de coluna errado (maiúscula, acento) | rode `df.columns`, 01 |
| `name 'pd' is not defined` | faltou rodar os imports | 00 |
| `FileNotFoundError` | caminho errado, os arquivos estão em `dados/` | 00 |
| `could not convert string to float` | texto no X do modelo | 22 (`get_dummies`) |
| `Input contains NaN` | ausente no X do modelo | 19 (decida: `dropna` ou `fillna`) |
| `The least populated class...` / erro no stratify | usou `stratify` em regressão | 23 |
| precision/recall = 0 com aviso "ill-defined" | modelo não previu nenhum 1 | 29 (baixe o corte) ou `class_weight` |
| erro de sintaxe no filtro | faltou parêntese ou usou `and` no lugar de `&` | 06 |
| muitos `NaT` depois de converter data | data boa morta por falta de `format` | 17 |
| datas fora do período esperado | `dayfirst=True` trocou dia e mês | 17 (confira `.min()`/`.max()`) |
| duplicata "removida" mas o id continua repetido | `drop_duplicates()` sem `subset` | 03 |
| 5 temas quando deviam ser 4 | acento ou grafia não unificada | 16 |
| `inf` ou mediana estranha na taxa | divisão por alcance zero | 19 |
| R² de 0,95+ de primeira | vazamento: resultado dentro do X | 22 |
| explode não mudou o nº de linhas | faltou `.str.split(",")` antes | 10 |
| `ConvergenceWarning` / `FigureCanvasAgg` | só aviso, o código rodou | nenhuma |

## 33. Frases prontas

**Ctrl+F:** resposta, Markdown, interpretação, limitação, recomendação, causalidade, justificar

Metade da nota está no texto. Conte as frases que o enunciado pede, use os números da **sua** tela e adapte as palavras (não cole a mesma frase em todas).

1. **Mediana:** A mediana de \_\_\_\_ é \_\_\_\_%, ou seja, metade das publicações do tema ficou acima e metade abaixo desse valor, o que a torna menos sensível que a média a uma peça atípica.
2. **Empate:** A diferença entre \_\_\_\_ e \_\_\_\_ é de apenas \_\_\_\_ ponto percentual, calculada sobre \_\_\_\_ publicações, pequena demais para sustentar um ranking; o que os dados mostram com segurança é que \_\_\_\_ fica atrás dos demais.
3. **Amostra pequena:** A base tem só \_\_\_\_ registros (\_\_\_\_ por dia / por grupo), então uma única publicação fora do padrão já muda a média ou a posição no ranking.
4. **Generalização:** Os dados vêm de uma única campanha de uma organização fictícia e não têm coluna de \_\_\_\_ (rede, público, bairro), então descrevem só este conjunto e não todas as redes ou públicos.
5. **Causalidade:** Isto é uma associação observada nesta base, não uma relação de causa: \_\_\_\_ e \_\_\_\_ não foram distribuídos de forma controlada, então não dá para afirmar que mudar \_\_\_\_ produziria o efeito observado.
6. **Recorte não prova:** O ranking seleciona as \_\_\_\_ melhores de um grupo de \_\_\_\_ já filtrado por \_\_\_\_; para sustentar que \_\_\_\_ funciona seria preciso comparar com \_\_\_\_ nas mesmas condições.
7. **Limpeza:** \_\_\_\_ (removi / descartei / padronizei) \_\_\_\_ porque \_\_\_\_; conferi pelo \_\_\_\_ (print, `value_counts`, `.min()`/`.max()`) que \_\_\_\_.
8. **MAE e R²:** O MAE de \_\_\_\_ significa que, em média, a previsão erra a taxa em cerca de \_\_\_\_ ponto percentual; o R² de \_\_\_\_ indica que o modelo explica \_\_\_\_ da variação, contra MAE de \_\_\_\_ do modelo que só chuta a média.
9. **Vazamento:** Não usei \_\_\_\_ (alcance, interações, a própria taxa) como característica porque só existem depois da publicação; usá-las seria prever olhando o gabarito.
10. **Corte:** Escolhi \_\_\_\_ com corte \_\_\_\_ porque \_\_\_\_; um falso positivo significa \_\_\_\_ (gastar um espaço de divulgação à toa) e um falso negativo significa \_\_\_\_ (deixar sem apoio uma peça que renderia); com \_\_\_\_ positivos no teste, cada acerto muda o recall em cerca de \_\_\_\_, então a vantagem não é regra estável.
11. **Importância:** Importância alta só mostra que \_\_\_\_ foi útil para a árvore separar os dados de treino; \_\_\_\_ e \_\_\_\_ empatam em \_\_\_\_, então trocar o `random_state` ou acrescentar publicações poderia inverter o ranking.
