# 12 — Erros possíveis, questão por questão

Organizado pela ordem das questões do simulado. Antes de fechar cada questão,
bata o olho na lista dela. `11-erros-comuns.md` é por mensagem de erro; este
aqui é por questão.

---

## Os 4 erros que atravessam TODAS as questões

Estes não são de uma questão só — confira em todas:

1. **Arquivo errado.** Q1 e Q2 usam `publicacoes_brutas.csv`. Q3 a Q8 usam
   **somente** `publicacoes_analise.csv`. Usar a bruta onde o enunciado diz
   "use somente a de análise" invalida a questão.
2. **Taxa errada.** São **duas** taxas diferentes:
   - `taxa_utilidade_pct` = (compartilhamentos + salvamentos) / alcance × 100
     → você **cria**. Usada nas **Q2 e Q3**.
   - `taxa_engajamento_pct` → **já existe** na base de análise. Usada nas
     **Q4, Q5, Q6, Q7 e Q8**.
   Calcular utilidade onde se pede engajamento (ou vice-versa) muda todos os
   números e toda a resposta escrita.
3. **Média × mediana.** Q4 pede **média** da taxa por dia. Q2, Q3 e Q5 pedem
   **mediana**. Confira palavra por palavra.
4. **Variável nova.** Q2, Q4, Q5, Q7 e Q8 dizem "em uma nova variável" /
   "refaça de modo independente". Recarregue o CSV; não reaproveite o `df`
   tratado de outra questão.

---

## Questão 1 — Diagnóstico inicial

**O enunciado exige:** head(5) · shape · ausências **só das colunas com ≥1** ·
limitação em até 2 frases.

### Erros de código
- Mostrar `df.isna().sum()` inteiro, com as colunas que têm zero ausência.
  O enunciado pede "somente as colunas que têm ao menos uma" → filtre com
  `ausencias[ausencias > 0]`.
- Esquecer um dos três itens (o `shape` é o mais esquecido).
- Escrever só `df.shape` sem contexto. Melhor: `print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")`.
- Tentar limpar a base aqui. A Q1 é só diagnóstico — a limpeza é a Q2.

### Erros na resposta escrita
- Falar do código ("usei o isna para ver os ausentes") em vez de falar dos
  **dados**. A pergunta é sobre representatividade.
- Dizer apenas "a base tem valores ausentes". Isso é qualidade de dado, não
  limite de representatividade.
- Passar de 2 frases.
- **Certo:** O que a resposta precisa ter: recorte estreito (um festival, 8 semanas,
  dados sintéticos) → não generaliza para outras redes/públicos/bairros.

---

## Questão 2 — Tratamento dos registros

**O enunciado exige:** 5 tarefas de limpeza + `taxa_utilidade_pct` + tabela por
tema (contagem **e** mediana, ordenada) + decisões em até 4 frases.

### A armadilha principal: as datas
A base tem formatos misturados (`2026-08-05` e `25/08/2026`).
- `pd.to_datetime(s, errors="coerce")` sozinho → um dos formatos vira
  `NaT` e você **perde linhas sem perceber**.
- `format="mixed", dayfirst=True` (o jeito da Aula 10) → no pandas 3,
  **inverte dia e mês das ISO** com dia ≤ 12 (`2026-08-05` vira 8 de maio); no
  pandas 1.5, zera tudo. Não dá erro nenhum.
- **Certo:** `converter_data` do `02-limpeza.md` (seção 4 do template): ISO separado,
  método da aula só no resto. Certo em todas as versões.
- **Certo:** Depois confira: `df["data_publicacao"].isna().sum()` e `.min()/.max()`.
  Se aparecer mês fora de agosto/setembro, está errado.

### Erros de código
- `drop_duplicates()` sem `subset="id_publicacao"`. O enunciado pede
  duplicidade **por id**, e sem o subset só remove linhas 100% idênticas.
- Padronizar tema sem conferir depois. Rode
  `sorted(df["tema"].unique())` — tem que sobrar **4** temas. Se sobrar 7 ou
  12, a padronização não pegou tudo e todo o `groupby` sai errado.
- Esquecer `.str.strip()` — `" Cultura "` e `"Cultura"` continuam
  diferentes mesmo depois do `.title()`.
- Criar a taxa **antes** de tratar o denominador → `inf` na coluna
  (e `inf` não aparece em `isna()`).
- Errar a ordem da fórmula: é `(compart + salv) / alcance * 100`. Sem os
  parênteses no numerador o resultado muda.
