# 04 — Gráficos

**Regra que vale para todos:** título + nome dos dois eixos + **a fonte escrita dentro da figura**. Se o enunciado escreve `Fonte: ...`, isso precisa aparecer no gráfico, não só no texto da resposta. No template: **seção 7** (e 8, 9, 10, 11 para os gráficos específicos).

O estilo abaixo é o das aulas 6 a 13: `fig, ax = plt.subplots(...)`, `ax.set_...` e a fonte com `fig.text`.

## Fonte (defina uma vez)

```python
import matplotlib.pyplot as plt

FONTE = "Fonte: dados sintéticos do Festival ViraBairro (2026)"   # <-- troque

def fonte(fig):
    fig.text(0.01, -0.02, FONTE, fontsize=8, color="gray")      # igual às aulas
```

Se a fonte sumir ao exportar (ela fica logo abaixo da figura), use uma posição dentro dela: `fig.text(0.99, 0.01, FONTE, ha="right", fontsize=8, color="gray")`.

---

## Barras — comparar categorias

```python
serie = df.groupby("tema")["taxa_utilidade_pct"].median().sort_values(ascending=False)   # ordene ANTES

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(serie.index, serie.values, color="#3b6ea5")
ax.set_title("Qual tema as pessoas mais salvam ou compartilham?")    # <-- comunique a PERGUNTA
ax.set_xlabel("Tema")                                                 # <--
ax.set_ylabel("Mediana da taxa de utilidade (%)")                     # <-- com a unidade
fonte(fig)
fig.tight_layout()
plt.show()
```

Se o resumo veio do `.agg(...)` (um DataFrame), use `resumo.index` e `resumo["mediana"]`.

### Combinações de duas categorias (tema × formato)

```python
resumo2 = (df.groupby(["tema", "formato"])["taxa_engajamento_pct"]
           .agg(publicacoes="count", mediana="median")
           .sort_values("mediana", ascending=False).reset_index())
rotulos = resumo2["tema"] + " – " + resumo2["formato"]

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(rotulos, resumo2["mediana"], color="#27824c")
ax.set_title("Mediana da taxa de engajamento por tema e formato")
ax.set_xlabel("Combinação tema × formato")
ax.set_ylabel("Mediana da taxa de engajamento (%)")
ax.tick_params(axis="x", rotation=60)          # 16 rótulos não cabem retos
for r in ax.get_xticklabels():
    r.set_ha("right")
fonte(fig)
fig.tight_layout()
plt.show()
```

### Barras agrupadas (uma cor por formato) — mais legível

```python
matriz = df.pivot_table(index="tema", columns="formato", values="taxa_engajamento_pct", aggfunc="median")

fig, ax = plt.subplots(figsize=(10, 6))
matriz.plot(kind="bar", ax=ax)
ax.set_title("Mediana da taxa de engajamento por tema e formato")
ax.set_xlabel("Tema")
ax.set_ylabel("Mediana da taxa de engajamento (%)")
ax.legend(title="Formato")
ax.tick_params(axis="x", rotation=0)
fonte(fig)
fig.tight_layout()
plt.show()
```

## Barras horizontais — importância de variável

```python
top5 = importancias.head(5).sort_values()     # CRESCENTE: o barh desenha de baixo para cima

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(top5.index, top5.values, color="#c0392b")
ax.set_title("Características mais usadas pela árvore")
ax.set_xlabel("Importância")
ax.set_ylabel("Característica")
fig.tight_layout()
plt.show()
```

## Linha — evolução no tempo

```python
diario = df.groupby("dia_publicacao")["taxa_engajamento_pct"].mean().sort_index()   # ordem cronológica

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(diario.index, diario.values, marker="o", color="#c0392b")
ax.set_title("Taxa média de engajamento por dia")
ax.set_xlabel("Dia da publicação")
ax.set_ylabel("Taxa média de engajamento (%)")
ax.tick_params(axis="x", rotation=30)
fonte(fig)
fig.tight_layout()
plt.show()
```

`marker="o"` mostra onde há observação de verdade (Aula 6: importante quando são poucos dias). Dados fora do período (ex: um post de 2025 numa coleta de 2026) achatam o gráfico — a Aula 6 corta com `diario[diario.index >= pd.to_datetime("2026-04-01").date()]`.

## Dispersão — relação entre duas numéricas

```python
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(df["seguidores_autor"], df["taxa_engajamento_pct"], alpha=0.6, color="#27824c")
ax.set_title("Seguidores do autor vs. taxa de engajamento")
ax.set_xlabel("Seguidores do autor")
ax.set_ylabel("Taxa de engajamento (%)")
ax.set_xscale("log")      # Aula 6: sem log, as poucas contas gigantes esmagam as pequenas num canto
fonte(fig)
fig.tight_layout()
plt.show()
```

## Dispersão — real × previsto (regressão)

```python
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(y_teste, y_previsto, alpha=0.6, color="#3b6ea5")
lo = min(y_teste.min(), y_previsto.min())
hi = max(y_teste.max(), y_previsto.max())
ax.plot([lo, hi], [lo, hi], "--", color="gray", label="previsão = valor real")
ax.set_title("Valores reais vs. previstos — taxa de engajamento")
ax.set_xlabel("Valor real (%)")
ax.set_ylabel("Valor previsto (%)")
ax.legend()
fig.tight_layout()
plt.show()
```

A linha tracejada é "acertou exatamente". Acima dela o modelo superestimou; abaixo, subestimou.

## Matriz de confusão

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_teste, previsto)
ConfusionMatrixDisplay(cm, display_labels=["Não", "Sim"]).plot(cmap="Blues")
plt.title("Matriz de confusão — Random Forest")     # <-- nome do modelo
plt.show()
```

## Armadilhas

- **Um `plt.subplots()` por gráfico.** Reaproveitar o mesmo `ax` desenha um em cima do outro.
- `fig.tight_layout()` evita rótulo cortado; `plt.show()` no fim de cada um.
- Rótulos sobrepostos → `ax.tick_params(axis="x", rotation=45)` ou `figsize` maior.
- Barras vazias → a tabela usada tem 0 linhas; confira com `print(len(...))` antes (Aula 6).
- **Título comunica a pergunta** quando o enunciado pede isso: "Qual tema é mais salvo ou compartilhado?" é melhor que "Taxa por tema".
- Barras começam no zero (é o padrão — não mexa) e vão ordenadas pelo valor.
