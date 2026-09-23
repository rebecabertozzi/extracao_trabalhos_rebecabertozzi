# 03 — Agrupar e montar tabelas

**Quando usar:** "monte uma tabela por tema com...", "número de publicações e
mediana de...", "uma linha para cada combinação de tema e formato", "ordenada
da maior para a menor", "por hashtag". No template: **seção 6**.

## Uma categoria

```python
resumo = (
    df.groupby("tema")["taxa_utilidade_pct"]           # <-- grupo e coluna
    .agg(publicacoes="count", mediana="median")         # <-- o que calcular
    .sort_values("mediana", ascending=False)
)
print(resumo)
```

O `.agg(nome="funcao")` já nomeia as colunas do jeito que você quer — evita
sair um `MultiIndex` feio que atrapalha na hora de plotar.

Funções mais usadas: `"count"`, `"mean"`, `"median"`, `"sum"`, `"min"`,
`"max"`, `"std"`, `"nunique"`.

## Duas categorias (tema × formato)

```python
resumo2 = (
    df.groupby(["tema", "formato"])["taxa_engajamento_pct"]
    .agg(publicacoes="count", mediana="median")
    .sort_values("mediana", ascending=False)
    .reset_index()
)
print(resumo2)
```

`.reset_index()` transforma `tema` e `formato` de índice em colunas normais —
necessário pra plotar e pra montar rótulos combinados.

### Versão em matriz (mais fácil de ler)

```python
tabela = df.pivot_table(
    index="tema", columns="formato",
    values="taxa_engajamento_pct", aggfunc="median"
).round(2)
print(tabela)
```

Saída fica assim, ótima pra enxergar padrão:

```
formato     carrossel  imagem  reel  video
tema
Cultura          7.80    7.37  8.71   8.27
Mobilidade       5.86   11.11  6.84   7.33
```

O enunciado geralmente pede "uma linha para cada combinação" → use o
`groupby` + `reset_index`. Mas você pode **mostrar os dois** (a lista ordenada
e a matriz); custa uma linha e mostra domínio.

## Agregar colunas diferentes com funções diferentes

```python
diario = (
    df.groupby("dia_publicacao")
    .agg(
        publicacoes=("id_publicacao", "count"),
        engajamento_medio=("taxa_engajamento_pct", "mean"),
        alcance_total=("alcance", "sum"),
    )
    .sort_index()
)
```

Essa forma — `nome=("coluna", "funcao")` — é a da Aula 5, a mais flexível e a
que resolve quase todo enunciado. Guarde ela.

## Por hashtag (Aula 5): `explode`

Cada post tem várias hashtags numa string só (`"cultura,festival,rio"`). Para
agrupar por hashtag, cada uma precisa virar uma linha:

```python
tags = df.dropna(subset=["hashtags"]).copy()                 # sem hashtag não há o que explodir
tags["hashtags"] = tags["hashtags"].str.split(",")           # "a,b,c" -> ["a", "b", "c"]
tags = tags.explode("hashtags")                              # uma linha por hashtag
tags["hashtags"] = tags["hashtags"].str.strip().str.lower()  # "Futebol" e "futebol" viram uma só

resumo_tags = (
    tags.groupby("hashtags")
    .agg(qtd_posts=("id_publicacao", "count"),
         engajamento_medio=("taxa_engajamento_pct", "mean"))
    .sort_values("engajamento_medio", ascending=False)
)
print(f"linhas antes: {len(df)} | depois do explode: {len(tags)}")
```

- O número de linhas **aumenta** (um post com 3 hashtags aparece 3 vezes). É o esperado.
- Alerta da Aula 6: o topo por engajamento médio costuma vir cheio de hashtags com 1 ou 2 posts — um vídeo que performou bem "arrasta" a média. Olhe `qtd_posts` antes de concluir.
- `str.contains("ia")` para buscar hashtag é armadilha: pega "not**ícia**s", "pol**ít**ica"... Depois do `explode`, compare com `==`.

## Tabela de relatório (nomes em português, taxa em %)

```python
tabela_final = resumo_tags.reset_index().rename(columns={
    "hashtags": "Hashtag", "qtd_posts": "Qtd. de posts", "engajamento_medio": "Engajamento médio (%)",
})
tabela_final.head(10)
```

## Ordenar

```python
.sort_values("mediana", ascending=False)   # maior → menor
.sort_values("mediana")                    # menor → maior
.sort_index()                              # pela chave do grupo (útil p/ data)
.sort_values(["tema", "mediana"], ascending=[True, False])   # dois critérios
```

## Contagens rápidas

```python
df["tema"].value_counts()                       # quantas por tema
df["tema"].value_counts(normalize=True) * 100   # em %
pd.crosstab(df["tema"], df["formato"])          # contagem cruzada
```

## Armadilhas

- **Mediana ≠ média.** Se pediu mediana, `median()`. Se pediu média, `mean()`.
  Errar isso muda o resultado e a resposta escrita.
- `count()` ignora ausentes daquela coluna; `size()` conta todas as linhas do
  grupo. Se a coluna tiver `NaN`, os dois dão números diferentes.
- Grupos com **poucas publicações** (2, 3 registros) produzem mediana instável
  — vale citar como limitação na resposta escrita. Por isso o enunciado quase
  sempre pede a **contagem junto** com a mediana: é pra você notar isso.
- Se o `groupby` devolver mais categorias do que deveria (ex: 7 temas quando
  são 4), você esqueceu de padronizar o texto → volte ao `02-limpeza.md`.
