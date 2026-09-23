# 06 — Regressão (prever um número)

**Como identificar:** o alvo é **numérico contínuo** (taxa esperada, alcance esperado). Se o alvo fosse categoria → `07-classificacao.md`. Se não houvesse alvo → `08-clusterizacao.md`. No template: **seção 9**.

O esqueleto do scikit-learn é sempre o mesmo (Aula 11): `modelo = Modelo()` → `modelo.fit(X_treino, y_treino)` → `modelo.predict(X_teste)`.

## Por que é regressão (resposta de Markdown)

> É um problema de **regressão** porque a variável-alvo (`taxa_engajamento_pct`) é numérica e contínua: o objetivo é estimar um valor, não atribuir uma categoria (classificação) nem descobrir grupos sem rótulo (clusterização).

---

## 1. Características (`X`) e alvo (`y`), sem vazamento

```python
FEATURES = [
    "tema", "formato", "seguidores_autor", "videos_autor",
    "tamanho_legenda", "n_emojis", "n_hashtags", "hora",
    "dia_semana", "duracao_segundos",
]                                          # <-- exatamente as permitidas
ALVO = "taxa_engajamento_pct"              # <--
```

**Vazamento (data leakage).** Se a pergunta é "estimar *antes* de publicar", não entra nada que só existe **depois**: `alcance`, interações, curtidas, compartilhamentos, salvamentos, nem nada derivado do alvo (`taxa_utilidade_pct`). Também fora: o identificador. A Aula 11 compara com "prever a nota da prova olhando o gabarito preenchido". Pergunta de cada feature: *esse dado já existe no momento da previsão?*

### Se a base não trouxer as features prontas (Aula 11)

A Aula 11 **deriva** as features de colunas cruas do export (`body`, `hashtags`, `timestamp`):

```python
import re

X = pd.DataFrame(index=df.index)
X["seguidores_autor"] = df["author_followers"]
X["videos_autor"] = df["author_videos"]
X["tam_legenda"] = df["body"].fillna("").str.len()                       # nº de caracteres
padrao_emoji = re.compile("[\U0001F000-\U0001FAFF☀-➿]")
X["n_emojis"] = df["body"].fillna("").apply(lambda s: len(padrao_emoji.findall(s)))
X["n_hashtags"] = df["hashtags"].fillna("").apply(lambda s: 0 if s == "" else len(s.split(",")))
momento = pd.to_datetime(df["timestamp"])
X["hora"] = momento.dt.hour
X["dia_semana"] = momento.dt.dayofweek                                   # 0 = segunda
```

Coluna que é quase sempre o mesmo valor (a aula cita `is_duet` e `is_ad`) não ajuda o modelo a distinguir nada — pode deixar de fora.

## 2. Categoria vira número

```python
X = pd.get_dummies(df[FEATURES], columns=["tema", "formato"], drop_first=True, dtype=int)
y = df[ALVO]
```

- `drop_first=True`: com 4 temas, 3 colunas bastam.
- `dtype=int`: 0/1 em vez de `True/False`.
- Se houver ausente: `df = df.dropna(subset=FEATURES + [ALVO])` **antes** de montar `X` e `y` (os dois do mesmo DataFrame, senão desalinham).

## 3. Treino e teste

```python
from sklearn.model_selection import train_test_split

X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42)
```

"Reserve 25% para teste" = `test_size=0.25`. Em regressão **não** se usa `stratify`.

## 4. Modelos — sempre com o modelo bobo

O professor sempre compara com o **modelo bobo** (*baseline*): prever a média do **treino** para todo mundo. Se o seu modelo não bate o bobo, ele não aprendeu nada.

