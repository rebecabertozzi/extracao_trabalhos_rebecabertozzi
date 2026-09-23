# Fluxograma rápido — o que fazer em cada questão

## Passo 1 — Qual arquivo a questão manda usar?

- **`*_brutas.csv`** (base suja) → diagnóstico e limpeza antes de tudo: `01-diagnostico.md` e `02-limpeza.md` (seções 3 e 4 do template)
- **`*_analise.csv`** (já tratada) → carregue **em variável nova** e use direto, sem limpar de novo

## Passo 2 — Que tipo de tarefa a questão pede?

- **Conhecer a base** (head, shape, ausências) → `01-diagnostico.md` (seção 3)
- **Limpar** (duplicata, texto, data, número, ausente) → `02-limpeza.md` (seção 4)
- **Criar uma taxa com fórmula** → `02-limpeza.md` (seção 5)
- **Tabela por grupo** (contagem + mediana, tema × formato, hashtags) → `03-agrupar-e-tabelas.md` (seção 6)
- **Gráfico** → `04-graficos.md` (seção 7) — veja "Qual gráfico usar" abaixo
- **Por dia, recorte, top 5** → `05-datas-e-recortes.md` (seção 8)
- **Prever um número** (taxa esperada) → regressão, `06-regressao.md` (seção 9)
- **Prever uma categoria** (merece / não merece) → classificação, `07-classificacao.md` (seção 10)
- **Agrupar sem rótulo** (segmentos, perfis) → clusterização, `08-clusterizacao.md` (seção 11)
- **Extrair de HTML** → `09-scraping-e-apis.md` (seção 12)

## Passo 3 — Checklist do que o professor sempre cobra

- [ ] Recarreguei o arquivo **em variável nova** quando o enunciado pediu
- [ ] Usei a medida pedida (**mediana ≠ média**) e a taxa pedida (**utilidade ≠ engajamento**)
- [ ] Gráfico com **título que comunica a pergunta**, **os dois eixos nomeados** e **a fonte dentro da figura**
- [ ] Nos modelos: `random_state=42`, split 75/25, **nenhuma feature de depois da publicação**
- [ ] Comparei com o **modelo bobo** (regressão) / não usei acurácia como critério (classificação)
- [ ] **Escrevi a interpretação** (nunca deixar só código ou gráfico), com os números do `>>> PARA A RESPOSTA`
- [ ] Incluí uma **limitação** e **não afirmei causalidade**
- [ ] Respeitei o **limite de frases** do enunciado

## Qual modelo usar (prever ou agrupar)

| Situação | Tipo | Métrica | Detalhe que cai |
|---|---|---|---|
| Existe alvo e ele é **número contínuo** | Regressão | MAE (menor = melhor) e R² | sem `stratify`; compare com o modelo bobo |
| Existe alvo e ele é **categoria** | Classificação | precisão, recall, F1 | `stratify=y`; matriz do maior F1; cortes com `predict_proba` |
| **Não existe alvo** | Clusterização | cotovelo + silhueta | padronizar (e log em cauda longa); dar nome aos grupos |

## Qual gráfico usar

| Situação | Gráfico |
|---|---|
| Comparar categorias (tema, formato) | Barras, ordenadas do maior pro menor |
| Combinações de duas categorias (tema × formato) | Barras com rótulo combinado, ou barras agrupadas (`pivot_table(...).plot(kind="bar")`) |
| Evolução no tempo | Linha com `marker="o"`, em ordem cronológica |
| Relação entre duas numéricas | Dispersão (escala log se poucos valores gigantes esmagam o resto) |
| Quão bem a regressão acertou | Dispersão real × previsto + linha tracejada "previsão = real" |
| O que o modelo mais usou | Barras horizontais (`barh`), top 5, ordenadas **crescente** |
| Acertos e erros da classificação | Matriz de confusão |
| Escolher o k / ver os grupos | Cotovelo + silhueta / PCA colorido por cluster |

## Ordem da limpeza

```
1. duplicatas    drop_duplicates(subset="id")
2. texto         strip + lower/title    -> confira: sobrou o número certo de categorias?
3. números       to_numeric(errors="coerce")
4. datas         converter_data         -> confira: o período bate com o enunciado?
5. inválidos     denominador <= 0 ou ausente: descarta
   ausentes      parcela de soma: preenche com a mediana
6. taxa          (a + b) / c * 100      -> confira: sem inf, sem negativo
```

Cada passo vira **uma frase** na resposta: o que fez e **por quê**.

## Regra do rótulo por percentil

```
corte = df["taxa"].quantile(0.75)
y = (df["taxa"] > corte).astype(int)      "acima do percentil 75" = >  (não >=)
```
Resultado: ~25% vira classe 1 → base **desbalanceada** → `stratify=y` e F1 no lugar de acurácia.

## Regra do vazamento

Para cada feature, pergunte: **esse dado já existe antes de publicar?**
- Sim: tema, formato, hora, dia da semana, seguidores, legenda, hashtags, duração → pode usar.
- Não: alcance, interações, curtidas, compartilhamentos, salvamentos, a taxa que gerou o alvo → **vazamento**, tire.
- R² ou F1 perto de 1 de primeira → quase certamente vazamento.

## Corte de decisão — o que muda quando baixa de 0,50 para 0,30

- **Recall sobe** → o modelo encontra mais publicações que mereciam (menos falso negativo = menos oportunidade perdida).
- **Precisão cai** → indica mais publicações que não mereciam (mais falso positivo = espaço de divulgação desperdiçado).
- Poucos espaços para divulgar → prefira **precisão** (corte mais alto). Custo maior em deixar passar → prefira **recall** (corte mais baixo).

## Média vs. mediana

- **Mediana** = valor típico (metade acima, metade abaixo). **Resistente** a publicações virais fora da curva.
- **Média** é puxada por poucos valores extremos. Média bem maior que mediana → poucos posts muito altos puxando.
- Grupo com poucas publicações → mediana instável → cite como **limitação**.

## Datas misturadas — a armadilha

`format="mixed", dayfirst=True` (Aula 10) **inverte dia e mês** das datas `2026-08-05` no pandas 3, sem dar erro. Use o `converter_data` (seção 4 do template) e confira `min()` e `max()` depois.