- Esquecer `dropna`/filtro em `alcance <= 0`.
- Preencher contagens com `fillna(0)` sem justificar — zero afirma "teve
  zero", diferente de "não sabemos".
- Tabela só com a mediana, sem a **contagem** de publicações (o enunciado
  pede os dois).
- Esquecer `.sort_values("mediana", ascending=False)`.
- Salvar arquivo com `to_csv` — o enunciado diz explicitamente que não precisa.

### Erros na resposta escrita
- Listar o que fez sem dizer **por quê**. O enunciado pede: "se descartar,
  preencher ou converter algo, diga por quê".
- Passar de 4 frases (uma por decisão resolve).

---

## Questão 3 — Escolha de tema para divulgação

**O enunciado exige:** só a base de análise · criar `taxa_utilidade_pct` ·
mediana por tema · gráfico de barras · recomendação de 3 a 5 frases.

### Erros de código
- Usar `taxa_engajamento_pct` (que já existe na base) em vez de **criar**
  `taxa_utilidade_pct`. O enunciado diz "com a mesma fórmula da questão
  anterior" — é compartilhamentos + salvamentos.
- Usar `publicacoes_brutas.csv`. Aqui é **somente** a de análise.
- Refazer toda a limpeza da Q2. A base de análise já vem tratada; só criar
  a taxa basta.
- Usar média em vez de mediana.
- Não ordenar as barras (o gráfico fica ilegível para comparar).

### Erros no gráfico (valem ponto)
- Sem título.
- Sem `xlabel` **e** `ylabel` (os dois).
- **Sem a fonte dentro da figura.** O enunciado escreve
  `"Fonte: dados sintéticos do Festival ViraBairro (2026)"` e diz "no próprio
  gráfico". Escrever só no texto da resposta não conta.
- Título genérico ("Taxa por tema") quando o enunciado pede título "que
  comunique a pergunta" → use algo como "Qual tema as pessoas mais salvam ou
  compartilham?".

### Erros na resposta escrita
- Não indicar um tema. A pergunta pede escolha, não descrição.
- Não explicar **o que a mediana representa** (é item explícito do enunciado).
- Não apresentar limitação (também é item explícito).
- Afirmar causalidade ("esse tema gera mais compartilhamento"). O enunciado
  avisa: "não afirme causalidade".
- Ficar fora da faixa de 3 a 5 frases.
- Deixar o valor genérico sem colocar o número que saiu.

---

## Questão 4 — Acompanhamento diário

**O enunciado exige:** converter data · criar `dia_publicacao` · tabela diária
(qtd, **média** de engajamento, alcance **total**) ordenada cronologicamente ·
gráfico de linhas com fonte · recorte de reels ≥18h com top 5.

### Erros de código
- Usar **mediana** na tabela diária. Aqui o enunciado pede **média**.
- Usar média de `alcance` em vez de **soma** ("alcance total").
- `dia_publicacao` contendo data **e** hora. O enunciado pede "somente a
  data" → `.dt.date`.
- Não ordenar cronologicamente. Depois do `groupby` use `.sort_index()`
  (ou `.sort_values("dia_publicacao")` se tiver dado `reset_index`).
  Ordenar pelo valor da taxa é erro — o pedido é cronológico.
- No recorte, esquecer parênteses: `df[df["formato"]=="reel" & df["hora"]>=18]`
  dá erro. O certo é `df[(df["formato"]=="reel") & (df["hora"]>=18)]`.
- Usar `and` em vez de `&`.
- Recorte vazio e não perceber. Cheque `len(recorte)` e
  `df["formato"].unique()` — pode ser `"Reel"` com maiúscula.
- Interpretar "a partir das 18h" como `> 18`. É `>= 18`.
- Mostrar o top 5 sem as colunas pedidas. O enunciado lista exatamente:
  `id_publicacao`, `dia_publicacao`, `hora`, `tema`, `taxa_engajamento_pct`.
- Esquecer a fonte no gráfico de linhas (vale igual à Q3).

### Erros na resposta escrita
- Afirmar tendência ("o engajamento vem crescendo"). O enunciado pede
  explicitamente descrever a variação **sem** afirmar tendência de longo prazo.
- Não explicar por que o recorte de reels noturnos **não prova** que
  horário ou formato causam engajamento (é item explícito).
- Passar de 4 frases.

---

## Questão 5 — Tema e formato

**O enunciado exige:** uma linha por combinação tema×formato (contagem +
**mediana** de `taxa_engajamento_pct`) · ordenada decrescente · gráfico de
barras comparando as combinações · 4 a 6 frases.

