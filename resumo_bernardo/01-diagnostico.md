# 01 — Diagnóstico inicial da base

**Quando usar:** o enunciado pede pra "conhecer" a base antes de mexer nela —
primeiras linhas, quantidade de linhas/colunas, valores ausentes por coluna.
No template: **seção 3** (que também avisa quais colunas de texto deveriam ser número).

## Template completo

```python
import pandas as pd

df = pd.read_csv("dados/publicacoes_brutas.csv")   # <-- caminho do enunciado

# 1. cinco primeiras linhas
print(df.head())

# 2. quantidade de linhas e colunas
print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")

# 3. ausências por coluna — SOMENTE as que têm ao menos uma
ausencias = df.isna().sum()
print(ausencias[ausencias > 0])
```

O filtro `ausencias[ausencias > 0]` é cobrado literalmente quando o
enunciado diz "somente as colunas que têm ao menos uma ausência". Imprimir a
série inteira com zeros conta como incompleto.

## Reconhecimento rápido (faça antes de limpar qualquer coisa)

```python
df.dtypes                              # o que veio como texto e deveria ser número/data?
df["tema"].unique()                    # quais grafias diferentes existem?
df["tema"].value_counts(dropna=False)  # quantas de cada, incluindo ausentes
df.duplicated(subset="id_publicacao").sum()   # tem duplicata?
df.describe()                          # min/max ajudam a achar valor inválido (negativo, zero)
```

Esses cinco comandos respondem sozinhos quase todo "diagnóstico" e ainda te
dizem **o que** você vai precisar limpar na questão seguinte. Vale rodar
mesmo quando o enunciado não pede — leva 10 segundos e evita erro depois.

### Como achar valor inválido que não é ausente

Ausente (`NaN`) e inválido são coisas diferentes: `isna()` não pega alcance
negativo, zero indevido ou string vazia.

```python
print((pd.to_numeric(df["alcance"], errors="coerce") <= 0).sum())   # zeros e negativos (funciona mesmo se veio como texto)
print(df.select_dtypes("object").columns)     # colunas que ficaram como texto
print((df["tema"].str.strip() == "").sum())   # strings vazias
```

## Resposta escrita típica ("limite de representatividade")

A pergunta é sobre os **dados**, não sobre o código. Modelo:

> A base cobre apenas oito semanas de um único festival fictício, com
> publicações de um conjunto restrito de perfis e plataformas, então os
> padrões observados não podem ser generalizados para outras redes, públicos
> ou bairros.

Peças que valem ponto nessa resposta: **recorte temporal curto**, **fonte
única / dados sintéticos**, **não é amostra aleatória de nada**.

## Armadilhas

- `df.shape` retorna uma tupla — `df.shape[0]` são linhas, `[1]` colunas.
- Se o CSV usar `;` como separador ou vírgula decimal:
  `pd.read_csv(arq, sep=";", decimal=",")`.
- Se aparecer acento quebrado: `pd.read_csv(arq, encoding="latin-1")`.
- `df.head()` dentro de `print()` some com a formatação bonita; se quiser a
  tabela formatada, deixe `df.head()` sozinho na **última linha** da célula.
