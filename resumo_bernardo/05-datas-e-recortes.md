# 05 — Datas, série diária e recortes

**Quando usar:** "converta para data/hora", "crie `dia_publicacao`", "tabela
por dia", "recorte apenas de reels após as 18h", "as cinco com maior...".
No template: **seção 8**.

## Converter e extrair o dia

```python
df["data_publicacao"] = pd.to_datetime(df["data_publicacao"], errors="coerce")
df["dia_publicacao"] = df["data_publicacao"].dt.date
```

Se a base for a **bruta** (formatos misturados), esse jeito simples perde ou
inverte datas — use o `converter_data` do `02-limpeza.md` (seção 4 do
template). Na base `*_analise.csv` (já tratada) o formato é único e a linha
acima basta. Confira sempre: `df["data_publicacao"].isna().sum()` e
`.min()/.max()`.

## Coisas que se extraem de uma data

```python
df["data_publicacao"].dt.date          # só a data (vira objeto date)
df["data_publicacao"].dt.day           # dia do mês
df["data_publicacao"].dt.month         # mês
df["data_publicacao"].dt.hour          # hora
df["data_publicacao"].dt.dayofweek     # 0 = segunda ... 6 = domingo
df["data_publicacao"].dt.day_name()    # "Monday", "Tuesday"...
df["data_publicacao"].dt.isocalendar().week   # número da semana
df["data_publicacao"].dt.to_period("W")       # agrupar por semana
```

## Tabela por dia

```python
diario = (
    df.groupby("dia_publicacao")
    .agg(
        publicacoes=("id_publicacao", "count"),
        engajamento_medio=("taxa_engajamento_pct", "mean"),
        alcance_total=("alcance", "sum"),
    )
    .sort_index()      # ordena cronologicamente (a data é o índice)
)
print(diario)
```

Se você já tiver dado `.reset_index()`, troque por
`.sort_values("dia_publicacao")`.

Depois, o gráfico de linhas está em `04-graficos.md`.

## Recorte com condição

```python
recorte = df[(df["formato"] == "reel") & (df["hora"] >= 18)]
print(f"{len(recorte)} publicações no recorte")   # confira que não ficou vazio
```

Operadores: `&` = e, `|` = ou, `~` = não. **Cada condição entre parênteses**
(obrigatório no pandas).

Outros filtros úteis:
```python
df[df["tema"].isin(["Cultura", "Saúde"])]          # em uma lista
df[df["tema"].str.contains("Cult", na=False)]      # contém texto
df[df["data_publicacao"] >= "2026-09-01"]          # a partir de uma data
df[df["taxa_engajamento_pct"].between(5, 10)]     # intervalo (inclui as pontas)
```

## Top N

```python
top5 = recorte.nlargest(5, "taxa_engajamento_pct")[
    ["id_publicacao", "dia_publicacao", "hora", "tema", "taxa_engajamento_pct"]
]
print(top5)
```

`nlargest(5, "col")` ordena e corta em um passo. `nsmallest` faz o inverso.
Equivalente: `.sort_values("col", ascending=False).head(5)`.

A lista de colunas entre colchetes é exatamente a que o enunciado pedir —
ele costuma listar quais colunas mostrar.

## Resposta escrita típica

Dois pedidos quase certos:

**Descrever a variação sem afirmar tendência:**
> A taxa média de engajamento oscila entre os dias da campanha, com picos
> pontuais e sem um padrão consistente de alta ou queda. O período coberto é
> curto demais para caracterizar uma tendência de longo prazo.

**Explicar por que o recorte não prova causalidade:**
> O recorte de reels publicados após as 18h mostra publicações com
> engajamento alto, mas isso não demonstra que o horário ou o formato causem
> esse resultado: essas peças também diferem em tema, tamanho de legenda e
> perfil de autor, e não houve comparação controlada entre horários.

## Armadilhas

- `hora` pode vir como texto (`"18:00"`) → `pd.to_numeric(..., errors="coerce")`
  antes de comparar com número, ou extraia com `.dt.hour`.
- `.dt.date` devolve `object`, não datetime — bom pra agrupar e rotular, ruim
  pra ordenar por tempo se virar string. Como índice de `groupby` + `sort_index()`
  funciona certo.
- Recorte vazio (`len == 0`) geralmente é valor escrito diferente: cheque
  `df["formato"].unique()` — pode ser `"Reel"` e não `"reel"`.
- Ao filtrar e depois criar coluna, use `.copy()` pra evitar
  `SettingWithCopyWarning`.
