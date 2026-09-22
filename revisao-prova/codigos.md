[codigos.md](https://github.com/user-attachments/files/32540960/codigos.md)
# Códigos — quando e como usar

Todo código aqui vem das aulas ou da resolução do simulado, e foi testado na base do simulado. Em cada bloco: **Quando usar** (as palavras do enunciado), **Como usar** (o que trocar) e **Cuidado** (a armadilha). `# TROQUE` marca a linha que você adapta. O que cada termo significa está em **conceitos.md**.

| A questão pede | Vá para | Simulado |
| --- | --- | --- |
| abrir, primeiras linhas, linhas e colunas, ausentes | [1](#1-abrir-e-olhar-a-base) | Q1 |
| duplicidade, padronizar, datas, tratar ausentes, criar taxa | [2](#2-limpar-a-base) | Q2 |
| tabela por tema, mediana, gráfico de barras | [3](#3-tabela-por-grupo-e-gráfico-de-barras) | Q2, Q3, Q5 |
| por dia, gráfico de linhas, recorte, cinco maiores | [4](#4-por-dia-recorte-e-top-5) | Q4 |
| características, transformar categorias, treino e teste | [5](#5-preparar-o-modelo) | Q6, Q7, Q8 |
| estimar um número, MAE, R², real x previsto | [6](#6-regressão) | Q7 |
| três classificadores, precisão, recall, F1, matriz, cortes | [7](#7-classificação-e-corte) | Q8 |
| importância, características mais usadas | [8](#8-importâncias-da-árvore) | Q6 |
| coisas das aulas que não caíram no simulado | [9](#9-extras-das-aulas) | — |

## 1. Abrir e olhar a base

**Quando usar:** sempre, no começo de toda questão. É também a Q1 inteira ("cinco primeiras linhas", "quantidade de linhas e colunas", "ausentes por coluna").

**Como usar:** troque o nome do arquivo pelo que o enunciado diz. Os imports rodam uma vez só na prova.

**Cuidado:** se pedir "somente as colunas com ausência", use a última linha. `isna().sum()` puro mostra também as que têm zero.

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("dados/ARQUIVO.csv")   # TROQUE
print(df.head())                        # 5 primeiras linhas
print(df.shape)                         # (linhas, colunas)
print(df.dtypes)                        # tipo de cada coluna
ausentes = df.isna().sum()
print(ausentes[ausentes > 0])           # só colunas com ausência
```

## 2. Limpar a base

**Quando usar:** "tratamento", "prepare os dados", "duplicidade", "padronizar", "formatos distintos", "converter", "tratar ausências", "crie a taxa". É a Q2.

**Como usar:** rode por partes e **olhe cada print** antes de decidir o próximo passo. O `value_counts` mostra quais grafias você precisa juntar no `replace`. Os prints de `NaT`, dtypes e "descartadas" são o que você escreve na resposta.

**Cuidado:**
- Duplicidade "por id" precisa do `subset`.
- `lower` não junta `saúde` e `saude`: pra isso serve o `replace`.
- Data misturada vai em duas passadas. Confira a menor e a maior data.
- Só descarte linha por campo que entra na fórmula.
- Não escreva que tratou algo que derrubou 0 linhas, nem que "converteu texto" se os dtypes já eram número.

```python
df = pd.read_csv("dados/publicacoes_brutas.csv")          # variável nova, do bruto
# a) duplicidade por id
print(df[df.duplicated(subset="id_publicacao", keep=False)])   # as cópias lado a lado
print("duplicadas:", df.duplicated(subset="id_publicacao").sum())
df = df.drop_duplicates(subset="id_publicacao", keep="first")
# b) padronizar texto
df["tema"] = df["tema"].str.strip().str.lower()
print(df["tema"].value_counts(dropna=False))
df["tema"] = df["tema"].replace({"saúde": "saude"})        # TROQUE conforme o value_counts
# c) data em duas passadas
ano_primeiro = df["data_publicacao"].str[:4].str.isdigit().fillna(False)
iso = pd.to_datetime(df["data_publicacao"].where(ano_primeiro), format="ISO8601", errors="coerce")
br = pd.to_datetime(df["data_publicacao"].where(~ano_primeiro), format="mixed", dayfirst=True, errors="coerce")
df["data_publicacao"] = iso.fillna(br)
print("NaT:", df["data_publicacao"].isna().sum(), "| de", df["data_publicacao"].min(), "até", df["data_publicacao"].max())
# d) números: olhar o tipo antes
cols = ["alcance", "compartilhamentos", "salvamentos"]       # TROQUE: colunas da fórmula
print(df[cols].dtypes)
for c in cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")
# e) ausentes e inválidos
antes = len(df)
df = df.dropna(subset=cols)                                  # sem esses campos a taxa não existe
df = df[df["alcance"] > 0]                                   # alcance zero quebra a divisão
print("descartadas:", antes - len(df), "| restam:", len(df))
# f) a taxa
df["taxa_utilidade_pct"] = (df["compartilhamentos"] + df["salvamentos"]) / df["alcance"] * 100   # TROQUE: fórmula
```

## 3. Tabela por grupo e gráfico de barras

**Quando usar:** "tabela por tema", "número de publicações e mediana", "compare os temas", "gráfico de barras". Com "combinação de tema e formato", use duas colunas.

**Como usar:** troque a coluna do grupo, a coluna do valor e a função: `"median"` pra mediana, `"mean"` pra média, `"sum"` pra total. O título tem que dizer a pergunta.

**Cuidado:**
- Com duas colunas, crie um rótulo juntando as duas e use `barh` (horizontal), senão os nomes se sobrepõem.
- Na resposta, olhe a coluna `publicacoes`: poucos casos e diferença pequena é empate.

```python
tabela = (df.groupby("tema")                                   # TROQUE: ou ["tema", "formato"]
            .agg(publicacoes=("id_publicacao", "count"),
                 mediana=("taxa_utilidade_pct", "median"))      # TROQUE: coluna e função
            .reset_index()
            .sort_values("mediana", ascending=False)            # da maior pra menor
            .round(2))
print(tabela.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tabela["tema"], tabela["mediana"])
ax.set_title("Qual tema as pessoas mais salvam e compartilham?")   # TROQUE
ax.set_xlabel("Tema")
ax.set_ylabel("Mediana da taxa (%)")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()

# com duas colunas (Q5):
# tabela["combinacao"] = tabela["tema"] + " / " + tabela["formato"]
# ax.barh(tabela["combinacao"][::-1], tabela["mediana"][::-1])    # [::-1] põe o maior no topo
# no barh o valor fica no eixo X: set_xlabel("Mediana (%)"), set_ylabel("Tema / formato")
```

## 4. Por dia, recorte e top 5

**Quando usar:** "crie dia_publicacao", "por dia", "ordem cronológica", "gráfico de linhas", "recorte apenas de...", "as cinco com maior...". É a Q4.

**Como usar:** a base de análise já tem a data num formato só, então basta `pd.to_datetime`. Troque as condições do recorte e as colunas pedidas no top 5.

**Cuidado:**
- No filtro com duas condições, cada uma vai entre parênteses, ligadas por `&` (e) ou `|` (ou). Nunca use `and`.
- "A partir das 18h" é `>=`.
- Na resposta, fale em variação e não em tendência. O top 5 não prova causa.

```python
df = pd.read_csv("dados/publicacoes_analise.csv")
df["data_publicacao"] = pd.to_datetime(df["data_publicacao"])
df["dia_publicacao"] = df["data_publicacao"].dt.date            # só a data
diaria = (df.groupby("dia_publicacao")
            .agg(publicacoes=("id_publicacao", "count"),
                 media=("taxa_engajamento_pct", "mean"),
                 alcance_total=("alcance", "sum"))
            .reset_index()
            .sort_values("dia_publicacao"))                      # cronológica
print(diaria)

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(diaria["dia_publicacao"], diaria["media"], marker="o")
ax.set_title("Como a taxa média de engajamento variou dia a dia")
ax.set_xlabel("Dia da publicação")
ax.set_ylabel("Taxa média de engajamento (%)")
ax.tick_params(axis="x", rotation=45)                           # datas legíveis
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()

recorte = df[(df["formato"] == "reel") & (df["hora"] >= 18)]    # TROQUE: condições
print(len(recorte))
print(recorte.nlargest(5, "taxa_engajamento_pct")[
    ["id_publicacao", "dia_publicacao", "hora", "tema", "taxa_engajamento_pct"]])   # TROQUE: colunas pedidas
```

## 5. Preparar o modelo

**Quando usar:** antes de qualquer modelo (Q6, Q7, Q8): "use apenas as características...", "transforme categorias em números", "reserve 75% para treino e 25% para teste".

**Como usar:** copie a lista de características do enunciado. Depois escolha **um** dos dois blocos de baixo: regressão, se o alvo é número, ou classificação, se o alvo é 0/1.

**Cuidado:**
- Sem `get_dummies` dá `could not convert string to float`.
- Nunca ponha alcance, curtidas, compartilhamentos, salvamentos, a taxa ou o id no X (vazamento).
- `stratify=y` **só** na classificação.

```python
from sklearn.model_selection import train_test_split
df = pd.read_csv("dados/publicacoes_analise.csv")
CARACTERISTICAS = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
                   "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]   # TROQUE: lista do enunciado
X = pd.get_dummies(df[CARACTERISTICAS], columns=["tema", "formato"])   # texto vira colunas 0/1

# REGRESSÃO (alvo é número):
y = df["taxa_engajamento_pct"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42)

# CLASSIFICAÇÃO (alvo 0/1 pelo percentil 75):
corte = df["taxa_engajamento_pct"].quantile(0.75)
y = (df["taxa_engajamento_pct"] > corte).astype(int)             # 1 acima do corte, 0 o resto
print("corte:", corte, "| positivos:", y.sum(), "de", len(y))
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
```

## 6. Regressão

**Quando usar:** "estimar a taxa", "regressão linear e árvore de regressão", "MAE e R²", "valores reais e previstos". É a Q7. Rode depois da parte REGRESSÃO do bloco 5.

**Como usar:** a tabela compara os modelos. Escolha o de **menor MAE** e use a previsão dele no gráfico.

**Cuidado:**
- O modelo bobo não é pedido, mas é ele que mostra se o modelo aprendeu alguma coisa.
- Na resposta, traduza o MAE pra unidade do alvo ("erra cerca de 0,35 ponto percentual").

```python
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score
prev_lin = LinearRegression().fit(X_treino, y_treino).predict(X_teste)
prev_arv = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_treino, y_treino).predict(X_teste)
prev_bobo = np.full(len(y_teste), y_treino.mean())              # chuta sempre a média
print(pd.DataFrame({"modelo": ["bobo", "linear", "árvore"],
                    "MAE": [mean_absolute_error(y_teste, p) for p in (prev_bobo, prev_lin, prev_arv)],
                    "R2":  [r2_score(y_teste, p) for p in (prev_bobo, prev_lin, prev_arv)]}).round(3))

previsao = prev_lin                                              # TROQUE: o de menor MAE
fig, ax = plt.subplots(figsize=(6.5, 6))
ax.scatter(y_teste, previsao, alpha=0.5)
minimo = float(min(y_teste.min(), previsao.min()))
maximo = float(max(y_teste.max(), previsao.max()))
ax.plot([minimo, maximo], [minimo, maximo], linestyle="--", color="red", label="previsão = valor real")
ax.set_title("Valor real x valor previsto")
ax.set_xlabel("Taxa real (%)")
ax.set_ylabel("Taxa prevista (%)")
ax.legend()
plt.show()
```

## 7. Classificação e corte

**Quando usar:** "merece divulgação", "escolha três classificadores", "precisão, recall e F1", "matriz de confusão do modelo com maior F1", "compare os cortes 0,50 e 0,30". É a Q8. Rode depois da parte CLASSIFICAÇÃO do bloco 5.

**Como usar:** a tabela sai ordenada por F1, e a matriz é do primeiro colocado. O laço do fim compara os cortes na logística.

**Cuidado:**
- A logística é obrigatória, porque o corte é mexido nela.
- A matriz sai como `[[VN FP] [FN VP]]`.
- O `ConvergenceWarning` é só aviso.
- Na resposta, diga o que FP e FN significam no caso (gastar divulgação à toa / deixar passar peça boa).

```python
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
modelos = {"logística": LogisticRegression(max_iter=5000),
           "árvore": DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced"),
           "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")}
linhas = []
for nome, m in modelos.items():
    d = m.fit(X_treino, y_treino).predict(X_teste)
    linhas.append({"modelo": nome,
                   "precisão": precision_score(y_teste, d, zero_division=0),
                   "recall": recall_score(y_teste, d, zero_division=0),
                   "F1": f1_score(y_teste, d, zero_division=0)})
tabela = pd.DataFrame(linhas).sort_values("F1", ascending=False).round(3)
print(tabela)
print(confusion_matrix(y_teste, modelos[tabela.iloc[0]["modelo"]].predict(X_teste)))

prob = modelos["logística"].predict_proba(X_teste)[:, 1]        # probabilidade de ser 1
for c in [0.50, 0.30]:                                           # TROQUE: cortes pedidos
    d = (prob >= c).astype(int)
    print(c, precision_score(y_teste, d, zero_division=0),
          recall_score(y_teste, d, zero_division=0), f1_score(y_teste, d, zero_division=0))
```

## 8. Importâncias da árvore

**Quando usar:** "quais características a árvore usou mais", "cinco de maior importância", "gráfico de barras horizontal". É a Q6. Rode depois da parte CLASSIFICAÇÃO do bloco 5.

**Como usar:** copie os parâmetros da árvore que o enunciado der (profundidade, `random_state`, pesos balanceados).

**Cuidado:**
- Importância não é causa.
- Se duas estão quase iguais, diga que o ranking é instável.

```python
from sklearn.tree import DecisionTreeClassifier
arvore = DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced").fit(X_treino, y_treino)
top5 = (pd.DataFrame({"caracteristica": X.columns, "importancia": arvore.feature_importances_})
          .sort_values("importancia", ascending=False)
          .head(5))
print(top5)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(top5["caracteristica"][::-1], top5["importancia"][::-1])
ax.set_title("O que a árvore mais usou para separar as publicações")
ax.set_xlabel("Importância (0 a 1)")
ax.set_ylabel("Característica")
fig.tight_layout()
plt.show()
```

## 9. Extras das aulas

Não caíram no simulado, mas estão nas aulas 5, 6 e 10 e podem aparecer.

| Quando o enunciado pede | Código | Aula |
| --- | --- | --- |
| resumo estatístico, média, mediana | `df["coluna"].describe()`, `.mean()`, `.median()` | 5 |
| filtrar por uma condição | `df[df["likes"] >= 5000]` | 5 |
| filtrar por um texto dentro da coluna | `df[df["hashtags"].str.contains("futebol", na=False)]` | 5 |
| contar quantas vezes cada valor aparece | `df["coluna"].value_counts()` | 5 |
| separar hashtags "a,b" em linhas | `df["hashtags"].str.split(",")` e depois `df.explode("hashtags")` | 5 |
| dispersão de dois números | `ax.scatter(df["x"], df["y"], alpha=0.6)`; se os valores forem muito espalhados, `ax.set_xscale("log")` | 6 |
| tirar símbolo de texto antes de converter | `df["preco"].str.replace("£", "", regex=False)` | 10 |
| preencher ausente | `df["coluna"].fillna(0)` (só se 0 não fingir ser dado real) | 10 |
| primeira letra maiúscula | `.str.title()` | 10 |