### Erros de código
- Agrupar por uma variável só, ou fazer duas tabelas separadas (uma por
  tema, outra por formato). O enunciado quer o **cruzamento**.
- Usar `taxa_utilidade_pct` (da Q3) em vez de `taxa_engajamento_pct`.
- Usar média em vez de mediana.
- Esquecer a contagem de publicações.
- Esquecer `.reset_index()` e depois não conseguir montar o rótulo nem
  plotar.
- Não ordenar da maior para a menor mediana.
- Gráfico com 16 rótulos sobrepostos e ilegíveis → falta
  `plt.xticks(rotation=45, ha="right")` e `figsize` maior.
- Esquecer a fonte na figura.

### Erros na resposta escrita
- Não destacar **uma combinação específica** para testar (é pedido direto).
- Não explicar **por que comparar duas variáveis é diferente de analisar
  uma** — é o núcleo conceitual da questão, e é onde mais se perde ponto.
  A explicação: a mediana do tema sozinho mistura formatos e pode não
  corresponder a nenhuma situação real.
- Não registrar limitação (combinações com poucas publicações).
- Ficar fora da faixa de 4 a 6 frases.

---

## Questão 6 — Importância das variáveis na árvore

**O enunciado exige:** alvo pelo percentil 75 · **as mesmas features da Q8** ·
75/25 com `random_state=42` e estratificado · árvore `max_depth=4`,
`random_state=42`, pesos balanceados · tabela ordenada + gráfico horizontal do
top 5.

### Erros de código
- **Não ir ler a lista de features na Questão 8.** O enunciado manda usar
  "as mesmas características listadas na Questão 8" — é fácil não ver e
  inventar a própria lista.
- **Vazamento:** incluir `taxa_engajamento_pct` entre as features. O alvo
  foi criado a partir dela → o modelo acerta quase tudo e a importância fica
  toda nela. Sinal de alerta: importância ≈ 1.0 numa variável só.
- Incluir `alcance`, `interacoes`, `compartilhamentos`, `salvamentos` ou
  `id_publicacao`.
- Esquecer `pd.get_dummies` nas categóricas → `ValueError: could not
  convert string to float: 'Cultura'`.
- Usar `quantile(75)` em vez de `quantile(0.75)`.
- Usar `>=` no percentil quando o enunciado diz "acima do percentil 75" (`>`).
- Esquecer `stratify=y` ("preservando a proporção do alvo").
- Esquecer `class_weight="balanced"` ("pesos balanceados entre as classes").
- Esquecer `max_depth=4` ou `random_state=42`.
- Usar `train_test_split(..., test_size=0.75)` — 75% é **treino**, então
  `test_size=0.25`.
- No `barh`, ordenar decrescente: o matplotlib desenha de baixo pra cima e
  a maior barra vai parar embaixo. Ordene **crescente** (`sort_values()`).
- Gráfico horizontal sem título/eixos.

### Erros na resposta escrita
- Tratar importância como causa ("o horário determina o engajamento").
- Não citar **uma mudança concreta na base** que alteraria o ranking (é
  item explícito): entrada de um formato novo, concentração em um tema,
  mudança no alcance orgânico da plataforma.
- Passar de 4 frases.

---

## Questão 7 — Estimativa de engajamento (regressão)

**O enunciado exige:** dizer o tipo de aprendizado e por quê · features
listadas · 75/25 com `random_state=42` · regressão linear + árvore
`max_depth=4` · tabela MAE e R² · dispersão real×previsto do menor MAE com
linha de referência · até 5 frases.

### Erros de código
- Usar `stratify` aqui. Isso é de classificação; em regressão dá erro ou
  não faz sentido.
- **Vazamento:** usar `alcance`, `interacoes` ou `taxa_utilidade_pct`. O
  enunciado é explícito: "não use identificador, alcance, interações nem
  variáveis calculadas a partir da taxa".
- Usar `DecisionTreeClassifier` em vez de `DecisionTreeRegressor`.
- Calcular métricas no **treino**. É sempre em `X_teste`/`y_teste`.
- Esquecer o R² ou esquecer o MAE (pede os dois, em tabela).
- Escolher o modelo pelo R² quando o enunciado diz "para o modelo com menor
  MAE".
- Plotar a dispersão do modelo errado (tem que ser o de **menor MAE**).
- Esquecer a **linha de referência** onde previsão = valor real (item
  explícito).
- Trocar os eixos sem rotular — fica impossível saber o que é real e o que
  é previsto.

