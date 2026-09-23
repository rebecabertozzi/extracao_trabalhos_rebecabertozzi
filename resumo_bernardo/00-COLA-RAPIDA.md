# 00 — Cola rápida

Os snippets mais usados, numa página, com os nomes de coluna do simulado. `# <--` marca o que trocar. A versão completa (com diagnóstico, log de limpeza e os números para a resposta) está no `prova-template.ipynb`.

## Imports

```python
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import (
    mean_absolute_error, r2_score,
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, ConfusionMatrixDisplay, silhouette_score,
)

pd.set_option("display.max_columns", None)
FONTE = "Fonte: dados sintéticos do Festival ViraBairro (2026)"   # <-- troque
```

## Conhecer a base

```python
df = pd.read_csv("dados/publicacoes_brutas.csv")     # <-- troque (export das aulas: sep=";")
print(df.head())
print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")
a = df.isna().sum()
print(a[a > 0])                                      # SÓ as colunas com ausência
print(df.dtypes)
print(df["tema"].unique())                           # grafias inconsistentes?
print(df.duplicated(subset="id_publicacao").sum())   # duplicatas pelo id
```

## Limpeza

```python
df = df.drop_duplicates(subset="id_publicacao").copy()
df["tema"] = df["tema"].str.strip().str.lower().str.title()
df["formato"] = df["formato"].str.strip().str.lower()
for col in ["alcance", "compartilhamentos", "salvamentos"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")   # texto que não é número vira NaN

# DATAS MISTURADAS: ISO separado (no pandas 3, o método da Aula 10 sozinho inverte dia/mês das ISO com dia <= 12)
PANDAS_2 = int(pd.__version__.split(".")[0]) >= 2
def converter_data(serie):
    texto = serie.astype("string").str.strip()
    eh_iso = texto.str.match(r"\d{4}-\d{2}-\d{2}").fillna(False).astype(bool)
    if PANDAS_2:
        iso = pd.to_datetime(texto.where(eh_iso), format="ISO8601", errors="coerce")
        outros = pd.to_datetime(texto.where(~eh_iso), format="mixed", dayfirst=True, errors="coerce")
    else:
        iso = pd.to_datetime(texto.where(eh_iso), errors="coerce")
        outros = pd.to_datetime(texto.where(~eh_iso), dayfirst=True, errors="coerce")
    return iso.fillna(outros)

df["data_publicacao"] = converter_data(df["data_publicacao"])
print(df["data_publicacao"].isna().sum(), df["data_publicacao"].min(), df["data_publicacao"].max())   # CONFIRA

df = df[df["alcance"] > 0].copy()                    # denominador inválido (NaN, 0, negativo) sai
df["compartilhamentos"] = df["compartilhamentos"].fillna(df["compartilhamentos"].median())
```

## Taxa e tabela por grupo

```python
df["taxa_utilidade_pct"] = (df["compartilhamentos"] + df["salvamentos"]) / df["alcance"] * 100   # <-- fórmula do enunciado

resumo = (df.groupby("tema")["taxa_utilidade_pct"]
          .agg(publicacoes="count", mediana="median")
          .sort_values("mediana", ascending=False))

resumo2 = (df.groupby(["tema", "formato"])["taxa_engajamento_pct"]
           .agg(publicacoes="count", mediana="median")
           .sort_values("mediana", ascending=False)
           .reset_index())

# hashtags (Aula 5): uma linha por hashtag
tags = df.dropna(subset=["hashtags"]).copy()
tags["hashtags"] = tags["hashtags"].str.split(",")
tags = tags.explode("hashtags")
tags["hashtags"] = tags["hashtags"].str.strip().str.lower()
por_tag = tags.groupby("hashtags").agg(qtd_posts=("id_publicacao", "count"),
                                      engajamento_medio=("taxa_engajamento_pct", "mean"))
```

## Gráficos (título + eixos + fonte, no estilo das aulas)

```python
# barras
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(resumo.index, resumo["mediana"], color="#3b6ea5")
ax.set_title("Qual tema as pessoas mais salvam ou compartilham?")
ax.set_xlabel("Tema"); ax.set_ylabel("Mediana da taxa de utilidade (%)")
fig.text(0.01, -0.02, FONTE, fontsize=8, color="gray")
fig.tight_layout(); plt.show()

# linha (por dia)
df["dia_publicacao"] = df["data_publicacao"].dt.date
diario = (df.groupby("dia_publicacao")
          .agg(publicacoes=("id_publicacao", "count"),
               engajamento_medio=("taxa_engajamento_pct", "mean"),
               alcance_total=("alcance", "sum"))
          .sort_index())
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(diario.index, diario["engajamento_medio"], marker="o", color="#c0392b")
ax.set_title("Taxa média de engajamento por dia")
ax.set_xlabel("Dia"); ax.set_ylabel("Taxa média de engajamento (%)")
ax.tick_params(axis="x", rotation=30)
fig.text(0.01, -0.02, FONTE, fontsize=8, color="gray")
fig.tight_layout(); plt.show()
```

