[07-prova-2025-resolvida.md](https://github.com/user-attachments/files/32528565/07-prova-2025-resolvida.md)
# Prova A1 — 2025.2 (com gabarito)

> Extraído de `A1_Métodos_Estatísticos_Aplicados_às_Ciências_Sociais_GABARITO.ipynb`, na pasta da matéria. O arquivo original tinha 7 questões no enunciado, mas o gabarito disponível cobre as 3 primeiras (1.5 + 0.5 + 3 = 5 pontos) — confira se você tem uma versão mais completa antes da prova.

## Instruções originais da prova (pra saber o que esperar no formato)

- Avaliação individual, composta por várias questões.
- Consulta permitida a: materiais de aula, próprias anotações, internet.
- Consulta **proibida** a: colegas e LLMs (ChatGPT, Claude, Gemini etc.) — por isso a lógica desse repositório é ter tudo pronto **antes**.
- Celular/tablet proibidos durante a prova.
- Questão em branco = errada.
- **Sempre interprete os resultados.**
- **Não esqueça medidas de centro, dispersão e correlação de Pearson quando fizerem sentido.**

Setup usado:
```python
import pandas as pd
import altair as alt
alt.data_transformers.disable_max_rows()
```

---

## Questão 1 (1.5 pontos) — ENEM

Base de microdados do ENEM 2023 (amostra 1%) com variáveis qualitativas (cor/raça, sexo, tipo de escola, acesso à internet, renda familiar em faixas etc.) e quantitativas (notas).

**(a) Análise univariada de duas variáveis qualitativas:**

```python
alt.Chart(enem).mark_bar().encode(
    alt.X("TP_COR_RACA", sort='-y'),
    alt.Y('count()'),
    tooltip=['TP_COR_RACA', 'count()']
).properties(width=300)
```
> A maior parte se identifica como parda ou branca; participação indígena é muito baixa.

```python
alt.Chart(enem).mark_arc().encode(
    theta="count()", color="TP_SEXO", tooltip=['TP_SEXO', 'count()']
)
```
> Participantes do gênero feminino são maioria.

**(b) Bivariada: cor/raça × acesso à internet (tabela de dupla entrada):**

```python
tabela = enem.groupby(['TP_COR_RACA', 'Q025']).size().unstack(1)
tabela.loc['Total', :] = tabela.sum(axis=0)
tabela.loc[:, 'Total'] = tabela.sum(axis=1)

tabela_long = pd.pivot_table(enem, index=['TP_COR_RACA', 'Q025'], aggfunc='size')

# distribuição condicional de acesso à internet dentro de cada cor
(tabela_long / tabela_long.groupby(level=0).transform(sum) * 100)

# gráfico de barras segmentadas em percentual
aux = tabela_long.reset_index().rename(columns={0: 'contagem'})
alt.Chart(aux).mark_bar().encode(
    x=alt.X('contagem', stack="normalize"),
    y='TP_COR_RACA:N',
    color='Q025:N'
)
```
> Para todas as cores, mais de 75% têm acesso à internet. Indígenas são os que menos têm acesso (>23% sem acesso); brancos são os que mais têm (~95% com acesso). Olhando a distribuição condicional invertida (composição de quem NÃO tem acesso por cor): mais de 73% dos sem-acesso se autodeclaram negros (pardos + pretos), contra ~21% brancos — evidenciando desigualdade racial no acesso à internet.

---

## Questão 2 (0.5 ponto) — Série temporal de clima (INMET)

Dados diários (2020–2025) de uma estação meteorológica: chuva, radiação, temperatura, umidade, vento.

```python
clima = pd.read_csv(f'{folder}/inmet_A652_2020_2025.csv', sep=';')
clima['DATA (YYYY-MM-DD)'] = pd.to_datetime(clima['DATA (YYYY-MM-DD)'])

alt.Chart(clima).mark_line().encode(
    x='DATA (YYYY-MM-DD)',
    y=alt.Y('temp_max:Q', scale=alt.Scale(domain=[15, 45])),
    tooltip=['DATA (YYYY-MM-DD)', 'temp_max']
).properties(height=800, width=2000)
```
> Comportamento cíclico claro em todas as variáveis (chuva, temperatura, radiação, umidade), com falha de dados em um trecho de 2024. Chuva tem picos entre fev-abr; temperaturas extremas (máx. e mín.) tendem a ocorrer após o meio do ano (~setembro); radiação tem ciclo muito regular; umidade é cíclica mas com uma anomalia batendo 100% no início de 2023.

**Agregação por mês (resample):**

> ⚠️ O gabarito original usa `resample('M')`, que **dá erro nas versões atuais do pandas** — hoje é `'ME'` (mês) e `'YE'` (ano). Copiou daqui e deu `ValueError: 'M' is no longer supported`? Troque por `'ME'`.

```python
clima_idx = clima.set_index('DATA (YYYY-MM-DD)')
clima_mensal = clima_idx.resample('ME').temp_max.mean()   # no gabarito original: 'M'

alt.Chart(clima_mensal.reset_index()).mark_line().encode(
    x='DATA (YYYY-MM-DD)', y='temp_max:Q'
).properties(height=800, width=2000)
```

---

## Questão 3 (3 pontos) — Pesquisas nacionais (PNAD + Censo)

### Parte 1 — PNAD (0.5 ponto)

> Pergunta: rendimento domiciliar per capita médio (R$1.848) vs. mediano (R$1.177) — o que isso diz sobre a distribuição?

**Resposta-modelo:**
> A média ser bem maior que a mediana aponta para uma distribuição fortemente assimétrica à direita: poucas observações com renda muito elevada puxam a média para cima (a média não é resistente a valores atípicos, a mediana é). Isso reforça a desigualdade de renda no Brasil — muitos com renda baixa, poucos com renda muito mais alta.

### Parte 2 — Censo Demográfico 2010 (2.5 pontos)

**(a) Univariada de "Renda per capita" e outra variável, nível município:**

```python
censo_municipios = pd.read_csv(f'{folder}/Censo_municipios_2010.csv')

alt.Chart(censo_municipios).mark_bar().encode(
    alt.X("Renda per capita 2010", bin=alt.Bin(step=100)), y='count()'
)
censo_municipios["Renda per capita 2010"].describe()
```
> Distribuição de renda per capita por município é clássica: assimétrica à direita, concentrada em valores baixos. Média puxada por poucos municípios de renda alta (ex: São Caetano do Sul-SP, Niterói-RJ, ambos >R$2.000), enquanto o mínimo (Marajá do Sena-MA) é <R$100 — grande amplitude e desigualdade territorial. AIQ (Q3-Q1) = ~R$369,50 (metade central dos municípios entre R$281 e R$650).

Mesma lógica repetida para "Esperança de vida ao nascer" (quase simétrica, pouco desvio padrão → pouca desigualdade) e "Mortalidade infantil" / "Taxa de analfabetismo" (ambas assimétricas à direita, com concentrações regionais nos piores valores — Alagoas/Maranhão para mortalidade; Piauí/Alagoas/Paraíba/Pernambuco para analfabetismo).

**(b) Bivariada de dois indicadores, nível estado:**

```python
censo_estados = pd.read_csv(f'{folder}/Censo_estados_2010_desagregado.csv')

alt.Chart(censo_estados).mark_circle().encode(
    alt.X("Renda per capita 2010"),
    alt.Y("Taxa de analfabetismo - 18 anos ou mais de idade 2010"),
    tooltip=['Territorialidades', 'Renda per capita 2010', 'Taxa de analfabetismo - 18 anos ou mais de idade 2010']
)
censo_estados[['Renda per capita 2010', 'Taxa de analfabetismo - 18 anos ou mais de idade 2010']].corr(numeric_only=True)
```
> Relação linear negativa forte (r ≈ -0.79): quanto maior a renda per capita, menor a taxa de analfabetismo. Distrito Federal é um claro valor atípico (renda muito acima do padrão para sua taxa de analfabetismo). Removendo-o, r fica ainda mais forte (≈ -0.87) — o outlier estava **atenuando** a relação.

**(c) Boxplots comparativos (homem×mulher; branco×negro):**

```python
melted = censo_estados.melt(
    id_vars=['Territorialidades'],
    value_vars=['Desagregação HOMEM Renda per capita Censo', 'Desagregação MULHER Renda per capita Censo'],
    var_name='Category', value_name='Value'
)
alt.Chart(melted).mark_boxplot(extent=1.5, size=40).encode(
    alt.X("Value:Q"), alt.Y("Category:N")
).properties(height=200, width=600)
```
> Renda per capita por gênero: distribuições parecidas, ambas assimétricas à direita; mediana de homens um pouco maior; AIQ maior para homens (R$318 vs R$294) → maior dispersão entre homens; ambos têm valor atípico no Distrito Federal.

> Taxa de analfabetismo por raça (branco × negro): diferença substancial — distribuição de negros inteira deslocada à direita. Mediana de negros ~11% (mais de 4 p.p. acima da de brancos). AIQ semelhante entre os dois grupos, mas a distribuição de negros se alonga mais nos extremos (mín/máx).
