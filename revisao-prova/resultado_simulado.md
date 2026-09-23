[simulado (1).md](https://github.com/user-attachments/files/32544901/simulado.1.md)

# Gabarito do simulado: Festival ViraBairro

Cada questão tem: **tema**, **arquivo**, cada item explicado **separado** e depois **tudo junto** pra copiar, e a **resposta escrita**. Os números são os da plataforma; na prova use os da **sua** tela.

| Questão | Tema | Vá para |
| --- | --- | --- |
| 1 | Olhar a base (linhas, colunas, ausentes) | [Q1](#questão-1-diagnóstico-da-base) |
| 2 | Limpeza (duplicata, texto, data, ausentes, taxa, tabela) | [Q2](#questão-2-limpeza-da-base) |
| 3 | Tabela por grupo + gráfico de barras | [Q3](#questão-3-tabela-por-tema-e-barras) |
| 4 | Data, tabela por dia, gráfico de linha, filtro, top 5 | [Q4](#questão-4-acompanhamento-diário) |
| 5 | Tabela por duas colunas + barras horizontais | [Q5](#questão-5-tema-e-formato-juntos) |
| 6 | Árvore de classificação + importâncias | [Q6](#questão-6-importâncias-da-árvore) |
| 7 | Regressão (MAE, R², real x previsto) | [Q7](#questão-7-regressão) |
| 8 | Classificação (3 modelos, matriz, corte) | [Q8](#questão-8-classificação-e-corte) |
| — | Regras que valem pra todas | [Regras](#regras-que-valem-pra-todas) |

## Regras que valem pra todas

- **Cada questão abre o arquivo numa variável nova** (`q1`, `q2`...), porque cada uma tem que funcionar sozinha.
- **Só aparece na tela o que está em `print(...)`**, ou o que está sozinho na **última linha** da célula (aí sai como tabela bonita).
- **Ritmo de todo passo:** olhar → consertar → olhar de novo.
- **Imports** (uma vez, no topo da célula):

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

- **Avisos amarelos** `FigureCanvasAgg is non-interactive` e `ConvergenceWarning` **não são erro**.
- **Na resposta:** use os números da tela, conte as frases pedidas, diga "associação, não causa" e cite a amostra pequena.

## Questão 1: diagnóstico da base

**Tema:** olhar a base antes de mexer. **Arquivo:** `publicacoes_brutas.csv`.

**a) Abrir e ver as 5 primeiras linhas.** `read_csv` abre o arquivo; `head()` mostra as 5 primeiras.

```python
q1 = pd.read_csv("dados/publicacoes_brutas.csv")
q1.head()
```

**b) Linhas e colunas.** `shape` devolve (linhas, colunas). Não leva parênteses.

```python
print(q1.shape)          # (36, 12)
```

**c) Ausentes só das colunas que têm.** `isna().sum()` conta os vazios de cada coluna; o filtro `[ausentes > 0]` tira as que deram zero (**a pegadinha**).

```python
ausentes = q1.isna().sum()
print(ausentes[ausentes > 0])     # alcance 1, comentarios 1, salvamentos 1
```

**Tudo junto** (o `head` vai por último pra sair como tabela):

```python
q1 = pd.read_csv("dados/publicacoes_brutas.csv")
print(q1.shape)
ausentes = q1.isna().sum()
print(ausentes[ausentes > 0])
q1.head()
```

**Resposta (até 2 frases):**

> A base traz apenas 36 registros de uma única organização, referentes a uma campanha específica, e não tem nenhuma coluna que identifique a rede social, o público ou o bairro de cada publicação. Com esse tamanho e sem essas informações, os resultados descrevem só este conjunto de publicações e não podem ser lidos como retrato de todas as redes, públicos ou bairros.

## Questão 2: limpeza da base

**Tema:** limpar a base bruta e fazer uma tabela por tema. **Arquivo:** `publicacoes_brutas.csv`.

**a) Abrir numa variável nova.**

```python
q2 = pd.read_csv("dados/publicacoes_brutas.csv")
```

**b) Duplicidade por `id_publicacao`.** A mesma publicação duas vezes conta em dobro. "Por id" = `subset="id_publicacao"`. Sem "por id" no enunciado → `q2.drop_duplicates()`. `keep="first"` guarda a primeira (é o padrão).

```python
print("duplicadas:", q2.duplicated(subset="id_publicacao").sum())
q2 = q2.drop_duplicates(subset="id_publicacao", keep="first")
print("linhas depois:", len(q2))        # 36 -> 35
```

**c) Padronizar o tema.** Olhe com `value_counts()`: devia ter 4 temas e apareceram 7. `strip` tira o espaço invisível (`"mobilidade "`), `lower` tira a maiúscula (`Cultura`) e `replace` troca o que sobrou (`saúde` → `saude`; copie do `value_counts`).

```python
q2["tema"] = q2["tema"].str.strip().str.lower()
q2["tema"] = q2["tema"].replace({"saúde": "saude"})
print(q2["tema"].value_counts())        # só 4 temas
```

**d) Converter a data.** Veio como texto (`dtype: object`) e em 3 formatos. `dayfirst=True` = "o dia vem primeiro" (05/08 = 5 de agosto). **Confira** com `min`/`max` (tem que dar 01/08 a 28/08/2026) e `NaT` (tem que dar 0). Se aparecer mês estranho, use o bloco de duas passadas do codigos.md.

```python
q2["data_publicacao"] = pd.to_datetime(q2["data_publicacao"], format="mixed", dayfirst=True, errors="coerce")
print(q2["data_publicacao"].min(), q2["data_publicacao"].max())
print("NaT:", q2["data_publicacao"].isna().sum())
```

**e) Colunas numéricas.** As "do cálculo" são as da fórmula. Olhe o tipo: já eram número (`float64`/`int64`), então **não precisou converter**. Se fosse `object`: `pd.to_numeric(q2[c], errors="coerce")`.

```python
print(q2[["alcance", "compartilhamentos", "salvamentos"]].dtypes)
```

**f) Ausentes e inválidos.** Sem `alcance` ou `salvamentos` não dá pra calcular a taxa → descarta (inventar seria criar dado). Sem `comentarios` **fica**, porque não entra na fórmula. Depois olhe o menor `alcance`: é o número **de baixo da divisão** e não pode ser zero. Deu 765, então não precisou filtrar. *Se desse 0:* `q2 = q2[q2["alcance"] > 0]`.

```python
q2 = q2.dropna(subset=["alcance", "compartilhamentos", "salvamentos"])
print("linhas agora:", len(q2))         # 35 -> 33
print(q2["alcance"].min())              # 765
```

**g) Criar a taxa.** É a fórmula com os mesmos símbolos (`+ / *`). O nome da tabela vai antes de cada coluna.

