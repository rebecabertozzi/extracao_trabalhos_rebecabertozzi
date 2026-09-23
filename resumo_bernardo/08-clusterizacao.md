# 08 — Clusterização (agrupar sem rótulo)

**Como identificar:** **não existe variável-alvo**. A pergunta é "que grupos existem nessas publicações?", "como segmentar os perfis?", e não "prever X". É o **aprendizado não supervisionado** (Aula 13). No template: **seção 11**.

Mesmo quando a questão é de regressão ou classificação, o enunciado costuma pedir que você **explique por que não é clusterização** — a resposta pronta está no fim deste arquivo.

## Passo a passo

### 1. Escolher as variáveis

```python
COLS = ["seguidores_autor", "tamanho_legenda", "n_hashtags", "taxa_engajamento_pct"]   # <-- numéricas
base = df[COLS].dropna().copy()
```

Aqui **pode** usar variáveis de resultado (`taxa_engajamento_pct`, `alcance`): não há previsão, então não existe vazamento. O critério é outro — as variáveis devem fazer sentido juntas para descrever o que você quer agrupar. A Aula 13 avisa: **a escolha das variáveis decide o resultado** — outra lista daria outros grupos.

Só entram colunas numéricas (a aula usa `df.select_dtypes("number")`, sem o id). Categoria: `pd.get_dummies(..., dtype=int)` antes.

### 2. Log nas colunas de cauda longa e padronização

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

entrada = base.copy()
entrada["seguidores_autor"] = np.log1p(entrada["seguidores_autor"])   # <-- colunas de cauda longa
X_pad = StandardScaler().fit_transform(entrada)                      # média 0, desvio 1
```

- **Padronizar é obrigatório** (Aula 13): o KMeans mede distância, e sem padronizar `seguidores_autor` (dezenas de milhares) domina `n_hashtags` (0 a 5) — o KMeans agrupa praticamente só por seguidores.
- **Log em cauda longa** (seguidores, alcance, plays): sem ele, meia dúzia de contas gigantes vira um cluster sozinha (testado). É a mesma ideia da escala log do gráfico de dispersão da Aula 6.

### 3. Escolher o k: cotovelo e silhueta

```python
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

ks, inercias, silhuetas = list(range(2, 9)), [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X_pad)
    inercias.append(km.inertia_)
    silhuetas.append(silhouette_score(X_pad, km.labels_))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4))
ax1.plot(ks, inercias, marker="o", color="#3b6ea5")
ax1.set_title("Cotovelo: inércia por k"); ax1.set_xlabel("k (número de grupos)"); ax1.set_ylabel("inércia")
ax2.plot(ks, silhuetas, marker="o", color="#c0392b")
ax2.set_title("Silhueta média por k"); ax2.set_xlabel("k (número de grupos)"); ax2.set_ylabel("silhueta")
fig.tight_layout()
plt.show()
```

- **Cotovelo (inércia):** sempre cai quando k aumenta; procure onde ela **para de cair rápido** e a curva "dobra".
- **Silhueta:** de -1 a 1; escolha o k com a **maior**. Abaixo de ~0,2 em todo k = os dados quase não têm estrutura de grupo (resultado legítimo de reportar).
- Quando os dois apontam o mesmo k, dá confiança. Quando não, a escolha é sua — justifique.

### 4. Ajustar e perfilar (a parte que vale nota)

```python
K = 3                                                            # <-- k escolhido
base["cluster"] = KMeans(n_clusters=K, n_init=10, random_state=42).fit_predict(X_pad)

perfil = base.groupby("cluster")[COLS].mean().round(2)           # valores ORIGINAIS, para ler
perfil["tamanho"] = base["cluster"].value_counts().sort_index()
print(perfil)
print(base[COLS].mean().round(2))                                # compare com a média geral
```

Leia **comparando os grupos entre si e com a média geral**: qual tem mais seguidores, legenda mais longa, mais hashtags, engajamento maior.

### 5. Dar nome aos grupos (Aula 13)

```python
NOMES = {0: "criadores: legenda curta, muitas hashtags",          # <-- escreva a partir da tabela
         1: "institucionais: muitos seguidores, poucas hashtags",
         2: "coletivos: poucos seguidores, legenda longa"}
base["segmento"] = base["cluster"].map(NOMES)
```

A numeração (0, 1, 2) muda de execução para execução: escreva o dicionário **depois** de ler a sua tabela. Sem nomear e descrever, a questão fica incompleta.

### 6. Visualizar com PCA (Aula 13)

```python
from sklearn.decomposition import PCA

coords = PCA(n_components=2, random_state=42).fit_transform(X_pad)   # comprime tudo em 2 eixos, só para ver

fig, ax = plt.subplots(figsize=(7, 6))
for c in sorted(base["cluster"].unique()):
    sel = (base["cluster"] == c).values
    ax.scatter(coords[sel, 0], coords[sel, 1], s=14, alpha=0.6, label=NOMES[c])
ax.set_title("Publicações em 2 dimensões (PCA), coloridas por cluster")
ax.set_xlabel("componente 1"); ax.set_ylabel("componente 2")
ax.legend()
fig.text(0.01, -0.02, FONTE, fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

Grupos em regiões separadas, com alguma sobreposição nas bordas, é o esperado (Aula 13: "segmento é uma simplificação útil, não uma divisão perfeita da realidade").

---

## Os três tipos de aprendizado

| | Tem alvo? | Alvo é... | Exemplo no festival |
|---|---|---|---|
| **Regressão** | sim | número contínuo | estimar a taxa de engajamento esperada |
| **Classificação** | sim | categoria | prever se merece divulgação adicional |
| **Clusterização** | **não** | — | descobrir perfis de publicação sem rótulo prévio |

## Resposta escrita — "por que NÃO é clusterização"

> Clusterização não responde a essa pergunta porque é um método **não supervisionado**: ela agrupa registros semelhantes sem usar um rótulo conhecido. Aqui já sabemos o valor correto de cada publicação na base, e o objetivo é **prever** esse valor para peças novas — o que exige um método supervisionado.

## Resposta escrita — "por que É clusterização" e interpretação

> É um caso de clusterização porque não há variável-alvo: nenhuma coluna indica a que grupo cada publicação pertence, e o objetivo é **descobrir** agrupamentos pela semelhança entre as características. Padronizei as variáveis (e apliquei log em seguidores, de cauda longa) porque o KMeans mede distância e a coluna de maior escala dominaria. Escolhi k = **[K]** pelo cotovelo e pela maior silhueta (**[S]**). O grupo **[A]** reúne [descrição com números]; o **[B]**, [...]. Os grupos dependem das variáveis e do k escolhidos, e o KMeans supõe grupos "redondos" e de tamanho parecido — é uma segmentação útil, não a única possível.

## Armadilhas

- **Esquecer de padronizar** é o erro nº 1.
- Cluster minúsculo (3 ou 4 registros) = outliers numa coluna de cauda longa → log nela.
- `n_init=10` e `random_state=42` sempre.
- Os **números dos clusters não têm ordem**: o 2 não é "melhor" que o 0.
- `could not convert string to float` → sobrou coluna de texto; `Input contains NaN` → faltou `dropna`.
- Silhueta baixa em todo k — reporte honestamente, não force uma narrativa.
