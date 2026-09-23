# 11 — Erros comuns (troubleshooting)

Ctrl+F a mensagem de erro aqui.

## Erros que NÃO dão erro (os piores)

Rodou, não reclamou, e o resultado está errado. Confira sempre:

| Sintoma | Causa provável | Correção |
|---|---|---|
| Aparecem 7+ temas quando deveriam ser 4 | faltou padronizar texto | `.str.strip().str.lower().str.title()` |
| Datas fora do período da campanha | pandas 3: `format="mixed", dayfirst=True` (Aula 10) inverteu dia e mês das ISO com dia ≤ 12 | `converter_data` (`02-limpeza.md`, seção 4 do template) |
| Muitas linhas sumiram após converter data | `to_datetime(errors="coerce")` sem formato virou `NaT` em um dos formatos | `converter_data` |
| TODAS as datas viraram `NaT` | pandas 1.x não conhece `format="mixed"` / `"ISO8601"` e, com `errors="coerce"`, zera tudo calado | `converter_data` (já trata a versão) |
| Taxa acima de 100% ou negativa | denominador errado ou não tratado | confira a fórmula e `alcance > 0` |
| `inf` na coluna calculada | divisão por zero | `df = df[df["alcance"] > 0]` |
| Recorte vazio (0 linhas) | valor escrito diferente do filtro | `df["formato"].unique()` |
| Gráfico desenhado em cima do anterior | reaproveitou a mesma figura | um `fig, ax = plt.subplots()` novo por gráfico |
| Clusters separados praticamente por uma coluna só | faltou padronizar | `StandardScaler()` antes do KMeans |
| Um cluster com 3 ou 4 registros | outliers numa coluna de cauda longa (seguidores, alcance) | `np.log1p` nessa coluna antes de padronizar |
| Acurácia alta, mas o modelo quase nunca acerta a classe 1 | classe rara: chutar "não" já acerta ~75% | olhe recall e matriz de confusão; `class_weight` ou corte menor |
| R² de 0,95 ou F1 = 1 de primeira | vazamento (Aula 11) | tire da lista o que só existe depois da publicação |

**Hábito que salva:** depois de cada transformação, rode `df.shape`,
`.unique()` ou `.describe()` e olhe se faz sentido. Custa 5 segundos.

---

## Mensagens de erro

### `KeyError: 'nome_da_coluna'`
A coluna não existe com esse nome. Rode `print(df.columns.tolist())` e copie o
nome exato — costuma ser acento, maiúscula ou espaço sobrando.
Para tirar espaços de todos os nomes: `df.columns = df.columns.str.strip()`.

### `ValueError: could not convert string to float: 'Cultura'`
Você mandou texto para um modelo do scikit-learn. Faltou:
```python
X = pd.get_dummies(X, columns=["tema", "formato"], drop_first=True, dtype=int)
```

### `ValueError: Input contains NaN`
O modelo não aceita ausentes. Antes de treinar:
```python
df = df.dropna(subset=FEATURES + [ALVO])
```

### `ValueError: Found input variables with inconsistent numbers of samples`
`X` e `y` têm tamanhos diferentes — normalmente porque você filtrou um e não o
outro. Construa os dois a partir do **mesmo** DataFrame já filtrado.

### `ConvergenceWarning: lbfgs failed to converge`
Regressão logística sem escalonamento. Corrija:
```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
modelo = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
```

### `TypeError: __init__() got an unexpected keyword argument 'class_weight'`
`AdaBoostClassifier` e `GaussianNB` não aceitam `class_weight`. Remova.

### `AttributeError: 'LogisticRegression' object has no attribute 'feature_importances_'`
Só modelos de árvore têm isso. Para a logística, use os coeficientes:
```python
pd.Series(modelo.coef_[0], index=X_treino.columns).abs().sort_values(ascending=False)
```
Se estiver dentro de um pipeline:
```python
modelo.named_steps["logisticregression"].coef_[0]
```

### `UndefinedMetricWarning: Precision is ill-defined`
O modelo não previu nenhum positivo. Adicione `zero_division=0` nas métricas —
e considere `class_weight="balanced"` ou um corte mais baixo.

### `SettingWithCopyWarning`
Você filtrou e depois escreveu no resultado. Adicione `.copy()` no filtro:
```python
df = df[df["alcance"] > 0].copy()
```

### `ValueError: The truth value of a Series is ambiguous`
Você usou `and`/`or` em vez de `&`/`|`, ou esqueceu parênteses:
```python
df[(df["formato"] == "reel") & (df["hora"] >= 18)]   # correto
```

### `FileNotFoundError: dados/arquivo.csv`
O caminho é relativo à pasta do notebook. Verifique:
```python
import os
print(os.getcwd())
print(os.listdir("dados"))
```

### `NameError: name 'pd' is not defined`
Faltou rodar a célula de imports (ou o kernel reiniciou). Rode-a de novo.

### `ModuleNotFoundError: No module named 'sklearn'`
```bash
uv add scikit-learn        # se o projeto usa uv
pip install scikit-learn   # senão
```
No notebook: `!pip install scikit-learn` e reinicie o kernel.

### `UnicodeDecodeError` ao ler CSV
```python
pd.read_csv(arq, encoding="latin-1")
```

### Colunas todas grudadas em uma só
Separador diferente:
```python
pd.read_csv(arq, sep=";", decimal=",")
```

---

## Ver melhor o que está acontecendo

```python
pd.set_option("display.max_columns", None)     # não corta colunas
pd.set_option("display.width", 200)
df.info()                                       # tipos + ausentes + memória
df.sample(5)                                    # linhas aleatórias
```

## Se travar de vez

- Reinicie o kernel e rode tudo de novo de cima (variável antiga contaminada é
  causa frequente de resultado inexplicável).
- Isole: rode a expressão em partes e imprima cada pedaço.
- Se um modelo não funcionar, **troque por outro da lista permitida** e siga —
  não perca 15 minutos num só. A questão pede três modelos quaisquer da lista.
- Entregue com o que tem: código parcial + resposta escrita honesta vale mais
  que célula vazia.
