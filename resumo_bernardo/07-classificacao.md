# 07 — Classificação (prever uma categoria)

**Como identificar:** o alvo tem **categorias** (merece / não merece; alto /
baixo; sim / não). Número contínuo → `06-regressao.md`. Sem rótulo nenhum →
`08-clusterizacao.md`. No template: **seção 10**.

Da Aula 12: **o rótulo é uma decisão sua** (um corte), e com classe rara
**a acurácia engana**.

## Passo a passo completo

### 1. Criar o alvo por percentil

```python
limite = df["taxa_engajamento_pct"].quantile(0.75)          # <-- percentil
df["mereceu_divulgacao_adicional"] = (df["taxa_engajamento_pct"] > limite).astype(int)

print("limite p75:", round(limite, 2))
print(df["mereceu_divulgacao_adicional"].value_counts())    # confira o balanceamento
```

Com o percentil 75, ~25% das linhas ficam na classe 1 → base **desbalanceada**.
É por isso que o enunciado pede `stratify` e que vale usar
`class_weight="balanced"` nas árvores. "Acima do percentil 75" é `>`, não `>=`.

### 2. Características sem vazamento

```python
FEATURES = [
    "tema", "formato", "seguidores_autor", "videos_autor",
    "tamanho_legenda", "n_emojis", "n_hashtags", "hora",
    "dia_semana", "duracao_segundos",
]                                          # <-- exatamente as permitidas

X = pd.get_dummies(df[FEATURES], columns=["tema", "formato"],
                   drop_first=True, dtype=int)
y = df["mereceu_divulgacao_adicional"]
```

**Nunca** inclua `taxa_engajamento_pct` — o alvo foi criado a partir dela,
então o modelo acertaria 100% sem aprender nada. Isso é vazamento clássico.
Também fora: `alcance`, `interacoes`, `id_publicacao`.

### 3. Split estratificado

```python
X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
```

`stratify=y` = "preservando a proporção do alvo" nos dois conjuntos. Sem isso,
o teste pode ficar quase sem casos positivos e as métricas viram loteria.

### 3b. Modelo bobo: por que a acurácia engana (Aula 12)

```python
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, recall_score

bobo = DummyClassifier(strategy="most_frequent").fit(X_treino, y_treino)   # responde sempre "não"
p = bobo.predict(X_teste)
print(f"acurácia {accuracy_score(y_teste, p):.2f} | recall {recall_score(y_teste, p, zero_division=0):.2f}")
# acurácia ~0.75 com recall 0: acerta 75% sem encontrar NENHUMA publicação que merecia
```

É o argumento para usar precisão, recall e F1. Na resposta: "um modelo que
dissesse sempre 'não' teria acurácia de ~75% e seria inútil".

### 4. Ajustar os modelos (escolha 3 da lista do enunciado)

```python
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB

modelos = {
    "Regressão logística": make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)),        # como na Aula 12 (ver nota abaixo)
    "Árvore de classificação": DecisionTreeClassifier(
        max_depth=4, random_state=42, class_weight="balanced"),
    "Random Forest": RandomForestClassifier(
        random_state=42, class_weight="balanced"),
    # "Extra Trees": ExtraTreesClassifier(random_state=42, class_weight="balanced"),
    # "AdaBoost": AdaBoostClassifier(random_state=42),        # não aceita class_weight
    # "Gaussian Naive Bayes": GaussianNB(),                    # não aceita class_weight
}

for modelo in modelos.values():
    modelo.fit(X_treino, y_treino)
```

**Padronize a logística.** A Aula 12 usa `LogisticRegression(max_iter=1000)`
direto; com features em escalas muito diferentes (seguidores na casa dos
milhares, hora de 0 a 23) isso pode dar `ConvergenceWarning` (testado). O
`make_pipeline(StandardScaler(), ...)` padroniza e ajusta num objeto só, e o
`.predict()` aplica a mesma transformação no teste.

**Balancear a logística ou não?** Na Aula 12, a árvore usa
`class_weight="balanced"` e a logística não: para a logística, o professor
compensa a classe rara **baixando o corte** (passo 6), e diz que os dois são
"o mesmo trade-off, por outro caminho". Usar os dois juntos compensa duas
vezes. Por isso aqui a logística fica sem `class_weight`. Se quiser ligar,
diga na resposta.

`AdaBoostClassifier` e `GaussianNB` **não aceitam** `class_weight`. Se
incluir, dá `TypeError`.

### 5. Tabela de precisão, recall e F1 + matriz de confusão

```python
from sklearn.metrics import (precision_score, recall_score, f1_score,
                             confusion_matrix, ConfusionMatrixDisplay)

linhas = []
for nome, modelo in modelos.items():
    previsto = modelo.predict(X_teste)
    linhas.append({
        "modelo": nome,
        "precisao": precision_score(y_teste, previsto, zero_division=0),
        "recall":   recall_score(y_teste, previsto, zero_division=0),
        "f1":       f1_score(y_teste, previsto, zero_division=0),
    })

tabela = pd.DataFrame(linhas).sort_values("f1", ascending=False)
print(tabela)

# matriz de confusão do modelo com maior F1
melhor_nome = tabela.iloc[0]["modelo"]
melhor = modelos[melhor_nome]
cm = confusion_matrix(y_teste, melhor.predict(X_teste))
ConfusionMatrixDisplay(cm, display_labels=["Não", "Sim"]).plot(cmap="Blues")
plt.title(f"Matriz de confusão — {melhor_nome}")
plt.show()
print(cm)
```

`zero_division=0` evita aviso/erro quando um modelo não prevê nenhum positivo
(acontece em base desbalanceada).

Atalho para ver tudo de uma vez:
```python
from sklearn.metrics import classification_report
print(classification_report(y_teste, melhor.predict(X_teste), zero_division=0))
```