```python
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error, r2_score

modelos = {
    "Modelo bobo (média)": DummyRegressor(strategy="mean"),     # = np.full(len(y_teste), y_treino.mean())
    "Regressão linear": LinearRegression(),
    "Árvore de regressão": DecisionTreeRegressor(max_depth=4, random_state=42),   # <-- max_depth do enunciado
}

linhas = []
for nome, m in modelos.items():
    m.fit(X_treino, y_treino)
    previsto = m.predict(X_teste)
    linhas.append({"modelo": nome,
                   "MAE": mean_absolute_error(y_teste, previsto),
                   "R2": r2_score(y_teste, previsto)})

tabela = pd.DataFrame(linhas).sort_values("MAE")      # menor MAE primeiro
print(tabela)
```

Se o enunciado pede só "uma tabela com a linear e a árvore", o bobo pode ficar como linha extra de referência — não atrapalha e mostra critério.

## 5. Real × previsto do modelo escolhido

```python
melhor = modelos[tabela[tabela["modelo"] != "Modelo bobo (média)"].iloc[0]["modelo"]]
y_previsto = melhor.predict(X_teste)
```

Gráfico em `04-graficos.md` → "Dispersão — real × previsto" (com a linha `previsão = valor real`).

## 6. Coeficientes da linear (se pedirem interpretação)

```python
coef = pd.DataFrame({"feature": X.columns, "coeficiente": modelos["Regressão linear"].coef_}).sort_values("coeficiente")
print(coef)
```

Aula 11: como as features têm escalas diferentes (seguidores em milhões, hora de 0 a 23), **só o sinal é comparável** entre elas, não o tamanho. Positivo = quando a feature sobe, a previsão sobe. E é associação, não causa.

## 7. Alvo com cauda longa (Aula 11)

Se o histograma do alvo tem uma cauda longa à direita (ex: `plays`, com meia dúzia de virais gigantes), treine em `log1p` e desfaça na previsão:

```python
modelo = LinearRegression().fit(X_treino, np.log1p(y_treino))
previsto = np.expm1(modelo.predict(X_teste))       # volta para a unidade original
```

---

## O que cada métrica significa (cai na resposta escrita)

**MAE — erro absoluto médio.** Em média, o quanto a previsão erra, **na mesma unidade do alvo**. MAE de 0,9 numa taxa em % = "em média a previsão erra 0,9 ponto percentual". Quanto menor, melhor.

**R².** Quanto da variação do alvo o modelo explica. 1 = perfeito; 0 = igual a chutar a média; **negativo = pior do que chutar a média** (acontece de verdade e é resultado válido para reportar).

**RMSE** (se pedirem): parecido com o MAE, mas pune mais os erros grandes: `mean_squared_error(y_teste, previsto) ** 0.5`.

A Aula 11 chama um R² de 0,28 de "modesto e honesto: prever engajamento a partir de poucas features simples é difícil". Não precisa pedir desculpa por R² baixo — precisa interpretar.

## Resposta escrita — modelo

> É um problema de **regressão**, porque o alvo é numérico e contínuo. O **MAE** mede o erro médio absoluto entre o valor previsto e o observado, na mesma unidade da taxa: um MAE de **[X]** significa que, em média, a estimativa erra [X] pontos percentuais. Escolhi **[MODELO]**, com o menor MAE no teste, abaixo do modelo bobo (MAE [Y]). Uma limitação é que o modelo capta associações estatísticas entre as características disponíveis antes da publicação e o engajamento nesta base; fatores não medidos (conteúdo da peça, distribuição do algoritmo da plataforma) também explicam o resultado, então a previsão não deve ser lida como relação causal.

## Armadilhas

- **R² de 0,95 de primeira** = quase sempre vazamento (Aula 11). Reveja as features.
- **R² negativo** = pior que a média: features sem relação com o alvo, `X` e `y` desalinhados, ou poucos dados.
- Métrica sempre no **teste**. No treino todo modelo parece bom.
- Árvore sem `max_depth` decora o treino e vai mal no teste.
- `could not convert string to float` → faltou `get_dummies`. `Input contains NaN` → faltou `dropna`.
- `DecisionTreeRegressor` para número, `DecisionTreeClassifier` para categoria — não troque.