```python
q2["taxa_utilidade_pct"] = (q2["compartilhamentos"] + q2["salvamentos"]) / q2["alcance"] * 100
```

**h) Tabela por tema.** "Por tema" = `groupby("tema")`. Duas contas = `agg` (`count` = quantidade, `median` = mediana). "Da maior para a menor" = `ascending=False`.

```python
tabela = q2.groupby("tema").agg(
    publicacoes=("id_publicacao", "count"),
    mediana_utilidade_pct=("taxa_utilidade_pct", "median"),
)
tabela = tabela.sort_values("mediana_utilidade_pct", ascending=False)
print(tabela)      # saude 11 / 1,18 | cultura 7 / 1,14 | mobilidade 8 / 1,13 | trabalho 7 / 0,86
```

**Tudo junto:**

```python
q2 = pd.read_csv("dados/publicacoes_brutas.csv")

print("duplicadas:", q2.duplicated(subset="id_publicacao").sum())
q2 = q2.drop_duplicates(subset="id_publicacao", keep="first")
print("linhas depois:", len(q2))

q2["tema"] = q2["tema"].str.strip().str.lower()
q2["tema"] = q2["tema"].replace({"saúde": "saude"})
print(q2["tema"].value_counts())

q2["data_publicacao"] = pd.to_datetime(q2["data_publicacao"], format="mixed", dayfirst=True, errors="coerce")
print(q2["data_publicacao"].min(), q2["data_publicacao"].max())
print("NaT:", q2["data_publicacao"].isna().sum())

print(q2[["alcance", "compartilhamentos", "salvamentos"]].dtypes)

q2 = q2.dropna(subset=["alcance", "compartilhamentos", "salvamentos"])
print("linhas agora:", len(q2))
print(q2["alcance"].min())

q2["taxa_utilidade_pct"] = (q2["compartilhamentos"] + q2["salvamentos"]) / q2["alcance"] * 100

tabela = q2.groupby("tema").agg(
    publicacoes=("id_publicacao", "count"),
    mediana_utilidade_pct=("taxa_utilidade_pct", "median"),
)
tabela = tabela.sort_values("mediana_utilidade_pct", ascending=False)
print(tabela)
```