### 6. Comparar cortes de decisão (0,50 × 0,30)

`predict()` usa corte 0,50 por padrão. Para outro corte, use a probabilidade:

```python
prob = modelos["Regressão logística"].predict_proba(X_teste)[:, 1]

linhas_corte = []
for corte in [0.50, 0.30]:                # <-- cortes do enunciado
    previsto_corte = (prob >= corte).astype(int)
    linhas_corte.append({
        "corte": corte,
        "precisao": precision_score(y_teste, previsto_corte, zero_division=0),
        "recall":   recall_score(y_teste, previsto_corte, zero_division=0),
        "f1":       f1_score(y_teste, previsto_corte, zero_division=0),
        "VP": int(((previsto_corte == 1) & (y_teste.values == 1)).sum()),   # acertos (como na Aula 12)
        "FP": int(((previsto_corte == 1) & (y_teste.values == 0)).sum()),   # alarmes falsos
    })

print(pd.DataFrame(linhas_corte))
```

`[:, 1]` pega a probabilidade da **classe 1** (a positiva). Use a **mesma
logística já ajustada** e o **mesmo conjunto de teste** — não reajuste nada.

### 7. Importância das características

```python
importancias = pd.Series(
    modelos["Árvore de classificação"].feature_importances_,   # árvore, floresta, extra trees, adaboost
    index=X_treino.columns
).sort_values(ascending=False)
print(importancias.head(5))
```

Aula 12: a importância mostra o que a árvore **mais usou** para separar as
classes nesta base — não é regra causal de como viralizar.

Se o modelo for regressão logística (não tem `feature_importances_`):
```python
log = modelos["Regressão logística"].named_steps["logisticregression"]
importancias = pd.Series(log.coef_[0], index=X_treino.columns).abs().sort_values(ascending=False)
```
Gráfico horizontal em `04-graficos.md`.

---

## Como ler a matriz de confusão

```
                previu Não   previu Sim
real Não            VN           FP
real Sim            FN           VP
```

- **VP** — merecia e o modelo indicou (acerto).
- **FP (falso positivo)** — **não** merecia, mas o modelo indicou → a equipe
  gasta um espaço escasso de divulgação em peça que não traria retorno.
- **FN (falso negativo)** — merecia, mas o modelo não indicou → a equipe
  **perde** uma publicação promissora.
- **VN** — não merecia e não foi indicada (acerto).

**Precisão** = dos que o modelo indicou, quantos realmente mereciam.
`VP / (VP + FP)` → protege contra **desperdício**.

**Recall** = dos que realmente mereciam, quantos o modelo encontrou.
`VP / (VP + FN)` → protege contra **oportunidade perdida**.

**F1** = média harmônica das duas; é o critério quando você quer equilíbrio.

### O trade-off do corte (o que o enunciado quer ver)

**Baixar o corte (0,50 → 0,30)** faz o modelo marcar mais peças como
positivas: **recall sobe, precisão tende a cair**. Subir o corte faz o
contrário.

Como decidir:
- **Poucos espaços de divulgação** e alto custo de desperdício → corte mais
  alto, prioriza **precisão**.
- **Custo maior em deixar passar** uma peça boa (e sobra capacidade de
  divulgar) → corte mais baixo, prioriza **recall**.

Na prova, **olhe a sua tabela** e justifique com os números que saíram. Se o
recall subir muito com pouca perda de precisão, o corte 0,30 se justifica; se
a precisão despencar, fique em 0,50.

## Resposta escrita — modelos prontos

**Por que classificação (e não os outros dois):**
> É um problema de **classificação**, porque o alvo
> (`mereceu_divulgacao_adicional`) é categórico: cada publicação recebe o
> rótulo 1 ou 0. **Regressão** não responde diretamente porque estimaria um
> número contínuo, e a decisão da equipe é binária (dar ou não divulgação
> adicional). **Clusterização** também não serve porque já sabemos o rótulo
> correto de cada publicação na base: não é preciso descobrir grupos, e sim
> aprender a prever uma categoria conhecida a partir das características.

**Decisão final e riscos de erro:**
> Escolhi o modelo **[NOME]**, que apresentou o maior F1 no conjunto de teste,
> com o corte de **[0,50 ou 0,30]**. Um **falso positivo** significa destinar
> um dos poucos espaços de divulgação a uma publicação que não traria retorno
> relevante — desperdício direto de um recurso escasso. Um **falso negativo**
> significa deixar de impulsionar uma publicação que teria bom desempenho,
> ou seja, oportunidade perdida. Ao baixar o corte para 0,30, o recall subiu
> de [X] para [Y] e a precisão caiu de [A] para [B]. Como faltam duas semanas
> para o festival e os espaços de divulgação são limitados, priorizei
> **[precisão/recall]**, aceitando [perder algumas peças boas / incluir
> algumas peças fracas] em troca de [não desperdiçar espaço / cobrir mais
> publicações promissoras].

Preencha [X], [Y], [A], [B] com os números da **sua** tabela — é isso que
diferencia uma resposta justificada de uma genérica.

## Armadilhas

- Base desbalanceada: **acurácia engana**. Um modelo que diz "não" para tudo
  acerta 75% e tem recall zero. Por isso o enunciado pede precisão/recall/F1.
- Métricas sempre no **teste**, nunca no treino.
- `zero_division=0` para não travar quando um modelo não prevê positivos.
- Não reajuste o modelo ao comparar cortes — use o `predict_proba` do que já
  está treinado.
- `stratify=y` no split; `class_weight="balanced"` nas árvores e florestas.
- **Só uma classe no treino ou no teste** (Aula 12): o corte ficou extremo demais — reveja o percentil.
