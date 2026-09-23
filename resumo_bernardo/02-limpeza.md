# 02 — Limpeza e tratamento

**Quando usar:** base "suja" (`*_brutas.csv`) — duplicata, grafia inconsistente, tipo errado, ausência, valor inválido, coluna calculada. No template: **seções 4 e 5** (a célula `[NÃO COLE]` da seção 4 imprime os números de cada decisão para a resposta).

## Ordem

1. duplicata → 2. texto → 3. números → 4. datas → 5. inválidos e ausentes → 6. coluna calculada → 7. **conferir**

Criar a taxa antes de tratar o denominador gera `inf`. Converter antes de tirar duplicata só desperdiça trabalho.

Postura da Aula 10: nunca mexa no bruto — trabalhe numa cópia (`df = df_bruto.copy()`) e registre cada decisão com o número de linhas afetadas.

---

## 1. Duplicata

```python
antes = len(df)
df = df.drop_duplicates(subset="id_publicacao").copy()   # <-- coluna identificadora
print(f"{antes - len(df)} duplicatas removidas")
```

- `subset=` é o que o enunciado pede quando diz "duplicidade **por** id". Sem ele, só saem linhas 100% idênticas (é o que a Aula 5 faz com `df.drop_duplicates()`).
- `.copy()` evita o `SettingWithCopyWarning` nas edições seguintes. Sempre que filtrar e depois escrever no resultado, use `.copy()`.

## 2. Texto categórico

`"Saúde"`, `"saúde"` e `" SAÚDE "` contam como três temas no `groupby`.

```python
df["tema"] = df["tema"].str.strip().str.lower().str.title()    # "Primeira Maiúscula"
df["formato"] = df["formato"].str.strip().str.lower()          # "tudo minúsculo"
print(sorted(df["tema"].unique()))                             # CONFIRA: sobrou o número certo?
```

Grafias realmente diferentes (sinônimo, abreviação) não se resolvem com caixa — mapeie na mão, como a Aula 10 faz com `"Sci-Fi"` → `"Science Fiction"`:

```python
df["tema"] = df["tema"].replace({"Saude": "Saúde", "Mob.": "Mobilidade"})
```

Nunca adivinhe o mapa: rode `df["tema"].unique()` antes e escreva com base no que apareceu.

## 3. Números que vieram como texto

```python
for col in ["alcance", "compartilhamentos", "salvamentos"]:        # <-- troque
    df[col] = pd.to_numeric(df[col], errors="coerce")
```

`errors="coerce"`: o que não converte ("sem dado", "Grátis") vira `NaN` em vez de quebrar o código. Você trata no passo 5, de forma visível.

Se tiver símbolo junto (Aula 10: `"£51.77"`), tire antes:

```python
livros["preco"] = livros["preco"].str.replace("£", "", regex=False).str.strip()
livros["preco"] = pd.to_numeric(livros["preco"], errors="coerce")
# formato brasileiro "1.234,56":
# df["valor"] = df["valor"].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
```

## 4. Datas em formatos misturados — a armadilha nº 1

O simulado diz que há "datas em formatos distintos" (`2026-08-05` e `25/08/2026`). **Os jeitos óbvios erram sem dar erro, e o erro muda com a versão do pandas** (testado com 1.5, 2.2 e 3.0 — veja a sua com `print(pd.__version__)`):

| O que você escreve | O que acontece |
|---|---|
| `pd.to_datetime(s, errors="coerce")` | pandas 2 e 3: adivinha o formato pelo primeiro valor e transforma em `NaT` o que for diferente — perde linhas calado. pandas 1.5: inverte as `dd/mm` com dia ≤ 12 |
| `pd.to_datetime(s, format="mixed", dayfirst=True)` (**Aula 10**) | pandas 2.2: certo. **pandas 3: inverte dia e mês das ISO com dia ≤ 12** (`2026-08-05` vira 8 de maio). pandas 1.5: não existe, zera tudo sem avisar. Na aula não apareceu porque todas as datas tinham dia ≥ 20 |
| `pd.to_datetime(s, format="mixed")` | inverte as `dd/mm` com dia ≤ 12 |
| **ISO separado + método da aula no resto** | certo nas três versões |

O `requirements.txt` do curso não fixa versão, então quem instalou agora com `uv pip install` tem pandas 3 — justamente a versão em que o método da aula inverte as datas.

A forma correta (é a do template):