### Erros na resposta escrita
- Dizer "classificação" porque o resultado parece categorizável. O alvo é
  contínuo → **regressão**.
- Explicar MAE errado. MAE é o **erro médio absoluto na unidade do alvo**,
  não porcentagem de acerto nem "quão bom é o modelo" genericamente.
- Achar que **R² negativo** é erro seu. Não é — significa que o modelo é
  pior que chutar a média. Reporte e comente.
- Não indicar qual modelo escolheu.
- Não registrar a limitação causal.
- Passar de 5 frases.

---

## Questão 8 — Priorização de divulgação (classificação)

**O enunciado exige:** 8.1 tipo de aprendizado e por que os outros dois não ·
alvo pelo p75 · features permitidas · 75/25 `random_state=42` estratificado ·
**3 classificadores da lista** · tabela precisão/recall/F1 · matriz de confusão
do maior F1 · comparação dos cortes 0,50 e 0,30 · até 6 frases.

### Erros de código
- **Vazamento** — o erro mais grave desta questão. Usar
  `taxa_engajamento_pct` como feature faz o F1 ir a ~1.0. O enunciado diz:
  "isso seria vazamento de dados". Se o seu F1 der perto de 1, **desconfie**.
- Escolher modelo **fora da lista** do enunciado (regressão logística,
  árvore, Random Forest, Extra Trees, AdaBoost, Gaussian NB). KNN ou SVM não
  estão na lista.
- Usar 2 ou 4 modelos. São exatamente **três**.
- Passar `class_weight` para `AdaBoostClassifier` ou `GaussianNB` →
  `TypeError`. Esses dois não aceitam.
- Ligar `class_weight="balanced"` na logística **e** ainda baixar o corte:
  compensa a classe rara duas vezes. A Aula 12 usa um caminho ou o outro.
- Regressão logística sem escalonar → `ConvergenceWarning` e resultado
  ruim. Use `make_pipeline(StandardScaler(), LogisticRegression(...))`.
- Esquecer `stratify=y`.
- Reportar **acurácia**. O enunciado pede precisão, recall e F1 — e com
  base desbalanceada (25% positivos) a acurácia engana: um modelo que responde
  "não" sempre acerta 75%.
- `UndefinedMetricWarning` quando um modelo não prevê positivos → adicione
  `zero_division=0`.
- Mostrar a matriz de confusão do modelo errado. É a do **maior F1**.
- **Reajustar o modelo** para testar o corte 0,30. O enunciado diz "na
  regressão logística **já ajustada** e no **mesmo** conjunto de teste" — use
  `predict_proba` do modelo que já está treinado.
- Usar `predict()` e tentar mudar o corte. `predict()` é fixo em 0,50; o
  corte só muda via `predict_proba(X_teste)[:, 1] >= corte`.
- Pegar `[:, 0]` em vez de `[:, 1]` no `predict_proba` — `[:, 1]` é a
  probabilidade da classe positiva.
- Comparar cortes de um modelo que não é a logística.

### Erros na resposta escrita
- Na 8.1, explicar só por que é classificação e **não dizer por que
  regressão e clusterização não servem** — o enunciado pede os dois
  descartes explicitamente.
- Inverter falso positivo e falso negativo. No contexto:
  - **FP** = divulgou algo que não merecia → desperdício de espaço escasso.
  - **FN** = deixou de divulgar algo que merecia → oportunidade perdida.
- Escolher o corte sem olhar a tabela. A justificativa precisa citar os
  **seus** números (recall subiu de X para Y, precisão caiu de A para B).
- Dizer que 0,30 é "melhor" sem explicar o trade-off. Baixar o corte
  **aumenta recall e reduz precisão** — isso tem que aparecer.
- Não informar modelo **e** corte escolhidos (pede os dois).
- Passar de 6 frases.

---

## Varredura final (2 minutos, antes de enviar)

- [ ] Todas as células **executadas**, na ordem, sem erro visível
- [ ] Nenhum `NaT`/`NaN` inesperado depois das conversões
- [ ] `tema` com exatamente 4 categorias após padronizar
- [ ] Todo gráfico: título + xlabel + ylabel + fonte **na figura**
- [ ] Nenhum F1 suspeito perto de 1.0 (sinal de vazamento)
- [ ] Nenhum modelo usando `alcance`, `interacoes` ou a taxa-alvo
- [ ] Toda resposta dentro do limite de frases
- [ ] Nenhuma palavra causal: causa, provoca, garante, prova que
- [ ] Números reais preenchidos no lugar dos genéricos
- [ ] Nome e matrícula no notebook
