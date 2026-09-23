
# Como ler a questão — Extração e Análise de Dados

22/09/2026

Como transformar o enunciado no código certo e o resultado numa resposta que dá ponto. Todo código citado aqui vem das aulas 5, 6, 10, 11, 12 e 13 ou da resolução do simulado. O código completo está em **codigos.md** e os conceitos em **conceitos.md**.

## 1. Garimpar a questão antes de escrever código

Faça isso em toda questão, nesta ordem:

1. **Leia o enunciado duas vezes e sublinhe cada verbo.** Cada verbo é uma entrega que vale ponto: "carregue", "mostre", "crie", "ordene", "faça um gráfico", "explique".
2. **Ache o arquivo.** Está sempre escrito: `dados/publicacoes_brutas.csv` (bruta, com sujeira) ou `dados/publicacoes_analise.csv` (já tratada). "Use somente" quer dizer que não pode usar o outro.
3. **Carregue numa variável nova** (`q3 = pd.read_csv(...)`). O enunciado pede questões independentes: não reaproveite tabela de outra questão.
4. **Rode `head()` e `columns`** pra ver o nome exato das colunas antes de usar.
5. **Identifique o tipo de pergunta** pela bússola abaixo: descrever, limpar, comparar grupos, acompanhar no tempo, estimar um número, decidir uma categoria ou agrupar.
6. **Anote os detalhes que mudam o código:** mediana ou média? ordem crescente ou decrescente? "somente as colunas com ausência"? "por id"? "preservando a proporção"? "horizontal"?
7. **Escreva o código, rode e olhe o resultado.** Só depois escreva a resposta, com os números da sua tela.
8. **Conte as frases** que o enunciado pede na Markdown ("até duas", "de 3 a 5", "até seis").

**Questão parece nova?** Quase sempre é uma combinação de peças conhecidas. A Q4 do simulado, por exemplo, é converter data + tabela por dia + gráfico de linha + filtro com duas condições + os 5 maiores. Quebre em pedacinhos e resolva um de cada vez.

## 2. Bússola: que questão é essa?

Olhe o que a pergunta quer saber e quantas variáveis ela envolve. Isso decide a técnica, o gráfico e a medida.

| A pergunta quer... | Pista no enunciado | Técnica | Gráfico | Medida | Simulado |
| --- | --- | --- | --- | --- | --- |
| conhecer a base | "diagnóstico", "primeiras linhas", "ausentes" | `head`, `shape`, `isna().sum()` | nenhum | contagens | Q1 |
| arrumar a base | "tratamento", "padronizar", "converter", "duplicidade" | limpeza da aula 10 | nenhum | linhas antes e depois | Q2 |
| comparar categorias de **uma** variável | "por tema", "comparar os temas" | `groupby` de 1 coluna + `agg` | barras | mediana ou média por grupo | Q3 |
| ver variação no tempo | "ao longo dos dias", "acompanhamento diário", "cronológica" | `to_datetime` + `.dt.date` + `groupby` | linha | média por dia | Q4 |
| achar os melhores de um grupo | "recorte", "apenas", "cinco maiores" | filtro + `nlargest` | nenhum | ranking | Q4 |
| cruzar **duas** variáveis categóricas | "combinação", "tema e formato", "aparecem juntos" | `groupby([...])` com lista | barras horizontais | mediana por combinação | Q5 |
| relacionar duas variáveis numéricas | "relação", "contas com mais seguidores..." | nenhuma conta, só olhar | dispersão | padrão visual | aula 6 |
| **estimar um número** | "estimar", "taxa esperada", alvo contínuo | regressão (aula 11) | dispersão real x previsto | MAE, R² | Q7 |
| **decidir sim ou não** | "merece", "viralizou", "percentil", "chance de" | classificação (aula 12) | matriz de confusão | precisão, recall, F1 | Q8 |
| saber o que o modelo usou | "importância", "características mais usadas" | `feature_importances_` | barras horizontais | importância 0 a 1 | Q6 |
| agrupar sem resposta pronta | "segmentar", "grupos parecidos", "perfis" | KMeans (aula 13) | dispersão com PCA | silhueta, inércia | aula 13 |

### Regressão, classificação ou clusterização?

Pergunte: **o que eu quero prever?**