**Resposta (até 4 frases, sempre "fiz X porque Y"):**

> Removi 1 duplicidade por `id_publicacao`, mantendo a primeira ocorrência, porque a mesma publicação contada duas vezes distorceria a tabela, e usei `subset` porque o enunciado pediu duplicidade pelo id. Padronizei `tema` com `strip` e `lower`, que resolveram espaço sobrando e letra maiúscula, e unifiquei `saúde` com `saude` por uma tabela de equivalência, porque o acento fazia o mesmo tema contar como dois; conferi com `value_counts` que ficaram só os 4 temas. Converti `data_publicacao` de texto para data com `dayfirst=True`, porque a coluna misturava formatos com o ano e com o dia na frente, e conferi que todas as datas ficaram entre 01/08/2026 e 28/08/2026, sem nenhuma perdida; as colunas da fórmula já chegaram como número, então não precisaram de conversão. Descartei as 2 publicações sem `alcance` ou sem `salvamentos`, porque sem esses valores a taxa não pode ser calculada e preencher seria inventar dado, e mantive a que só não tinha `comentarios`, porque essa coluna não entra na fórmula.

## Questão 3: tabela por tema e barras

**Tema:** agrupar por uma coluna + gráfico de barras. **Arquivo:** `publicacoes_analise.csv` (já limpa). É o final da Q2 na base limpa, com um gráfico.

**a) Abrir e criar a taxa** (mesma fórmula da Q2; a base limpa não precisa de limpeza).

```python
q3 = pd.read_csv("dados/publicacoes_analise.csv")
q3["taxa_utilidade_pct"] = (q3["compartilhamentos"] + q3["salvamentos"]) / q3["alcance"] * 100
```

**b) Tabela da mediana por tema** (igual à Q2).

```python
tabela_q3 = q3.groupby("tema").agg(
    publicacoes=("id_publicacao", "count"),
    mediana_utilidade_pct=("taxa_utilidade_pct", "median"),
)
tabela_q3 = tabela_q3.sort_values("mediana_utilidade_pct", ascending=False)
print(tabela_q3)
```

**c) Gráfico de barras.** Esqueleto de todo gráfico: criar (`subplots`) → desenhar (`bar`) → textos (título, eixos, fonte) → mostrar. `tabela_q3.index` são os temas (depois do `groupby`, o tema vira o índice).

```python
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tabela_q3.index, tabela_q3["mediana_utilidade_pct"])
ax.set_title("Qual tema as pessoas mais salvam e compartilham?")
ax.set_xlabel("Tema da publicação")
ax.set_ylabel("Mediana da taxa de utilidade (%)")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

**Tudo junto:** a, b e c em sequência, na mesma célula.

**Resultado:** mobilidade 1,15 (33) | cultura 1,13 (26) | saude 1,10 (35) | trabalho 0,96 (26). As três primeiras estão **empatadas**.

**Resposta (3 a 5 frases):**

> Entre os quatro temas, mobilidade tem a maior mediana de taxa de utilidade, com 1,15%, seguida de perto por cultura, com 1,13%, e saúde, com 1,10%, enquanto trabalho fica abaixo, com 0,96%. A mediana é o valor do meio, com metade das publicações do tema acima e metade abaixo, e por isso é menos afetada do que a média por uma peça fora do padrão. Os três primeiros temas estão praticamente empatados, com diferenças de até 0,05 ponto sobre 26 a 35 publicações por tema, o que é pouco para sustentar uma escolha. Por isso, a decisão defensável é descartar trabalho e escolher entre os outros três por critério editorial. Como limitação, os temas não foram publicados nos mesmos formatos e horários, então isto é associação observada, não prova de que o tema cause mais compartilhamento.

## Questão 4: acompanhamento diário

**Tema:** data, tabela por dia, gráfico de linha, filtro com duas condições, top 5. **Arquivo:** `publicacoes_analise.csv`.

**a) Converter a data e criar `dia_publicacao`.** Aqui as datas vêm num formato só, então basta o `to_datetime` simples. `.dt.date` pega só o dia (sem a hora), pra agrupar por dia.

```python
q4 = pd.read_csv("dados/publicacoes_analise.csv")
q4["data_publicacao"] = pd.to_datetime(q4["data_publicacao"])
q4["dia_publicacao"] = q4["data_publicacao"].dt.date
```

**b) Tabela por dia.** Três contas: `count` (quantidade), `mean` (média), `sum` (total). "Cronológica" = ordenar pelo dia, do mais antigo pro mais novo (o padrão, sem `ascending=False`).

```python
diaria = q4.groupby("dia_publicacao").agg(
    publicacoes=("id_publicacao", "count"),
    media_engajamento_pct=("taxa_engajamento_pct", "mean"),
    alcance_total=("alcance", "sum"),
)
diaria = diaria.sort_values("dia_publicacao")
print(diaria)
print("dias:", len(diaria))     # 56
```

**c) Gráfico de linhas.** Linha porque o eixo de baixo é tempo. `diaria.index` são os dias. `rotation=45` inclina as datas.

```python
fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(diaria.index, diaria["media_engajamento_pct"], marker="o")
ax.set_title("Como a taxa média de engajamento variou dia a dia")
ax.set_xlabel("Dia da publicação")
ax.set_ylabel("Taxa média de engajamento (%)")
ax.tick_params(axis="x", rotation=45)
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