## Recorte e top N

```python
rec = df[(df["formato"] == "reel") & (df["hora"] >= 18)]     # cada condição entre ( ); "a partir de" = >=
rec.nlargest(5, "taxa_engajamento_pct")[["id_publicacao", "dia_publicacao", "hora", "tema", "taxa_engajamento_pct"]]
```

## Features sem vazamento

```python
FEATURES = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
            "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]    # <-- as permitidas
X = pd.get_dummies(df[FEATURES], columns=["tema", "formato"], drop_first=True, dtype=int)
```

## Regressão (prever número) — sempre com o modelo bobo

```python
y = df["taxa_engajamento_pct"]
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42)

modelos_reg = {
    "Modelo bobo (média)": DummyRegressor(strategy="mean"),
    "Regressão linear": LinearRegression(),
    "Árvore de regressão": DecisionTreeRegressor(max_depth=4, random_state=42),
}
tab_reg = pd.DataFrame([{"modelo": n,
                         "MAE": mean_absolute_error(yte, m.fit(Xtr, ytr).predict(Xte)),
                         "R2": r2_score(yte, m.predict(Xte))}
                        for n, m in modelos_reg.items()]).sort_values("MAE")
```

## Classificação (prever categoria)

```python
limite = df["taxa_engajamento_pct"].quantile(0.75)
y = (df["taxa_engajamento_pct"] > limite).astype(int)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

modelos = {
    "Regressão logística": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced")),
    "Árvore de classificação": DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(random_state=42, class_weight="balanced"),
}
for m in modelos.values():
    m.fit(Xtr, ytr)

tab = pd.DataFrame([{"modelo": n,
                     "precisao": precision_score(yte, m.predict(Xte), zero_division=0),
                     "recall": recall_score(yte, m.predict(Xte), zero_division=0),
                     "f1": f1_score(yte, m.predict(Xte), zero_division=0)}
                    for n, m in modelos.items()]).sort_values("f1", ascending=False)

melhor = modelos[tab.iloc[0]["modelo"]]
ConfusionMatrixDisplay(confusion_matrix(yte, melhor.predict(Xte)), display_labels=["Não", "Sim"]).plot()
plt.show()

prob = modelos["Regressão logística"].predict_proba(Xte)[:, 1]      # modelo JÁ ajustado
cortes = pd.DataFrame([{"corte": c,
                        "precisao": precision_score(yte, (prob >= c).astype(int), zero_division=0),
                        "recall": recall_score(yte, (prob >= c).astype(int), zero_division=0),
                        "f1": f1_score(yte, (prob >= c).astype(int), zero_division=0)}
                       for c in [0.50, 0.30]])

imp = pd.Series(modelos["Árvore de classificação"].feature_importances_,
                index=Xtr.columns).sort_values(ascending=False)
```

## Clusterização (agrupar sem rótulo)

```python
cols = ["seguidores_autor", "tamanho_legenda", "n_hashtags", "taxa_engajamento_pct"]   # <-- troque
base = df[cols].dropna().copy()
entrada = base.copy()
entrada["seguidores_autor"] = np.log1p(entrada["seguidores_autor"])   # cauda longa: log antes
Xs = StandardScaler().fit_transform(entrada)                          # padronizar é obrigatório

for k in range(2, 8):
    km = KMeans(n_clusters=k, random_state=42, n_init=10).fit(Xs)
    print(k, round(km.inertia_, 1), round(silhouette_score(Xs, km.labels_), 3))

base["cluster"] = KMeans(n_clusters=3, random_state=42, n_init=10).fit_predict(Xs)   # <-- k escolhido
print(base.groupby("cluster").mean().round(2))
```

## As 3 palavras-chave da resposta escrita

- **"associado a"**, nunca "causa".
- **"mediana"** = valor típico, menos sensível a extremos que a média.
- **"limitação"**: base sintética, período curto, poucos registros por grupo, variáveis não observadas.