- Um **número que pode ter decimal** (taxa, visualizações) → **regressão**.
- Uma **categoria**, normalmente 0 ou 1, criada por um corte ("acima do percentil 75") → **classificação**.
- **Nada**, só quero achar grupos parecidos → **clusterização**.

A mesma coluna pode virar as duas coisas. Na Q7, `taxa_engajamento_pct` é o alvo, então é regressão. Na Q8, a mesma taxa virou 0/1 pelo percentil 75, então é classificação.

### Mediana ou média?

Use **a que o enunciado pede**: Q2, Q3 e Q5 pedem mediana, a Q4 pede média. Se não disser, a mediana é mais segura quando há poucos posts virais puxando a média pra cima (aula 5). No `agg`, `"median"` é mediana e `"mean"` é média.

## 3. Dicionário: o enunciado diz, você escreve

Use Ctrl+F com a palavra do enunciado. Cada linha tem uma armadilha.

### Olhar e limpar

| O enunciado diz | Quer dizer | Código |
| --- | --- | --- |
| "cinco primeiras linhas" | as 5 do topo | `df.head()` |
| "quantidade de linhas e colunas", "dimensões" | tamanho da tabela | `df.shape` |
| "somente as colunas que têm ausência" | filtrar o resultado, não mostrar zeros | `a = df.isna().sum()` e `a[a > 0]` |
| "em uma nova variável", "parta novamente" | recarregar o arquivo do zero | `q2 = pd.read_csv(...)` |
| "duplicidade por id_publicacao" | mesmo id conta como repetido | `drop_duplicates(subset="id_publicacao", keep="first")` |
| "registro duplicado" (sem dizer coluna) | linha idêntica | `drop_duplicates()` |
| "padronizar", "forma consistente", "escritos de formas diferentes" | maiúscula, espaço e grafia | `.str.strip().str.lower()` + `.replace({...})` |
| "datas em formatos distintos" | coluna mistura formatos | duas passadas com `format="ISO8601"` e `dayfirst=True` |
| "converter para tipos adequados" | texto vira número ou data | `pd.to_numeric(..., errors="coerce")`, `pd.to_datetime(...)` |
| "tratar ausências de maneira justificada" | decidir e explicar | `dropna(subset=[...])` ou `fillna(...)` + frase "porque" |
| "sem criar informação" | não preencher com valor inventado | prefira `dropna` nos campos da fórmula |
| "valores inválidos" | zero onde divide, negativo, fora da escala | `df[df["alcance"] > 0]` |

### Calcular, agrupar, filtrar

| O enunciado diz | Quer dizer | Código |
| --- | --- | --- |
| "crie taxa = ... / alcance × 100" | coluna nova com a fórmula | `df["taxa"] = (a + b) / c * 100` |
| "tabela por tema" | uma linha por tema | `groupby("tema").agg(...)` |
| "número de publicações" | contar linhas | `("id_publicacao", "count")` |
| "mediana" / "média" / "total" | função do `agg` | `"median"` / `"mean"` / `"sum"` |
| "da maior para a menor" | decrescente | `sort_values(..., ascending=False)` |
| "cronológica" | data crescente | `sort_values("dia_publicacao")` |
| "combinação de tema e formato" | agrupar por duas | `groupby(["tema", "formato"])` |
| "somente a data", "dia_publicacao" | tirar a hora | `.dt.date` |
| "recorte apenas de reel a partir das 18h" | duas condições | `df[(df["formato"] == "reel") & (df["hora"] >= 18)]` |
| "a partir de" / "acima de" | maior ou igual / maior | `>=` / `>` |
| "as cinco com maior..." | top 5 | `nlargest(5, "coluna")` |

### Gráficos

| O enunciado diz | Código |
| --- | --- |
| "gráfico de barras" | `ax.bar(x, y)` |
| "barras horizontal" | `ax.barh(x, y)` (valor no eixo X) |
| "gráfico de linhas" | `ax.plot(x, y, marker="o")` |
| "dispersão" | `ax.scatter(x, y)` |
| "linha de referência onde previsão e real seriam iguais" | `ax.plot([minimo, maximo], [minimo, maximo], linestyle="--")` |
| "título que comunique a pergunta" | `ax.set_title("Qual tema...?")` |
| "eixos nomeados" | `ax.set_xlabel(...)` e `ax.set_ylabel(...)` |
| "fonte no próprio gráfico" | `fig.text(0.01, -0.02, "Fonte: ...", fontsize=8, color="gray")` |