**d) Recorte + top 5.** `==` pergunta "é igual?"; `>=` porque "a partir das 18h" inclui as 18h; `&` = "e"; cada condição entre parênteses. `nlargest(5, coluna)` pega os 5 maiores.

```python
recorte = q4[(q4["formato"] == "reel") & (q4["hora"] >= 18)]
print("reels a partir das 18h:", len(recorte))       # 21
top5 = recorte.nlargest(5, "taxa_engajamento_pct")
print(top5[["id_publicacao", "dia_publicacao", "hora", "tema", "taxa_engajamento_pct"]])
```

**Tudo junto:** a, b, c e d em sequência, na mesma célula. 1º lugar: OCB-003 (cultura, 22h, 6,82%).

**Resposta:**

> A taxa média de engajamento oscila de um dia para o outro ao longo da campanha, alternando picos e quedas sem uma direção estável de subida ou descida. Boa parte dessa oscilação vem do tamanho da amostra: são 120 publicações em 56 dias, cerca de duas por dia, e com tão poucas uma única peça acima ou abaixo do padrão desloca a média do dia inteiro, por isso o gráfico não permite afirmar tendência, só descrever a variação. O recorte dos cinco reels noturnos com maior taxa também não prova que horário ou formato causem engajamento, porque ele seleciona as melhores de um grupo de apenas 21 publicações já filtrado por formato e horário. Para sustentar essa conclusão, seria preciso comparar os reels noturnos com reels de outros horários e com outros formatos publicados à noite, e essa comparação não foi feita.

## Questão 5: tema e formato juntos

**Tema:** agrupar por **duas** colunas + gráfico de barras horizontal. **Arquivo:** `publicacoes_analise.csv`. É a Q3 com duas colunas.

**a) Abrir.** A `taxa_engajamento_pct` já vem pronta na base, então não precisa criar.

```python
q5 = pd.read_csv("dados/publicacoes_analise.csv")
```

**b) Tabela por tema e formato.** Pra agrupar por duas colunas, passe uma **lista** no `groupby`. Cada linha da tabela vira uma combinação (cultura + reel, cultura + imagem...). São 4 temas × 3 formatos = 12 linhas. O `reset_index()` devolve tema e formato como colunas normais, pra dar pra juntar os dois no passo c.

```python
tabela_q5 = q5.groupby(["tema", "formato"]).agg(
    publicacoes=("id_publicacao", "count"),
    mediana_engajamento_pct=("taxa_engajamento_pct", "median"),
).reset_index()
tabela_q5 = tabela_q5.sort_values("mediana_engajamento_pct", ascending=False)
print(tabela_q5)
```

**c) Um nome pra cada combinação.** O gráfico precisa de um rótulo só por barra, então juntamos os dois textos com `+`.

```python
tabela_q5["combinacao"] = tabela_q5["tema"] + " / " + tabela_q5["formato"]
```