```python
PANDAS_2 = int(pd.__version__.split(".")[0]) >= 2

def converter_data(serie):
    texto = serie.astype("string").str.strip()
    eh_iso = texto.str.match(r"\d{4}-\d{2}-\d{2}").fillna(False).astype(bool)   # começa com AAAA-MM-DD
    if PANDAS_2:
        iso = pd.to_datetime(texto.where(eh_iso), format="ISO8601", errors="coerce")
        outros = pd.to_datetime(texto.where(~eh_iso), format="mixed", dayfirst=True, errors="coerce")
    else:                                   # pandas 1.x não tem format="mixed" (e não avisa: zera tudo)
        iso = pd.to_datetime(texto.where(eh_iso), errors="coerce")
        outros = pd.to_datetime(texto.where(~eh_iso), dayfirst=True, errors="coerce")
    return iso.fillna(outros)

df["data_publicacao"] = converter_data(df["data_publicacao"])
```

Aceita `2026-08-05`, `2026-08-05 14:30`, `05/08/2026`, `21-08-2026`, `22-Aug-2026`. Data impossível (`2026-08-35`, `31/02/2026`) vira `NaT`.

**Confira sempre:**

```python
print("não convertidas:", df["data_publicacao"].isna().sum())
print(df["data_publicacao"].min(), "->", df["data_publicacao"].max())
```

Se aparecer mês fora do período do enunciado (janeiro numa campanha de agosto), a conversão inverteu dia e mês.

## 5. Inválidos e ausentes

Não existe resposta única (Aula 10): **descartar**, **preencher** ou **manter como ausente e documentar**. O que vale ponto é justificar.

```python
# denominador de taxa: zero, negativo ou ausente -> descarta (NaN > 0 é False, então sai junto)
df = df[df["alcance"] > 0].copy()

# campo essencial ausente -> descarta
df = df.dropna(subset=["id_publicacao"])

# parcela de uma soma -> preencher com a mediana é defensável
df["compartilhamentos"] = df["compartilhamentos"].fillna(df["compartilhamentos"].median())
```

Valor que existe, no tipo certo, mas fora do possível (Aula 10: avaliação vai de 1 a 5 estrelas; veio um 7). Nenhum `isna()` pega isso — só a regra do domínio:

```python
fora = (livros["avaliacao"] < 1) | (livros["avaliacao"] > 5)
print(f"{fora.sum()} avaliações fora de 1-5")
livros.loc[fora, "avaliacao"] = np.nan          # mantém a linha, marca o valor como ausente
```

- Mediana, não média: é menos sensível a extremos e mais fácil de justificar.
- `fillna(0)` em contagem afirma "teve zero" — diferente de "não sabemos". Só use com justificativa (a Aula 10 usa 0 como marcador explícito de "sem avaliação registrada").

## 6. Coluna calculada

```python
df["taxa_utilidade_pct"] = (df["compartilhamentos"] + df["salvamentos"]) / df["alcance"] * 100
```

Monte exatamente a fórmula do enunciado: numerador **entre parênteses**, divide, multiplica por 100 no fim. Se o denominador pudesse ser zero e você não tratou, sai `inf` — que **não** aparece em `isna()`:

```python
print(np.isinf(df["taxa_utilidade_pct"]).sum())
```

## 7. Conferir (10 segundos que salvam a questão)

```python
print(df.shape)
print(sorted(df["tema"].unique()))
print(df.dtypes)
print(df["taxa_utilidade_pct"].describe())
```

Taxa negativa, acima de 100% ou `inf` = algo errado no tratamento.

Validação no estilo da Aula 10 (para se a prova pedir "valide as colunas obrigatórias"):

```python
for coluna in ["id_publicacao", "tema", "alcance", "data_publicacao"]:
    if coluna not in df.columns:
        raise ValueError(f"Coluna obrigatória ausente: {coluna}")
    if df[coluna].isna().all():
        raise ValueError(f"Coluna obrigatória totalmente vazia: {coluna}")
print("Validação de colunas obrigatórias: OK")
```

---

## Resposta escrita (decisões de tratamento)

Uma frase por decisão, sempre com o **porquê**. Os números estão na célula `[NÃO COLE]` da seção 4 do template (`>>> PARA A RESPOSTA`).

> Removi os registros duplicados por `id_publicacao` para não contar a mesma publicação duas vezes. Padronizei `tema` (espaços e caixa) porque a mesma categoria aparecia escrita de formas diferentes, o que dividiria os grupos. Converti as datas tratando separadamente os formatos presentes, para não perder nem inverter registros. Descartei as linhas com `alcance` ausente ou não positivo, já que sem denominador válido a taxa não pode ser calculada, e preenchi ausências de `compartilhamentos` com a mediana, por ser menos sensível a valores extremos que a média.