### Modelos

| O enunciado diz | Quer dizer | Código |
| --- | --- | --- |
| "características disponíveis antes da publicação" | só a lista dada, nada de resultado | `X = df[CARACTERISTICAS]` |
| "transforme categorias em números" | texto vira colunas 0/1 | `pd.get_dummies(..., columns=["tema", "formato"])` |
| "não use alcance, interações, identificador" | evitar vazamento | deixe fora do X |
| "reserve 75% treino e 25% teste" | separar | `train_test_split(X, y, test_size=0.25, random_state=42)` |
| "preservando a proporção do alvo" | só em classificação | `stratify=y` |
| "profundidade máxima 4" | limitar a árvore | `max_depth=4` |
| "pesos balanceados entre as classes" | dar peso à classe rara | `class_weight="balanced"` |
| "percentil 75" | valor que separa os 25% maiores | `df["col"].quantile(0.75)` |
| "valor 1 quando acima do percentil" | criar o rótulo | `(df["col"] > corte).astype(int)` |
| "compare os cortes 0,50 e 0,30" | decidir pela probabilidade | `predict_proba(X_teste)[:, 1]` e `(prob >= corte)` |
| "modelo com maior F1" / "menor MAE" | escolher pela tabela | primeira linha depois de ordenar |

## 4. Como ler o que apareceu na tela

Antes de escrever, faça duas perguntas ao número: **quantos casos tem por trás dele?** E **qual a distância pro segundo colocado?** Se a distância for pequena e os casos poucos, você tem um empate, não um vencedor.

### .describe()

| Linha | O que é |
| --- | --- |
| `count` | quantos valores não ausentes |
| `mean` | média |
| `std` | desvio padrão (o quanto os valores se espalham) |
| `min` / `max` | menor e maior valor |
| `25%` / `50%` / `75%` | quartis; o `50%` é a mediana |

Média bem maior que a mediana: poucos posts virais puxando a média pra cima (aula 5).

### Tabelas por grupo

- Olhe sempre a coluna de **contagem**: mediana de 7 ou 8 publicações muda de posição por causa de uma peça só.
- Diferença de 0,05 ponto entre o 1º e o 3º é empate. Diga isso e aponte o que se separa de verdade (na Q3, trabalho ficou atrás).
- Numa tabela de duas variáveis, reagrupe na cabeça por uma delas. Na Q5, olhando tema por tema aparece que reel > carrossel > imagem em todos.

### Gráficos

- **Linha no tempo com poucos casos por dia:** o sobe e desce é em boa parte aritmética. Descreva a variação, nunca "tendência".
- **Top 5 de um recorte:** escolher os melhores de um grupo já filtrado não prova que o filtro funciona. Faltaria comparar com outros horários e formatos.
- **Dispersão real x previsto:** ponto acima da linha = previu mais do que aconteceu; abaixo = previu menos; nuvem larga = erro grande.

### Regressão

| Número | Como ler |
| --- | --- |
| **MAE** | quanto a previsão erra em média, **na unidade do alvo**. MAE 0,349 numa taxa em % = erra cerca de 0,35 ponto percentual |
| **R² = 1** | perfeito |
| **R² perto de 0** | igual a chutar a média sempre |
| **R² negativo** | pior que chutar a média |
| **R² de 0,95+ de primeira** | desconfie: quase sempre é vazamento |
| **modelo bobo** | chutar sempre a média do treino; o modelo de verdade tem que ganhar dele |
| **coeficiente** | só o **sinal** é comparável (+ sobe junto, − desce junto), porque as escalas são diferentes |

### Classificação

|  | modelo disse 0 | modelo disse 1 |
| --- | --- | --- |
| **era 0** | VN | **FP** = alarme falso |
| **era 1** | **FN** = deixou passar | VP |