**d) Gráfico de barras horizontal.** Horizontal (`barh`) porque são 12 barras com nome comprido. No `barh` o **valor fica no eixo X** e os nomes no eixo Y. `[::-1]` põe a maior barra em cima.

```python
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(tabela_q5["combinacao"][::-1], tabela_q5["mediana_engajamento_pct"][::-1])
ax.set_title("Quais combinações de tema e formato engajam mais?")
ax.set_xlabel("Mediana da taxa de engajamento (%)")
ax.set_ylabel("Tema / formato")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

**Tudo junto:**

```python
q5 = pd.read_csv("dados/publicacoes_analise.csv")

tabela_q5 = q5.groupby(["tema", "formato"]).agg(
    publicacoes=("id_publicacao", "count"),
    mediana_engajamento_pct=("taxa_engajamento_pct", "median"),
).reset_index()
tabela_q5 = tabela_q5.sort_values("mediana_engajamento_pct", ascending=False)
print(tabela_q5)

tabela_q5["combinacao"] = tabela_q5["tema"] + " / " + tabela_q5["formato"]

fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(tabela_q5["combinacao"][::-1], tabela_q5["mediana_engajamento_pct"][::-1])
ax.set_title("Quais combinações de tema e formato engajam mais?")
ax.set_xlabel("Mediana da taxa de engajamento (%)")
ax.set_ylabel("Tema / formato")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

**Resultado:** o topo é mobilidade / reel (5,10; 11 publicações), depois cultura / reel (4,82) e saude / reel (4,67). O último é trabalho / imagem (3,04). **Achado:** em todos os 4 temas a ordem é reel > carrossel > imagem.

**Resposta (4 a 6 frases):**

> A combinação de mobilidade em reel aparece no topo, com mediana de 5,10%, e é a candidata natural a ser testada, mas está a apenas 0,28 ponto de cultura em reel e a 0,43 de saúde em reel, com 8 a 12 publicações por combinação. O cruzamento mostra um padrão que uma variável sozinha esconderia: dentro de cada um dos quatro temas, a ordem é sempre reel, depois carrossel, depois imagem, o que indica que o formato ordena o resultado de forma mais consistente que o tema. Comparar duas variáveis juntas é diferente de analisar uma só porque, olhando só o tema, a vantagem de mobilidade poderia vir apenas de ela ter mais reels. Como limitação, nenhuma combinação passa de 12 publicações, e uma mediana com tão poucos casos pode mudar de posição por causa de uma única peça. A recomendação mais segura é priorizar o formato reel e tratar a escolha do tema como decisão editorial, lembrando que isto é associação observada, não causa.

## Questão 6: importâncias da árvore

**Tema:** treinar uma árvore de classificação e ver o que ela mais usou. **Arquivo:** `publicacoes_analise.csv`. É o começo da Q8 + importâncias.

**a) Criar o alvo.** 1 se a taxa está acima do percentil 75, 0 no resto.

```python
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

q6 = pd.read_csv("dados/publicacoes_analise.csv")
corte_p75 = q6["taxa_engajamento_pct"].quantile(0.75)
q6["mereceu_divulgacao_adicional"] = (q6["taxa_engajamento_pct"] > corte_p75).astype(int)
```

**b) X e y.** Só as características de antes de publicar (nada de alcance, interações ou taxa: seria vazamento). `get_dummies` transforma tema e formato (texto) em colunas 0/1.

```python
CARACTERISTICAS = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
                   "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]
X = pd.get_dummies(q6[CARACTERISTICAS], columns=["tema", "formato"])
y = q6["mereceu_divulgacao_adicional"]
```

**c) Treino e teste + árvore.** `test_size=0.25` = 25% pra teste; `stratify=y` = "preservando a proporção do alvo"; `max_depth=4` = "profundidade máxima 4"; `class_weight="balanced"` = "pesos balanceados". `.fit` treina.

```python
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
arvore = DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced")
arvore.fit(X_treino, y_treino)
```

**d) Top 5 importâncias + barras horizontais.**

```python
importancias = pd.DataFrame({"caracteristica": X.columns, "importancia": arvore.feature_importances_})
top5 = importancias.sort_values("importancia", ascending=False).head(5)
print(top5)

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(top5["caracteristica"][::-1], top5["importancia"][::-1])
ax.set_title("O que a árvore mais usou para separar as publicações de destaque")
ax.set_xlabel("Importância na árvore (0 a 1)")
ax.set_ylabel("Característica")
fig.tight_layout()
plt.show()
```

