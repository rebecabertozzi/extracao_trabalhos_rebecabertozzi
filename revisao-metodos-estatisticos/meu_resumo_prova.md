[meu_resumo_prova.md](https://github.com/user-attachments/files/32495260/meu_resumo_prova.md)
# Meu Resumo — Métodos Estatísticos

*Resumo enxuto, feito enquanto eu estudo. Vou atualizando conforme avanço nos temas.*

---

## 0. Como abrir tudo no dia da prova

1. Abrir o link do Colab da prova (ela manda o link direto).
2. Baixar as bases que ela mandar (no Teams/OneDrive): selecionar tudo → Baixar → vira um `.zip`.
3. No Colab: ícone de pasta 📁 (barra lateral esquerda) → ícone de upload → selecionar o `.zip` → Abrir.
4. Rodar numa célula de código:
   ```python
   !unzip -o nome_do_arquivo.zip
   ```
   Isso descompacta os arquivos direto dentro do Colab. Depois eles aparecem soltos no painel de Arquivos.
5. Importar o pandas (sempre a primeira coisa a rodar):
   ```python
   import pandas as pd
   ```

---

## 1. Como ler o enunciado ("garimpar a questão")

Antes de escrever qualquer código, faço isso:

1. **Acho o nome do arquivo** que o enunciado menciona (ex: "dados no arquivo HABILITA.xls").
2. **Identifico o que está sendo pedido**: descrever uma variável? comparar grupos? medir associação/correlação?
3. **Abro o arquivo**:
   ```python
   df = pd.read_csv('nome.csv')        # se for .csv
   df = pd.read_excel('nome.xls')      # se for .xls ou .xlsx
   ```
4. **Olho as colunas disponíveis**:
   ```python
   df.head()      # mostra as 5 primeiras linhas
   ```
5. **Escolho a análise certa** com base na tabela abaixo (Bloco 2).

> O nome do arquivo é sempre dado no enunciado — não precisa adivinhar.

### "Unidade de análise" / "observações originais"

Quando a pergunta menciona isso, ela quer saber: **cada linha da tabela representa o quê?** — e, se a tabela já vier resumida (tipo percentuais por categoria), quer saber o que existia **antes** desse resumo.

Pergunta pra responder: *"esses números vieram de alguém sendo perguntado/contado, um por um. Quem é esse 'alguém'?"* Ex: uma tabela de % de estudantes por área → a unidade de análise original é **o estudante individual** (cada um respondeu uma área, e só depois isso virou % agregado por área).

### Verificar consistência dos dados

Significa: **checar se os números fazem sentido matemático**. Na maioria dos casos, isso é: os percentuais somam ~100%? (já que cada observação só entra numa categoria).

```python
df['NOME_DA_COLUNA'].sum()
```

- Deu **exatamente ou muito perto de 100%** → consistente, a diferença é só arredondamento.
- Deu **bem menos que 100%** → normalmente sinal de que faltam categorias na tabela (o enunciado costuma avisar, tipo "só os mais populares").

---

## 2. Bússola: que análise fazer?

| Tipo de pergunta | Variáveis | Gráfico | Medida |
|---|---|---|---|
| Descrever | 1 qualitativa | Barras / Setores | % de cada categoria |
| Descrever | 1 quantitativa | Histograma | Média/mediana, desvio padrão/AIQ |
| Comparar grupos | 1 quanti + 1 quali | Boxplot lado a lado | Mediana e AIQ de cada grupo |
| Medir associação | 2 qualitativas | Tabela dupla entrada / barras segmentadas | % condicional |
| Medir correlação | 2 quantitativas | Dispersão | r de Pearson |

---

## 3. Pandas básico (o que já testei)

| Código | O que faz |
|---|---|
| `pd.read_csv('arquivo.csv')` | Lê um arquivo CSV e vira uma tabela |
| `pd.read_excel('arquivo.xls')` | Lê um arquivo Excel/.xls e vira uma tabela |
| `df.head()` | Mostra as 5 primeiras linhas da tabela |
| `df.shape` | Mostra (nº de linhas, nº de colunas) |

**Nome da tabela (`df`) — quando mudar:** `df` é só um apelido que eu escolho, não é fixo.
- **1 arquivo só na questão** → pode chamar de `df` mesmo.
- **2 ou mais arquivos ao mesmo tempo** (ex: comparar dois grupos) → dar um nome diferente pra cada um, tipo `df_cn` e `df_ny`, ou `df1` e `df2`. Se usar `df` pras duas leituras, a segunda **apaga** a primeira da memória (perde os dados do primeiro arquivo).

---

## 4. Tipos de variáveis

Duas grandes famílias, cada uma com 2 subtipos:

| Família | Subtipo | O que é | Exemplo |
|---|---|---|---|
| Qualitativa | Nominal | Categorias **sem** ordem | time de futebol, religião, UF |
| Qualitativa | Ordinal | Categorias **com** ordem | nível de satisfação, escolaridade, faixa etária |
| Quantitativa | Discreta | Vem de **contar** (não tem decimal) | nº de filhos, nº de homicídios |
| Quantitativa | Contínua | Vem de **medir** (pode ter decimal) | renda, taxa, altura |

**Algoritmo pra classificar qualquer variável:**
1. É categoria ou número-quantidade?
2. Se categoria → tem ordem lógica? Sim = ordinal / Não = nominal
3. Se número-quantidade → veio de contar ou medir? Contar = discreta / Medir = contínua

**Pegadinhas:**
- Número às vezes é só um código disfarçado (ex: 1=fundamental, 2=médio, 3=superior) → isso é **ordinal**, não quantitativo. Tirar média não faz sentido.
- Renda/idade em **faixas** (ex: "R$1000-3000") deixa de ser contínua e vira **ordinal** — porque você não sabe mais o valor exato, só a "gaveta".
- Taxas e percentuais são sempre **quantitativa contínua**.

---

## 5. Pizza (setores) ou barras? Como decidir

Os dois servem pra 1 variável qualitativa. A diferença é a quantidade de categorias:
- **Poucas categorias (até uns 5-6), que somam 100%** → pizza é aceitável
- **Muitas categorias (7+)** → sempre barras (fatias de pizza ficam pequenas e difíceis de comparar)
- Na dúvida, **barras é a escolha mais segura**.

---

## 6. Histograma e assimetria

Histograma = "gráfico de barras" de variável **quantitativa**: em vez de categorias, o eixo x é dividido em **faixas** (classes/bins) de um número, e a altura da barra é quantas observações caem em cada faixa. As barras ficam coladas (não são categorias soltas, é uma "régua" cortada em pedaços).

**Forma da distribuição** — olha pra onde a "cauda" (parte fina, esticada) do histograma aponta:

![Assimetria: simétrica, à direita e à esquerda](imgs/assimetria.svg)

- Cauda pra **direita** (valores altos) → assimetria à direita → **média > mediana**
- Cauda pra **esquerda** (valores baixos) → assimetria à esquerda → **média < mediana**
- Sem cauda de nenhum lado, os dois lados parecidos → simétrica → média ≈ mediana

Dá pra confirmar a forma sem nem olhar o gráfico, só comparando média e mediana no `.describe()`.

---

## 7. `.describe()` — o que cada linha quer dizer

```python
df['NOME_DA_COLUNA'].describe()
```

Resume uma coluna numérica em 8 números. Exemplo real (coluna `PctNascFora`, 51 estados):

```
count    51.000000
mean      8.401961
std       6.053908
min       1.200000
25%       3.800000
50%       6.300000
75%      12.500000
max      27.200000
```

| Linha | Nome | O que é |
|---|---|---|
| `count` | contagem | Quantas observações (linhas) existem — aqui, 51 estados |
| `mean` | média | Soma tudo e divide pela quantidade |
| `std` | desvio padrão | O quanto os valores variam/se espalham em torno da média. Maior = mais espalhado |
| `min` | mínimo | O menor valor de todos |
| `25%` | Q1 (1º quartil) | 25% dos dados ficam **abaixo** desse valor |
| `50%` | mediana (Q2) | O valor bem no meio: metade abaixo, metade acima |
| `75%` | Q3 (3º quartil) | 75% dos dados ficam **abaixo** desse valor |
| `max` | máximo | O maior valor de todos |

**Como pensar no Q1/mediana/Q3:** imagina todas as observações em fila, ordenadas do menor pro maior. Essa fila é cortada em 4 pedaços iguais (25% cada). Q1 é o corte depois do 1º pedaço, a mediana é o corte no meio (depois do 2º), Q3 é o corte depois do 3º.

```
[ 1º pedaço 25% ] Q1 [ 2º pedaço 25% ] Mediana [ 3º pedaço 25% ] Q3 [ 4º pedaço 25% ]
```

**Resumo dos 5 números** = min, Q1, mediana, Q3, max (as 5 linhas do describe, tirando count/mean/std). É a resposta pronta quando a questão pedir "dê o resumo dos 5 números".

---

## 8. AIQ e a regra 1,5×AIQ (valor atípico)

**AIQ (amplitude interquartil)** = Q3 − Q1. É o "tamanho" da metade central dos dados — a régua de quanta variação é considerada normal nessa distribuição.

**Pra que serve:** o AIQ é o ingrediente da fórmula que define os limites de "normalidade". Fora desses limites, o valor é considerado atípico:

```
limite_inferior = Q1 − 1,5 × AIQ
limite_superior = Q3 + 1,5 × AIQ
```

Qualquer observação **menor** que o limite inferior ou **maior** que o limite superior é um **valor atípico (outlier)**.

**Pegadinha importante — maior valor ≠ valor atípico:** ser o maior (ou menor) valor da distribuição não significa automaticamente que ele é atípico. Pode ser só o "topo natural" da distribuição, dentro do esperado. É preciso **aplicar a regra** pra confirmar: só é atípico se realmente ultrapassar o limite calculado.

**Exemplo real (% nascidos fora, por estado):** Q1 = 3,8, Q3 = 12,5 → AIQ = 8,7 → limite superior = 12,5 + 1,5×8,7 = 25,55. Como a Califórnia tem 27,2% (acima de 25,55), ela **é** atípica — não é só a maior observação, ela realmente foge do padrão.

---

## 9. Série temporal (gráfico de linha)

Usar quando a variável quantitativa é medida **ao longo do tempo** (ano, mês, data). Gráfico de linha, tempo no eixo x.

```python
df.plot(x='NOME_COLUNA_TEMPO', y='NOME_COLUNA_VALOR', kind='line')
plt.show()
```

**"Padrão geral" — o que o gráfico está fazendo, de forma ampla:**

| Padrão | Como a linha se comporta | Exemplo |
|---|---|---|
| Tendência de crescimento | Sobe o tempo todo | Mensalidade de faculdade subindo ano a ano |
| Tendência de queda | Desce o tempo todo | Preço de um produto caindo com o tempo |
| Estável / sem tendência | Fica sempre perto do mesmo nível | Uma taxa que não muda muito ano a ano |
| Cíclico / sazonal | Sobe e desce **repetidamente**, em padrão que se repete | Vendas de sorvete: sobe todo verão, cai todo inverno |

**Desvios do padrão geral** — o que responder quando a questão pedir isso: mesmo dentro de uma tendência geral (ex: crescimento), olhar o gráfico com atenção e procurar por:
- Trechos onde a subida **acelera** (fica mais "em pé", mais inclinada)
- Trechos onde a subida **desacelera** ou fica "achatada" (quase um platô)
- Quedas pontuais (mesmo numa tendência geral de alta)
- Valores atípicos isolados (um ponto muito fora do resto)

**Como responder:** dizer **qual desvio** aconteceu e **em que período/anos**. Ex: *"Entre 1994-2000 o crescimento desacelera (quase um platô); a partir de 2000 acelera bastante, especialmente até 2005 e de novo entre 2008-2010."*

**Valor bruto (R$/US$) ou percentual de aumento? Qual estudar:**

Exemplo pra entender o porquê: duas pessoas recebem um aumento de **exatamente $10**. Pessoa A ganhava $100 → 10% de aumento. Pessoa B ganhava $1000 → só 1% de aumento. Mesmo valor em dólar, "peso" bem diferente.

- Se a série **cresce bastante ao longo do tempo** (a base fica cada vez maior, como mensalidade de faculdade) → melhor usar o **percentual de aumento ano a ano**. Um mesmo salto em $ significa coisas diferentes dependendo da altura da série — o percentual normaliza isso e mostra melhor onde o crescimento realmente acelerou/desacelerou.
- Se a série é **mais estável**, sem uma base que cresce muito (valores ficam numa faixa parecida o tempo todo) → o **valor bruto já é suficiente**, não precisa complicar com percentual — a diferença entre os dois seria pequena e não mudaria a leitura do gráfico.

**Valor bruto vs. percentual de aumento:** quando o valor já vem crescendo o tempo todo, olhar só os números brutos dificulta ver **quando** o crescimento acelerou ou desacelerou (um "ano ruim" ainda parece alto perto do início da série). O **percentual de aumento ano a ano** resolve isso, porque normaliza a comparação.

---

## 10. Moda e boxplot

**Moda** = o valor que mais se repete nos dados. Diferente da média e da mediana:
- Pode **não existir** moda (se nenhum valor se repetir).
- Pode existir **mais de uma** (se dois ou mais valores empatarem como os mais frequentes).

```python
df['NOME_DA_COLUNA'].mode()
```

**Boxplot** = desenho visual do resumo dos 5 números (o mesmo do `.describe()`), numa "caixa":

```
        limite         Q1      mediana    Q3        limite
      inferior          |          |       |        superior
         |----------[   caixa: Q1 até Q3   ]----------|
      (bigode)                                     (bigode)
```

| Parte do desenho | O que representa |
|---|---|
| Caixa (retângulo) | Vai do Q1 até o Q3 — os 50% "do meio" dos dados |
| Linha dentro da caixa | Mediana |
| Bigode de baixo | Vai do Q1 até o **menor valor que não é atípico** |
| Bigode de cima | Vai do Q3 até o **maior valor que não é atípico** |
| Ponto separado (fora do bigode) | Valor atípico — calculado com a mesma regra 1,5×AIQ que já uso |

**Boxplot SEM valor atípico:** os bigodes vão direto até o mínimo e o máximo reais dos dados (porque nenhum valor ultrapassa os limites do 1,5×AIQ).

**Boxplot COM valor atípico:** o bigode **para no limite** (`Q1 − 1,5×AIQ` ou `Q3 + 1,5×AIQ`), não no valor extremo real — e o(s) valor(es) além do limite aparece(m) como **ponto(s) isolados**, separados do bigode.

**Exemplo numérico:** dados `5, 10, 10, 15, 20, 25, 30, 90`. Q1=10, Q3=25 → AIQ=15 → limite superior = 25 + 1,5×15 = 47,5. Como 90 > 47,5, ele é atípico. No boxplot: o bigode de cima só vai até **30** (maior valor dentro do limite), e o **90 aparece como uma bolinha isolada** bem acima do bigode.

```python
df['NOME_DA_COLUNA'].plot(kind='box')
plt.show()
```

**Boxplots lado a lado (pra comparar 2 grupos):** ver seção de código — dá pra colocar duas colunas no mesmo gráfico e comparar visualmente mediana, dispersão (tamanho da caixa) e atípicos entre os grupos.

**Exemplo real (Questão 7 — tempo de viagem ao trabalho, CN vs NY):**
- CN: resumo dos 5 números min=5, Q1=10, mediana=20, Q3=30, max=60 — boxplot **sem** valor atípico, o bigode de cima vai direto até 60 (o máximo real).
- NY: resumo dos 5 números min=5, Q1=15, mediana=22,5, Q3=41,25, max=85 — boxplot **com** valor atípico: AIQ = 41,25−15 = 26,25 → limite superior = 41,25 + 1,5×26,25 = 80,625. Como 85 > 80,625, é atípico → o bigode de cima para em 65 (maior valor dentro do limite) e o 85 aparece como bolinha isolada.
- Lado a lado, dá pra ver que NY tem mediana um pouco maior, caixa (dispersão) bem mais larga, e um trabalhador que é atípico (viagem muito mais longa que o resto) — CN não tem nenhum atípico.

---

## 11. Tabela de dupla entrada (associação entre 2 qualitativas)

Usar quando tem **2 variáveis qualitativas** e a pergunta é algo tipo "como [variável A] depende de [variável B]?" — quer saber se existe relação entre elas.

**3 tipos de percentual que dá pra calcular numa tabela cruzada:**

| Tipo | O que é | Quando usar |
|---|---|---|
| Conjunto | Uma célula específica ÷ total geral | Raramente é o que a questão pede |
| Marginal | Total de uma linha ou coluna ÷ total geral | Pra saber o "peso" de cada categoria sozinha |
| **Condicional** | Uma célula ÷ total **da sua própria linha (ou coluna)** | Quase sempre é isso que a questão quer — compara categorias **dentro de** cada grupo |

**Como saber se é condicional por linha ou por coluna:** a variável que "explica"/"causa" vai nas linhas, e você divide cada célula pelo total da própria linha. Ex: "como fumar depende do tratamento?" → tratamento explica, então tratamento nas linhas, e cada % é calculado dividindo pelo total daquele tratamento (não pelo total geral).

```python
tabela = df.pivot_table(index='COLUNA_QUE_EXPLICA', columns='COLUNA_RESULTADO', values='COLUNA_CONTAGEM')
percentual = tabela.div(tabela.sum(axis=1), axis=0) * 100
```

**Exemplo real (Questão 9 — CESSAFUMO, parar de fumar):** tratamento (Chantix/Bupropion/Placebo) explica o resultado (fumou ou não). Tabela cruzada:

| Tratamento | Não fumou | Fumou |
|---|---|---|
| Chantix | 155 | 197 |
| Bupropion | 97 | 232 |
| Placebo | 61 | 283 |

Percentual condicional (dividindo cada linha pelo total daquele tratamento): Chantix 44,03% não fumaram, Bupropion 29,48%, Placebo 17,73%. **Conclusão:** Chantix foi o tratamento mais eficaz — quase o dobro da taxa de sucesso do Bupropion, e bem mais que o dobro do Placebo.

---

## 12. Diagrama de dispersão (2 variáveis quantitativas)

Usar quando tem **2 variáveis quantitativas** e a pergunta pede pra ver se elas **se relacionam** (ex: "há associação entre X e Y?").

```python
df.plot(x='COLUNA_EXPLICATIVA', y='COLUNA_RESPOSTA', kind='scatter')
plt.show()
```

Cada ponto do gráfico é uma observação (ex: um estado). A posição horizontal (X) é o valor da variável explicativa, a posição vertical (Y) é o valor da variável resposta.

**Direção da associação** (olhando a "nuvem" de pontos):
- Pontos sobem da esquerda pra direita → associação **positiva** (quando um sobe, o outro sobe)
- Pontos descem da esquerda pra direita → associação **negativa** (quando um sobe, o outro desce)

**Concordância ou discordância:** isso depende do **significado** de cada variável no contexto da questão (não é automático — precisa pensar). Ex: se "valor baixo = bom" nas duas variáveis, uma associação **positiva** significa que elas **concordam** (os dois sobem ou descem juntos, mesmo sentido). Se uma tem "valor baixo = bom" e a outra "valor baixo = ruim", uma associação positiva já seria **discordância**. Sempre reler o que cada variável representa antes de responder.

**Valor atípico no diagrama de dispersão:** aqui não tem uma regra numérica como o AIQ — é **visual**: um ponto que fica bem separado/isolado da "nuvem" geral, fora do padrão que os outros pontos seguem.

**Exemplo real (Questão 8 — Estados Felizes):** BRFSS (escore de felicidade subjetiva, menor = mais feliz) x Posto/CompDif (ranking objetivo, Posto 1 = mais feliz). O gráfico mostrou associação **negativa** (Posto sobe, BRFSS desce). Como Posto baixo = feliz objetivamente e BRFSS baixo = feliz subjetivamente, a associação negativa significa que estados menos felizes objetivamente (Posto alto) tinham BRFSS mais baixo (mais felizes subjetivamente) — ou seja, as medidas **discordam**. Valor atípico: Louisiana, com BRFSS = 0,033, bem acima do esperado para seu Posto.

---

## 13. Unidimensional vs. bidimensional

- **Unidimensional** = olhar **1 variável de cada vez**, sozinha (histograma, média, mediana, 5 números, moda, describe...).
- **Bidimensional** = olhar **2 variáveis ao mesmo tempo**, relacionando uma com a outra, pra ver se existe associação entre elas.

| Se as 2 variáveis forem... | Ferramentas da análise bidimensional |
|---|---|
| Ambas qualitativas | Tabela de dupla entrada (percentual condicional) |
| Ambas quantitativas | Diagrama de dispersão + correlação de Pearson |

Muitas questões pedem as duas coisas juntas: primeiro uma análise unidimensional de cada variável separada, depois a bidimensional relacionando as duas.

---

## 14. Correlação de Pearson (r)

Quando as 2 variáveis são **quantitativas**, o diagrama de dispersão só dá uma impressão visual (positiva/negativa), mas não diz **quão forte** é essa associação, e isso é subjetivo de pessoa pra pessoa. O **coeficiente de correlação de Pearson (r)** resolve isso: é um número entre -1 e +1 que resume ao mesmo tempo a **direção** e a **força** da associação.

```python
df['COLUNA_1'].corr(df['COLUNA_2'])
```

**Como ler o valor de r:**

| Valor de r | Interpretação |
|---|---|
| próximo de **+1** | associação positiva forte |
| próximo de **0** | associação fraca ou inexistente |
| próximo de **-1** | associação negativa forte |

O sinal (+ ou −) confirma a direção que já víamos no gráfico de dispersão; o quão perto de 1 (em valor absoluto) mostra a força.

**Pegadinha do sinal:** olhar primeiro se o número é negativo ou positivo — isso decide de qual lado da reta ele mora — e só depois olhar o tamanho (ignorando o sinal) pra ver se está "bem na ponta" ou "no meio":

```
-1 -------- -0,87 -------- 0 -------- +0,87 -------- +1
```

`-0,87` está perto do **-1** (correlação negativa forte). Já `+0,87` estaria perto do **+1** (correlação positiva forte). É fácil ler rápido demais e esquecer o sinal de menos — sempre conferir se o resultado veio negativo antes de classificar.

**Exemplo real (Questão 10 — Escores SAT por estado):** variáveis `PctSAT` (% de alunos que fizeram o SAT) e `SAT-Mat` (média do escore de matemática). Diagrama de dispersão mostrou associação negativa (nuvem descendo). Calculando: `df['PctSAT'].corr(df['SAT-Mat'])` = **-0,87** → correlação **negativa forte**. Resposta à pergunta do enunciado ("o % que faz o SAT ajuda a explicar as diferenças na média?"): **sim** — quanto maior o percentual de alunos que fazem a prova num estado, menor tende a ser a média (porque quando poucos fazem, geralmente são só os mais preparados).

---

## 15. Temas que ainda vou preencher aqui
*(conforme a gente for vendo, viram seções novas)*

- [ ] (nada pendente no momento)
