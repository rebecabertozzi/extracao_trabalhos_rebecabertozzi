[codigos (1).md](https://github.com/user-attachments/files/32544870/codigos.1.md)

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

### Mostrar na tela

O código só mostra o que você **manda mostrar**. Comandos que **fazem** algo (abrir, remover, converter) não aparecem na tela.

| Jeito | Como aparece |
| --- | --- |
| `print(coisa)` | como texto; use pra tudo que quiser ver no meio da célula |
| `coisa` sozinha **na última linha** da célula | como tabela bonita (só funciona na última linha) |

| Quero ver | Código |
| --- | --- |
| a tabela (5 primeiras linhas) | `print(q2.head())` |
| uma coluna inteira | `print(q2["tema"])` |
| resumo de uma coluna de texto (cada valor e quantas vezes) | `print(q2["tema"].value_counts())` |
| várias colunas | `print(q2[["coluna1", "coluna2"]].head())` (dois colchetes) |
| quantas linhas | `print(len(q2))` |
| o tipo das colunas | `print(q2.dtypes)` |
| menor e maior valor | `print(q2["coluna"].min(), q2["coluna"].max())` |

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
# a) duplicidade: veja o quadro "Duplicatas: com ou sem subset" logo abaixo
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

### Duplicatas: com ou sem `subset`

**Como pensar:** leia se o enunciado diz **"por alguma coluna"**.

| O enunciado diz | Use | O que conta como duplicata |
| --- | --- | --- |
| "remover duplicidade **por id_publicacao**" | com `subset` | o **id** se repete, mesmo que outra coluna esteja diferente |
| "remover registros duplicados", "linhas repetidas" (sem "por") | sem `subset` | a linha é **igualzinha em todas as colunas** |

**Com `subset`** (o enunciado disse "por id_publicacao"):

```python
print("duplicadas:", df.duplicated(subset="id_publicacao").sum())   # olhar: quantas tem
df = df.drop_duplicates(subset="id_publicacao", keep="first")       # consertar: remove, fica a 1ª
print("linhas depois:", len(df))                                    # olhar de novo
```

**Sem `subset`** (o enunciado só disse "duplicados"):

```python
print("duplicadas:", df.duplicated().sum())      # olhar: linhas iguais em todas as colunas
df = df.drop_duplicates()                        # consertar: remove, fica a 1ª
print("linhas depois:", len(df))                 # olhar de novo
```

O que cada parte faz:
- `duplicated()` marca cada linha com "é repetida?". O `.sum()` conta quantas são.
- `drop_duplicates()` remove as repetidas.
- `subset="coluna"` diz "pra decidir, olhe **só** esta coluna". Se o enunciado disser "por" outra coluna, troque o nome.
- `keep="first"` guarda a primeira vez que aparece e apaga as seguintes. Sem ele, o padrão já é esse.
- `df =` na frente salva a tabela já limpa. Sem isso, nada muda.
- `len(df)` conta as linhas, pra conferir quantas sobraram.

No simulado, os dois jeitos dão o mesmo resultado (36 → 35), porque as duas cópias do `OCB-018` são idênticas. Use o que o enunciado pedir.

### Padronizar texto (tema)

**Quando usar:** "padronizar", "forma consistente", "nomes escritos de formas diferentes".

**Qual é o problema:** o mesmo tema escrito de jeitos diferentes (`cultura`, `Cultura`, `"mobilidade "`, `Saúde`). Pro Python, qualquer letra ou espaço diferente vira outro tema. Aí a tabela por tema sai errada.

**Como pensar:** olhar → consertar → olhar de novo.

1. **Olhar** com `value_counts()`. Ele lista cada escrita diferente e quantas vezes aparece. Se o enunciado diz que são 4 temas e aparecem 7 linhas, sobram escritas erradas. As erradas costumam aparecer 1 vez só. Se um tema aparece **duas vezes igualzinho**, tem um **espaço invisível**.
2. **Consertar** com o comando certo pra cada problema:

| Problema | Comando | Exemplo no simulado |
| --- | --- | --- |
| espaço sobrando (invisível) | `.str.strip()` | `"mobilidade "` → `"mobilidade"` |
| letra maiúscula | `.str.lower()` | `Cultura` → `cultura` |
| acento, abreviação ou qualquer outra escrita diferente | `.replace({"errado": "certo"})` | `saúde` → `saude` |

3. **Olhar de novo** com `value_counts()`. Tem que sobrar só o número certo de temas.

O que cada parte faz:
- `q2["tema"]` pega só a coluna tema (nome da tabela + nome da coluna entre colchetes e aspas).
- `print(q2["tema"].value_counts())` serve pra **ver a coluna em resumo**: cada valor diferente e quantas vezes aparece. É o melhor jeito de achar escrita errada. Pra ver a coluna inteira, linha por linha, use `print(q2["tema"])`. Funciona com qualquer coluna, é só trocar o nome.
- `.str` avisa que vem um comando de texto (vai antes de `strip` e `lower`).
- `replace` quer dizer "substituir". Na tabelinha `{ }`, à esquerda fica como está escrito e à direita como deve ficar. O que colocar ali você **copia do `value_counts`**.
- `q2["tema"] =` na frente salva o resultado de volta na coluna. Sem isso, nada muda.

**Código pronto:**

```python
print(q2["tema"].value_counts())                            # olhar: quais escritas existem
q2["tema"] = q2["tema"].str.strip().str.lower()             # consertar: espaço e maiúscula
print(q2["tema"].value_counts())                            # olhar de novo: o que sobrou
q2["tema"] = q2["tema"].replace({"saúde": "saude"})         # consertar: o que sobrou (TROQUE conforme o que aparecer)
print(q2["tema"].value_counts())                            # conferir: só os temas certos
```

### Converter tipos (data e número)

**Quando usar:** "converter", "tipos adequados", "datas em formatos distintos", "colunas numéricas usadas no cálculo".

**Como saber se precisa converter:** rode `print(q2.dtypes)`. Se uma coluna que deveria ser data ou número aparecer como **`object`** (= texto), precisa converter. Se já aparecer `int64`, `float64` ou `datetime64`, já está certa, e aí você **não** diz na resposta que converteu.

**Qual comando usar:** olhe o que a coluna **deveria ser**.

| A coluna deveria ser | Exemplo | Comando | Como conferir |
| --- | --- | --- | --- |
| data (com ou sem horário) | `2026-08-01 12:00`, `05/08/2026` | `pd.to_datetime(...)` | `.min()` e `.max()` batem com o período? `.isna().sum()` dá 0? |
| número | `929`, `1548.0` | `pd.to_numeric(..., errors="coerce")` | `.dtypes` mostra `int64` ou `float64`? |

#### Data

O que cada parte faz:
- `pd.to_datetime(...)` converte texto em data. Serve pra data com horário também, ele converte os dois juntos.
- `format="mixed"` quer dizer "cada linha pode estar num formato diferente".
- `dayfirst=True` quer dizer "na dúvida, o **dia** vem primeiro" (jeito brasileiro, `05/08/2026` = 5 de agosto).
- `errors="coerce"` diz que, se não conseguir converter, vira vazio (`NaT`) em vez de travar.
- `q2["data_publicacao"] =` na frente salva de volta na coluna.
- `.min()` / `.max()` mostram a data mais antiga e a mais nova. Têm que bater com as datas que você viu antes de converter. Se aparecer um mês estranho, dia e mês foram trocados: use o bloco de duas passadas da seção 2 (letra c).
- `.isna().sum()` conta as datas que não converteram. Tem que dar 0.

**Código pronto:**

```python
print(q2["data_publicacao"])                                   # olhar: como as datas estão escritas
q2["data_publicacao"] = pd.to_datetime(q2["data_publicacao"], format="mixed", dayfirst=True, errors="coerce")
print(q2["data_publicacao"].min(), q2["data_publicacao"].max())   # conferir: período certo?
print("NaT:", q2["data_publicacao"].isna().sum())              # conferir: tem que dar 0
```

Se a questão pedir **só o dia** ou **só a hora** (depois de converter):

```python
q2["dia_publicacao"] = q2["data_publicacao"].dt.date    # só a data, sem hora
q2["hora"] = q2["data_publicacao"].dt.hour              # só a hora (0 a 23)
```

#### Número

O que cada parte faz:
- As colunas "usadas no cálculo" são as que aparecem na fórmula (no simulado: `alcance`, `compartilhamentos`, `salvamentos`).
- `q2[["a", "b"]]` com **dois colchetes** pega várias colunas de uma vez.
- `.dtypes` mostra o tipo de cada coluna.
- `pd.to_numeric(..., errors="coerce")` converte texto em número. O que não for número vira vazio (`NaN`).
- O `for c in cols:` repete a conversão pra cada coluna da lista.

**Código pronto:**

```python
cols = ["alcance", "compartilhamentos", "salvamentos"]          # TROQUE: colunas da fórmula
print(q2[cols].dtypes)                                          # olhar: object = texto
for c in cols:
    q2[c] = pd.to_numeric(q2[c], errors="coerce")               # converter
print(q2[cols].dtypes)                                          # conferir: int64 ou float64
```

### Criar coluna calculada (taxa)

**Quando usar:** "crie a coluna X, definida por..." e uma fórmula.

**Como pensar:** é traduzir a fórmula do enunciado com os mesmos símbolos. `+` soma, `-` subtrai, `*` multiplica, `/` divide. Os parênteses fazem uma parte ser calculada antes, igual na matemática. O Python faz a conta **linha por linha**, sozinho.

**Por que o nome da tabela antes de cada coluna:** a coluna pertence a uma tabela, e na prova existem várias (`q1`, `q2`, `q3`...), todas com as mesmas colunas. `q2["alcance"]` quer dizer "o alcance **da tabela q2**". É como endereço: a tabela é a rua, a coluna é a casa.

**Molde genérico:**

```python
TABELA["COLUNA_NOVA"] = (TABELA["COLUNA_A"] + TABELA["COLUNA_B"]) / TABELA["COLUNA_C"] * 100
```

**O que trocar, com o exemplo do simulado:**

| No molde | O que é | No simulado (Q2) |
| --- | --- | --- |
| `TABELA` | o nome da sua variável | `q2` |
| `COLUNA_NOVA` | o nome que o enunciado manda criar | `taxa_utilidade_pct` |
| `COLUNA_A`, `COLUNA_B` | as colunas de cima da fórmula | `compartilhamentos`, `salvamentos` |
| `COLUNA_C` | a coluna de baixo da divisão | `alcance` |

Fórmula do enunciado: taxa_utilidade_pct = (compartilhamentos + salvamentos) / alcance × 100

**Código pronto (simulado):**

```python
q2["taxa_utilidade_pct"] = (q2["compartilhamentos"] + q2["salvamentos"]) / q2["alcance"] * 100
print(q2["taxa_utilidade_pct"].head())      # olhar: as primeiras taxas
```

Se a fórmula for outra, só muda a conta. Por exemplo, "curtidas dividido por alcance": `q2["taxa"] = q2["curtidas"] / q2["alcance"]`.

**Cuidado:** antes de criar a taxa, tire as linhas sem as colunas da fórmula e as com zero na coluna de baixo da divisão (letra e, no código da seção 2). Não existe divisão por zero.

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

### Agrupar: uma conta ou várias

**Como saber que é `groupby`:** o enunciado diz **"por"**, "de cada" ou "para cada" (por tema, por dia, por formato). O que vem depois do "por" vai dentro do `groupby`.

| O enunciado pede | Código |
| --- | --- |
| **uma** conta por grupo | `print(q2.groupby("tema")["coluna"].median())` |
| **duas ou mais** contas por grupo | `q2.groupby("tema").agg(nome1=("coluna", "conta"), nome2=("coluna", "conta"))` |
| agrupar por **duas** colunas | `groupby(["tema", "formato"])`, com lista |

Dentro do `agg`, cada linha cria uma coluna no formato `nome_que_voce_escolhe=("coluna_de_origem", "conta")`:

| O enunciado diz | Conta |
| --- | --- |
| quantidade, número de | `"count"` |
| média | `"mean"` |
| mediana | `"median"` |
| total, soma | `"sum"` |

| Ordem pedida | Código |
| --- | --- |
| da maior para a menor | `.sort_values("coluna", ascending=False)` |
| da menor para a maior | `.sort_values("coluna")` |
| cronológica (por data) | `.sort_values("coluna_do_dia")` |

`.reset_index()` no fim do `agg` devolve o grupo (tema, formato) como coluna normal. Use quando precisar usar essa coluna depois, por exemplo pra juntar tema e formato num rótulo. Sem ele, o grupo fica como "índice" e se pega com `tabela.index`.

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