**Tudo junto:** a, b, c e d em sequência. Resultado: formato_reel 0,28 | dia_semana 0,14 | n_hashtags 0,14 | tema_cultura 0,10 | videos_autor 0,09.

**Resposta:**

> A árvore usou principalmente `formato_reel`, com importância 0,28, seguido de `dia_semana` e `n_hashtags`, empatados em 0,14, depois `tema_cultura` com 0,10 e `videos_autor` com 0,09. Importância alta significa apenas que a característica foi útil para a árvore separar as publicações que ela viu no treino, não que ela cause o desempenho: os reels desta campanha podem concentrar certos temas, horários e durações, e a árvore aproveita essa associação sem separar o que vem de quê. O ranking também é instável porque a árvore foi treinada com apenas 90 publicações. Trocar o `random_state`, acrescentar algumas publicações ou distribuir formatos e horários de forma mais equilibrada poderia fazer `dia_semana` e `n_hashtags`, que hoje empatam, trocarem de posição.

## Questão 7: regressão

**Tema:** estimar um número (taxa) com regressão linear e árvore. **Arquivo:** `publicacoes_analise.csv`.

**a) X e y.** O alvo é a taxa, um **número** → regressão. **Sem** `stratify` (ele só existe em classificação).

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score

q7 = pd.read_csv("dados/publicacoes_analise.csv")
CARACTERISTICAS = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
                   "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]
X = pd.get_dummies(q7[CARACTERISTICAS], columns=["tema", "formato"])
y = q7["taxa_engajamento_pct"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42)
```

**b) Dois modelos + tabela de MAE e R².** MAE = erro médio na unidade da taxa (menor é melhor). R² = quanto o modelo explica (1 perfeito, 0 = chutar a média). O "bobo" chuta sempre a média: é a referência.

```python
prev_lin = LinearRegression().fit(X_treino, y_treino).predict(X_teste)
prev_arv = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_treino, y_treino).predict(X_teste)
prev_bobo = np.full(len(y_teste), y_treino.mean())
print(pd.DataFrame({"modelo": ["bobo", "linear", "árvore"],
                    "MAE": [mean_absolute_error(y_teste, p) for p in (prev_bobo, prev_lin, prev_arv)],
                    "R2": [r2_score(y_teste, p) for p in (prev_bobo, prev_lin, prev_arv)]}).round(3))
```

**c) Gráfico real x previsto do modelo de menor MAE** (aqui, a linear). A linha tracejada é onde previsto = real.

```python
previsao = prev_lin
fig, ax = plt.subplots(figsize=(6.5, 6))
ax.scatter(y_teste, previsao, alpha=0.5)
minimo = float(min(y_teste.min(), previsao.min()))
maximo = float(max(y_teste.max(), previsao.max()))
ax.plot([minimo, maximo], [minimo, maximo], linestyle="--", color="red", label="previsão = valor real")
ax.set_title("Valor real x valor previsto (regressão linear)")
ax.set_xlabel("Taxa de engajamento real (%)")
ax.set_ylabel("Taxa de engajamento prevista (%)")
ax.legend()
plt.show()
```

**Tudo junto:** a, b e c em sequência. Resultado: bobo MAE 0,603 | **linear MAE 0,349, R² 0,644** | árvore MAE 0,516, R² 0,129.

**Resposta:**

> O aprendizado adequado é a regressão, porque a variável-alvo, `taxa_engajamento_pct`, é um número contínuo e a equipe quer estimar o seu valor, não classificá-lo numa categoria. O MAE mede o erro absoluto médio na unidade do alvo: o MAE de 0,349 da regressão linear significa que, em média, a previsão erra a taxa em cerca de 0,35 ponto percentual para cima ou para baixo. Escolhi a regressão linear, que teve o menor MAE, 0,349 contra 0,516 da árvore, e o maior R², 0,644 contra 0,129, reduzindo o erro em cerca de 42% em relação ao modelo que sempre chuta a média. Como limitação, o modelo descreve associações observadas nesta campanha e não relações causais, então mudar uma característica numa nova peça não garante o efeito estimado.

## Questão 8: classificação e corte

**Tema:** decidir sim/não com 3 classificadores, matriz de confusão e corte. **Arquivo:** `publicacoes_analise.csv`.

**a) Alvo, X, y, treino e teste.** Igual aos passos a, b e c da Q6.

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

q8 = pd.read_csv("dados/publicacoes_analise.csv")
corte_p75 = q8["taxa_engajamento_pct"].quantile(0.75)
q8["mereceu_divulgacao_adicional"] = (q8["taxa_engajamento_pct"] > corte_p75).astype(int)
CARACTERISTICAS = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
                   "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]
X = pd.get_dummies(q8[CARACTERISTICAS], columns=["tema", "formato"])
y = q8["mereceu_divulgacao_adicional"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
```