| Número | Como ler |
| --- | --- |
| **precisão** | das que o modelo indicou, quantas eram de verdade |
| **recall** | das que eram de verdade, quantas o modelo achou |
| **F1** | equilíbrio entre precisão e recall |
| **acurácia** | acertos / total; engana quando a classe 1 é rara |
| **precisão 1,0 com recall baixo** | só aposta quando tem certeza e deixa muita coisa passar |
| **corte mais baixo** | normalmente mais recall e menos precisão; confira se houve mesmo troca |
| **poucos positivos no teste** | com 7 positivos, cada acerto muda o recall em cerca de 0,14 |

Traduza FP e FN pro caso: na Q8, FP = gastar um espaço de divulgação à toa; FN = deixar sem apoio uma peça que ia render.

### Importâncias e clusters

- **Importância** = o quanto a árvore usou a característica pra separar os dados de treino. Não é causa. Empate na segunda casa decimal = ranking instável.
- **Silhueta** perto de 1 = grupos bem separados; perto de 0 = ambíguos. **Inércia**: procure o cotovelo. Os números dos clusters (0, 1, 2) são só etiquetas.

## 5. Como escrever a resposta

Metade da nota do simulado está nos campos de Markdown. O enunciado quase sempre pede três coisas: **uma decisão**, **o que o número significa** e **uma limitação**. Responda as três, com os números da sua tela.

### Receita de uma boa resposta

1. **Leia o número:** "mobilidade tem a maior mediana, 1,15%, seguida de cultura, 1,13%..."
2. **Explique o que ele mede**, se o enunciado pedir: "a mediana é o valor do meio...", "o MAE de 0,349 significa que, em média, erra 0,35 ponto".
3. **Diga o tamanho da diferença e quantos casos tem por trás:** "diferença de 0,05 ponto, sobre 26 a 35 publicações".
4. **Entregue uma decisão mesmo assim:** "descartar trabalho e escolher entre os outros três por critério editorial".
5. **Feche com a limitação e a causalidade:** "isto é associação observada nesta base, não causa".

### O que dá e o que não dá ponto

| Dá ponto | Não dá ponto |
| --- | --- |
| "fiz X porque Y" | "limpei os dados e tratei os ausentes" |
| limitação que se vê na base: "só 36 registros, sem coluna de rede ou bairro" | "os dados podem ser limitados" |
| perceber o empate e dizer | apontar a barra mais alta como vencedora |
| traduzir o MAE pra unidade do caso | "o MAE mede o erro médio" e só |
| FP e FN no contexto ("gastar um espaço à toa") | a definição do livro |
| descrever só o que os prints mostraram | citar filtro que derrubou 0 linhas como tratamento |
| "associação", "nesta base", "nesta coleta" | "reel causa mais engajamento", "sempre", "garante" |

### Palavras proibidas sem ressalva

**causa, prova, garante, sempre, tendência, todos os públicos.** O simulado repete "não afirme causalidade", "sem afirmar tendência" e "apresente uma limitação" em quase toda questão. Ele está pedindo cautela, não ranking.

### Limitações que servem em quase toda questão

- **Amostra pequena:** poucos registros por grupo ou por dia; uma peça muda o resultado.
- **Uma base só:** uma organização, uma campanha, dados sintéticos; não generaliza.
- **Sem controle:** temas, formatos e horários não foram distribuídos de forma igual, então não dá pra separar o efeito de cada um.
- **Recorte escolhido pelo resultado:** o top 5 de um grupo filtrado não prova nada sobre o filtro.
- **Modelo instável:** poucos positivos no teste; trocar o `random_state` pode mudar o ranking.

## Checklist antes de entregar

- [ ] Cada questão carrega o próprio arquivo numa variável nova.
- [ ] Usei o arquivo certo (bruta só na Q1 e Q2 do simulado; "somente" a de análise nas outras).
- [ ] Mediana onde pediu mediana, média onde pediu média.
- [ ] Tabela ordenada como o enunciado pediu.
- [ ] Todo gráfico tem título, eixo X, eixo Y e fonte (se pedida).
- [ ] `get_dummies` nas categorias antes do modelo.
- [ ] Nada de resultado (alcance, interações, taxa) no X.
- [ ] `stratify=y` só na classificação.
- [ ] Datas conferidas com `.min()` e `.max()`.
- [ ] Todas as células foram executadas e mostram resultado.
- [ ] Cada resposta tem o número de frases pedido, com números da minha tela.
- [ ] Baixei a entrega e conferi nome, matrícula, código e respostas.