**b) Três modelos + tabela.** O laço `for` treina e testa cada um. Precisão = das indicadas, quantas eram boas; recall = das boas, quantas achou; F1 = equilíbrio.

```python
logistica = LogisticRegression(max_iter=5000)
modelos = {"regressão logística": logistica,
           "árvore de classificação": DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced"),
           "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")}
linhas = []
for nome, modelo in modelos.items():
    modelo.fit(X_treino, y_treino)
    decisao = modelo.predict(X_teste)
    linhas.append({"modelo": nome,
                   "precisão": precision_score(y_teste, decisao, zero_division=0),
                   "recall": recall_score(y_teste, decisao, zero_division=0),
                   "F1": f1_score(y_teste, decisao, zero_division=0)})
comparacao = pd.DataFrame(linhas).sort_values("F1", ascending=False).round(3)
print(comparacao)
```

**c) Matriz de confusão do maior F1.** VN e VP são acertos; FP = alarme falso; FN = deixou passar.

```python
nome_melhor = comparacao.iloc[0]["modelo"]
cm = confusion_matrix(y_teste, modelos[nome_melhor].predict(X_teste))
print("maior F1:", nome_melhor)
print(f"VN={cm[0, 0]}  FP={cm[0, 1]}")
print(f"FN={cm[1, 0]}  VP={cm[1, 1]}")
```

**d) Cortes 0,50 e 0,30.** `predict_proba(...)[:, 1]` dá a probabilidade de ser 1; com ela você escolhe o corte.

```python
probabilidade = logistica.predict_proba(X_teste)[:, 1]
linhas_corte = []
for corte in [0.50, 0.30]:
    d = (probabilidade >= corte).astype(int)
    linhas_corte.append({"corte": corte,
                         "precisão": precision_score(y_teste, d, zero_division=0),
                         "recall": recall_score(y_teste, d, zero_division=0),
                         "F1": f1_score(y_teste, d, zero_division=0)})
print(pd.DataFrame(linhas_corte).round(3))
```

**Tudo junto:** a, b, c e d em sequência. Resultado: logística F1 0,800 (maior), Random Forest 0,600, árvore 0,533; matriz VN=21, FP=2, FN=1, VP=6; corte 0,50 → F1 0,800; corte 0,30 → recall 1,0 e F1 0,824.

**Resposta 8.1 (tipo de modelo):**

> O aprendizado adequado é a classificação, porque a variável-alvo é binária, indicando se a publicação merece ou não divulgação adicional, e a decisão da equipe também é binária. A regressão não responde diretamente porque estima um valor contínuo, que ainda precisaria de um corte para virar ação, e a clusterização não responde porque agrupa registros por semelhança sem usar a resposta conhecida, que aqui foi definida pelo percentil 75.

**Resposta 8 (decisão, até 6 frases):**

> Escolhi a regressão logística, que teve o maior F1 entre os três modelos, com 0,800, e o corte de 0,30 em vez do padrão de 0,50. Um falso positivo significa gastar um dos poucos espaços de divulgação numa publicação que não iria render, e um falso negativo significa deixar sem apoio uma peça que teria bom desempenho. No corte de 0,50, o modelo encontrou 6 das 7 publicações que mereciam apoio, com 2 alarmes falsos e 1 deixada passar. Com o corte de 0,30, ele encontra todas as 7, com recall de 1,00, ao custo de só um alarme falso a mais: a precisão cai de 0,75 para 0,70 e o F1 sobe de 0,800 para 0,824. Como o ganho de recall custou quase nada em precisão, o corte mais baixo é melhor pelos dois critérios. A ressalva é que o teste tem apenas 7 positivos, então essa vantagem equivale a uma única publicação e não é regra estável.
