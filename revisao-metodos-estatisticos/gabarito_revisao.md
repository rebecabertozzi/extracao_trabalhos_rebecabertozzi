[gabarito_revisao (3).md](https://github.com/user-attachments/files/32519846/gabarito_revisao.3.md)


# Gabarito da Revisão

*Respostas das questões do notebook `Revisão.ipynb`, resolvidas junto com o Claude.*

## Índice — questão × técnica usada

1. [Questão 1 — Classificação de variáveis](#questão-1--classifique-as-variáveis) *(teoria, sem código)*
2. [Questão 2 — Gráfico de barras](#questão-2--qual-área-de-estudo-arquivo-habilitaxls)
3. [Questão 3 — Gráfico de barras + categoria "Outros"](#questão-3--você-ouve-rádio-arquivo-formatoradioxls)
4. [Questão 4 — Histograma + AIQ](#questão-4--nascidos-fora-arquivo-nascidosforaxls)
5. [Questão 5 — Gráfico de linha / série temporal](#questão-5--custo-faculdade-arquivo-faccustoxls)
7. [Questão 7 — Boxplot (moda, mediana, comparação de 2 grupos)](#questão-7--tempo-de-viagem-ao-trabalho-arquivos-tempoviagemcnxls-e-tempoviagemnyxls)
9. [Questão 9 — Tabela de dupla entrada](#questão-9--parar-de-fumar-arquivo-cessafumoxls)
8. [Questão 8 — Diagrama de dispersão (associação/concordância)](#questão-8--estados-felizes-arquivo-felicidadexls)
10. [Questão 10 — Dispersão + Correlação de Pearson](#questão-10--escores-sat-estaduais-arquivo-satmatxls)
11. [Questão 11 — Pesquisa externa](#questão-11--índice-de-desenvolvimento-da-educação-básica-ideb) *(sem código)*
6. [Questão 6 — Histograma](#questão-6--emissão-co2-arquivo-emissaoco2xls)
12. [Questão 12 — Classificação de faixas + Tabela de dupla entrada](#questão-12--análise-de-renda-arquivo-infofamiliasentrevistadascsv)
13. [Questão 13 — Histograma + Dispersão + Pearson](#questão-13--idh-oecd-arquivo-oecd_idh_datacsv)
14. [Questão 14 — Bivariada geral (todas as técnicas, conforme o par)](#questão-14--censo-demográfico-dos-estados-brasileiros-em-2000-arquivo-censo_estadosxlsx)

*(Se algum link não pular certinho, usa Ctrl+F e busca o número da questão.)*

---

## Questão 1 — Classifique as variáveis

> Classifique as variáveis abaixo segundo seus tipos:
> - (a) Quantidade de homicídios no Brasil em 2023.
> - (b) Time de futebol.
> - (c) Taxa de desemprego.
> - (d) Nível de satisfação com o governo do Presidente Lula
> - (e) Denominação religiosa
> - (f) Renda per capita

| Item | Variável | Tipo |
|---|---|---|
| a | Quantidade de homicídios no Brasil em 2023 | Quantitativa discreta |
| b | Time de futebol | Qualitativa nominal |
| c | Taxa de desemprego | Quantitativa contínua |
| d | Nível de satisfação com o governo do Presidente Lula | Qualitativa ordinal |
| e | Denominação religiosa | Qualitativa nominal |
| f | Renda per capita | Quantitativa contínua |

---

## Questão 2 — Qual área de estudo? (arquivo HABILITA.xls)

> Cerca de 1,5 milhão de estudantes se matricularam em faculdades e universidades em 2008.
>
> No arquivo HABILITA.xls estão dados sobre o percentual de estudantes de primeiro ano que pretendiam se habilitar em diversas áreas disciplinares.
>
> - (a) Quem eram, originalmente, as observações (unidades de análise) que geraram esses dados percentuais?
> - (b) Verifique a consistência desses dados.
> - (c) Faça uma análise desses dados a partir de gráficos e escreva uma breve interpretação dos resultados.

```python
df = pd.read_excel('HABILITA.xls')
df.head()

df['Percentual'].sum()   # (b) verificar consistência

df.sort_values('Percentual', ascending=False).plot(x='Área', y='Percentual', kind='bar')
plt.show()
```
*(Os nomes `'Percentual'` e `'Área'` podem ser diferentes no seu arquivo — confirme com `df.head()`.)*

**(a)** Originalmente, a unidade de análise era o estudante individual (calouro de 2008). Cada estudante respondeu em qual área disciplinar pretendia se habilitar, e esses dados foram depois agregados em percentuais por área — que é o que a tabela mostra.

**(b)** A soma dos percentuais é 99,9%, muito próxima de 100%. A pequena diferença é explicada por arredondamento nos valores individuais, não indicando inconsistência nos dados.

**(c)** Gráfico de barras (10 categorias, muitas pra pizza). Administração foi a área mais procurada (16,8%), seguida por Profissional (13,8%) e Artes&Humanidades (13,5%). A área menos procurada foi Técnico (1%).

---

## Questão 3 — Você ouve rádio? (arquivo FORMATORADIO.xls)

> O serviço de classificação Arbitron coloca as estações de rádio norte-americanas em mais de 50 categorias que descrevem o tipo de programa que transmitem. Quais formatos atraem maior audiência?
>
> No arquivo FORMATORADIO.xls estão as medidas dos níveis de audiência (pessoas com 12 anos ou mais) em um dado instante do tempo, para os formatos mais populares.
>
> - (a) Qual a soma dos níveis de audiência para esses formatos? Qual o percentual da audiência de rádio que ouve estações em outros formatos?
> - (b) Seria correto apresentar esses dados em um gráfico de setores? Por quê?
> - (c) Faça um gráfico de barras para apresentar esses dados. Certifique-se de incluir uma categoria "Outro formato".

```python
df = pd.read_excel('FORMATORADIO.xls')
df.head()

df['NivelAudiencia'].sum()          # (a) → deu 67,3
100 - df['NivelAudiencia'].sum()    # (a) → deu 32,7

df = df._append({'Formato': 'Outro formato', 'NivelAudiencia': 32.7}, ignore_index=True)

df.sort_values('NivelAudiencia', ascending=False).plot(x='Formato', y='NivelAudiencia', kind='bar')
plt.show()
```

**(a)** A tabela lista 12 formatos de rádio, com soma dos níveis de audiência = 67,3%. Como a Arbitron classifica mais de 50 categorias no total (e a tabela só traz os mais populares), a diferença até 100% corresponde aos formatos não listados: **100 − 67,3 = 32,7%** da audiência ouve estações em "outros formatos".

**(b)** Não seria adequado usar gráfico de setores (pizza), pois há 13 categorias no total (12 formatos + "outros"). Com tantas fatias, o gráfico fica poluído e difícil de comparar visualmente. Gráfico de barras é mais apropriado.

**(c)** Gráfico de barras com "Outro formato" incluído (32,7%). Apesar de ser a maior fatia isolada (é o agrupado dos formatos menos populares), entre os formatos individuais Notícias/Conversa/Informação e Sertaneja lideram (~12,5-12,6%), seguidos por Contemporâneo Adulto (8,2%). Os demais formatos têm audiência mais baixa e parecida entre si.

---

## Questão 4 — Nascidos Fora (arquivo NASCIDOSFORA.xls)

> Como os residentes nascidos fora dos Estados Unidos estão distribuídos?
>
> O país, como um todo, tem 13% de residentes nascidos fora, mas nos estados esses percentuais variam de 1.2% na Virgínia Ocidental a 27.2% na Califórnia.
>
> O arquivo NASCIDOSFORA.xls apresenta os dados para os 51 estados.
>
> - (a) Faça um histograma e analise brevemente seu resultado. Use classes de largura 5% começando em 0%. Isto é, a primeira barra cobre de 0% a < 5%, a segunda cobre de 5% a < 10%, e assim por diante.
> - (b) Dê o resumo dos 5 números da distribuição.
> - (c) A Califórnia é um potencial valor atípico ou simplesmente a maior observação da distribuição? O que diz a regra 1.5×AIQ?

```python
df = pd.read_excel('NASCIDOSFORA.xls')
df.head()

df['PctNascFora'].plot(kind='hist', bins=range(0, 30, 5), edgecolor='black')
plt.show()

df['PctNascFora'].describe()

Q1 = df['PctNascFora'].quantile(0.25)
Q3 = df['PctNascFora'].quantile(0.75)
AIQ = Q3 - Q1
limite_superior = Q3 + 1.5 * AIQ
print(limite_superior)
```

**(a)** Histograma (classes de largura 5%, começando em 0%) mostra distribuição assimétrica à direita: a maioria dos estados (33 de 51) tem entre 0% e 10% de residentes nascidos fora, com frequência decrescente até poucos estados acima de 20%.

**(b)** Resumo dos 5 números: mínimo = 1,2%, Q1 = 3,8%, mediana = 6,3%, Q3 = 12,5%, máximo = 27,2%.

**(c)** AIQ = Q3 − Q1 = 12,5 − 3,8 = 8,7. Limite superior = Q3 + 1,5×AIQ = 12,5 + 13,05 = 25,55%. Como a Califórnia tem 27,2% (acima de 25,55%), ela é um **valor atípico** pela regra 1,5×AIQ — não é apenas a maior observação da distribuição.

---

## Questão 5 — Custo Faculdade (arquivo FACCUSTO.xls)

> O arquivo FACCUSTO.xls possui os dados médios sobre mensalidades e taxas de matrícula cobradas de alunos do estado por faculdades e universidades de 4 anos, para os anos acadêmicos de 1980 a 2010. Os valores são dados em "dólares constantes", ajustados para terem o mesmo poder de compra de um dólar em 2010.
>
> - (a) Faça um gráfico temporal das mensalidades e taxas médias.
> - (b) Que padrão geral seu gráfico apresenta?
> - (c) Alguns possíveis desvios do padrão geral são valores atípicos, períodos em que as taxas caíram (em dólares de 2013), e períodos de aumentos particularmente rápidos. Quais estão presentes em seu gráfico, e durante quais anos?
> - (d) Ao procurar por padrões, você acha que seria melhor o estudo de uma série temporal das taxas para cada ano ou o percentual de aumento para cada ano? Por quê?

```python
df = pd.read_excel('FACCUSTO.xls')
df.head()

df.plot(x='Ano', y='Mensalidade', kind='line')
plt.show()
```
*(Confirme os nomes reais das colunas de ano e mensalidade com `df.head()` — podem vir com outro nome no seu arquivo.)*

**(a)** Gráfico de linha (ano no eixo x, mensalidade no eixo y) — mensalidade sobe de ~$2.100 (1980) para ~$7.500 (2010).

**(b)** Padrão geral: tendência de crescimento constante — a mensalidade sobe ao longo de todo o período, sem nenhuma queda.

**(c)** Principal desvio: aceleração do crescimento a partir dos anos 2000. Entre 1994-2000 o crescimento é mais lento (quase um platô); a partir de 2000 a subida acelera bastante, especialmente até 2005 e de novo entre 2008-2010. Não há quedas nem valores atípicos isolados.

**(d)** Melhor estudar o percentual de aumento ano a ano. Como a mensalidade já vem de uma base crescente, um mesmo aumento em dólares representa uma aceleração diferente dependendo do ano — o percentual normaliza essa comparação e mostra melhor em quais anos o crescimento realmente acelerou ou desacelerou.

---

## Questão 7 — Tempo de viagem ao trabalho (arquivos TEMPOVIAGEMCN.xls e TEMPOVIAGEMNY.xls)

> A Pesquisa da Comunidade Americana pergunta, dentre muitas outras coisas, o tempo de viagem para o trabalho. No arquivo TEMPOVIAGEMCN.xls temos o tempo de viagem para 15 trabalhadores da Carolina do Norte, escolhidos aleatoriamente pelo Census Bureau, e no arquivo TEMPOVIAGEMNY.xls temos o tempo de viagem para o trabalho de 20 trabalhadores do estado de Nova York, escolhidos aleatoriamente.
>
> Faça uma análise completa desses dados a partir da média, moda, mediana, quartis, boxplot e valores atípicos.
>
> Não se esqueça de interpretar os resultados e também fazer análises comparativas entre as duas bases de dados.

```python
df_cn = pd.read_excel('TEMPOVIAGEMCN.xls')
df_cn.head()
df_cn['Minutos'].describe()
df_cn['Minutos'].mode()
df_cn['Minutos'].plot(kind='box')
plt.show()

df_ny = pd.read_excel('TEMPOVIAGEMNY.xls')
df_ny.head()
df_ny['Minutos'].describe()
df_ny['Minutos'].mode()
df_ny['Minutos'].plot(kind='box')
plt.show()

comparar = pd.DataFrame({'Carolina do Norte': df_cn['Minutos'], 'Nova York': df_ny['Minutos']})
comparar.plot(kind='box')
plt.show()
```

**Carolina do Norte (15 trabalhadores):** média = 22,47 min, moda = 10 min, mediana = 20 min, Q1 = 10, Q3 = 30, máximo = 60. Nenhum valor atípico (o boxplot mostra os bigodes indo direto até o mínimo e o máximo reais).

**Nova York (20 trabalhadores):** média = 31,25 min, moda = 15 min, mediana = 22,5 min, Q1 = 15, Q3 = 41,25, máximo = 85. **Tem um valor atípico**: AIQ = 41,25 − 15 = 26,25 → limite superior = 41,25 + 1,5×26,25 = 80,625. Como 85 > 80,625, esse trabalhador é atípico — o boxplot mostra o bigode de cima parando em 65 (maior valor dentro do limite) e o 85 aparece como ponto isolado.

**Análise comparativa:** os trabalhadores de Nova York gastam, em geral, mais tempo pra chegar ao trabalho que os da Carolina do Norte — tanto a média (31,25 vs 22,47) quanto a mediana (22,5 vs 20) são maiores em NY. A dispersão (variação) também é bem maior em NY: a caixa do boxplot é mais larga (Q3−Q1 = 26,25 em NY contra 20 em CN), e é só em NY que aparece um valor atípico — um trabalhador com tempo de viagem bem acima do padrão do grupo. Ou seja, além de os nova-iorquinos gastarem mais tempo em média, o tempo de viagem entre eles também varia mais.

---

## Questão 9 — Parar de fumar (arquivo CESSAFUMO.xls)

> Um grande experimento aleatorizado foi realizado para avaliar a eficácia de Chantix para parar de fumar, comparado com bupropion (mais comumente conhecido como Wellbutrin ou Zyban) e um placebo. Chantix é diferente da maioria dos produtos para parar de fumar, pois tem como alvo os receptores de nicotina no cérebro, ataca-os e impede que a nicotina os alcance, enquanto o bupropion é um antidepressivo muito usado para ajudar as pessoas a pararem de fumar.
>
> Fumantes com boa saúde geral que fumavam, pelo menos, 10 cigarros por dia, foram associados aleatoriamente aos tratamentos com Chantix (n = 352), com bupropion (n = 329), ou com o placebo (n = 344). A medida da resposta é a cessação contínua do fumo para as semanas 9 a 12 do estudo.
>
> O arquivo CESSAFUMO.xls é uma tabela de dupla entrada dos resultados.
>
> Se um sujeito fumou nas semanas 9 a 12, como isso depende do tratamento recebido?

```python
df = pd.read_excel('CESSAFUMO.xls')
df.head()

tabela = df.pivot_table(index='Tratamento', columns='Fumou', values='Contagem')
tabela

percentual = tabela.div(tabela.sum(axis=1), axis=0) * 100
percentual
```

Tabela de dupla entrada (tratamento x resultado):

| Tratamento | Não fumou | Fumou | Total |
|---|---|---|---|
| Chantix | 155 | 197 | 352 |
| Bupropion | 97 | 232 | 329 |
| Placebo | 61 | 283 | 344 |

Percentual condicional (dentro de cada tratamento, % que não fumou nas semanas 9-12): **Chantix 44,03%**, **Bupropion 29,48%**, **Placebo 17,73%**.

**Resposta:** fumar ou não nas semanas 9-12 depende fortemente do tratamento recebido. O Chantix foi o tratamento mais eficaz para parar de fumar, com a maior taxa de cessação (44,03%) — quase o dobro da taxa do Bupropion (29,48%) e mais que o dobro da taxa do Placebo (17,73%). O Placebo teve o pior resultado, como esperado por não ter princípio ativo: 82,27% dos participantes continuaram fumando.

---

## Questão 8 — Estados Felizes (arquivo FELICIDADE.xls)

> A felicidade humana, ou bem-estar, pode ser avaliada subjetivamente ou objetivamente. Uma avaliação subjetiva pode ser feita, ouvindo-se o que as pessoas dizem. Uma avaliação objetiva pode ser feita a partir de dados relacionados a bem-estar, como renda, preços das casas, ausência de congestionamentos de tráfego etc. As avaliações subjetivas e objetivas coincidem? Para estudar esse assunto, os investigadores fizeram avaliações, tanto subjetivas como objetivas, para cada um dos 50 estados norte-americanos (que constam no arquivo FELICIDADE.xls).
>
> A medida subjetiva foi o escore médio de questões de satisfação com a vida, encontradas no Behavioral Risk Factor Surveillance System (BRFSS), um sistema de pesquisas de saúde com base nos estados. Menores escores indicam um maior grau de felicidade. Para a avaliação objetiva da felicidade, os investigadores calcularam um escore de bem-estar (chamado escore de compensação de diferenciais) para cada estado, com base em medidas objetivas relacionadas à felicidade e ao bem-estar. Os estados foram, então, ordenados de acordo com esse escore (Posto 1 sendo o mais feliz).
>
> - (a) Faça um diagrama de dispersão do BRFSS médio (variável resposta) contra o posto com base nos escores de compensação de diferenciais (variável explicativa).
> - (b) Há uma associação geral positiva ou uma associação geral negativa entre BRFSS e o posto com base no método de compensação de diferenciais?
> - (c) A associação geral mostra concordância ou discordância entre o escore médio subjetivo BRFSS e o posto com base nos dados objetivos usados no método de compensação de diferenciais?
> - (d) Há algum valor atípico? Se for o caso, quais são os escores BRFSS correspondentes a esses valores atípicos?

```python
df = pd.read_excel('FELICIDADE.xls')
df.head()

df.plot(x='CompDif', y='BRFSS', kind='scatter')
plt.show()

df.sort_values('BRFSS', ascending=False).head()
```

**(a)** Diagrama de dispersão: Posto/CompDif no eixo X (variável explicativa), BRFSS no eixo Y (variável resposta).

**(b)** Associação geral **negativa** — conforme o Posto (CompDif) aumenta, o BRFSS diminui.

**(c)** **Discordância.** Posto baixo = estado mais feliz objetivamente; BRFSS baixo/negativo = estado mais feliz subjetivamente. A associação negativa mostra o oposto do que seria concordância: estados rankeados como menos felizes objetivamente (Posto alto) têm BRFSS mais negativo (relatam ser mais felizes subjetivamente). As duas medidas de felicidade não concordam entre si.

**(d)** Sim, há um valor atípico: **Louisiana**, com BRFSS = 0,033 (Posto = 8) — bem mais alto que o esperado para seu Posto, destoando da tendência geral de queda do gráfico.

---

## Questão 10 — Escores SAT Estaduais (arquivo SATMAT.xls)

> O arquivo SATMAT.xls possui informações, para cada estado norte-americano, sobre o percentual de egressos do Ensino Médio que realizam o teste SAT para entrar em uma universidade e o escore médio estadual em matemática.
>
> O percentual de estudantes do ensino médio que fazem o SAT varia de estado para estado. Esse fato ajuda a explicar as diferenças entre os estados relativas à média do escore SAT de matemática?
>
> - (a) Faça uma análise unidimensional de ambas as variáveis com sua distribuição, média, desvio padrão e resumo dos 5 números
> - (b) Faça uma análise bidimensional das variáveis (correlação entre elas), incluindo seu diagrama de dispersão e interpretação respondendo à pergunta levantada no enunciado da questão.

```python
df = pd.read_excel('SATMAT.xls')
df.head()

df['PctSAT'].describe()
df['SAT-Mat'].describe()

df.plot(x='PctSAT', y='SAT-Mat', kind='scatter')
plt.show()

df['PctSAT'].corr(df['SAT-Mat'])
```

**(a)** Análise unidimensional:
- **PctSAT** (% de alunos que fizeram o SAT): média = 39,33%, desvio padrão = 31,12, resumo dos 5 números: mín=3, Q1=8, mediana=32, Q3=68,5, máx=100. Grande variação entre estados; mediana bem menor que a média sugere leve assimetria à direita.
- **SAT-Mat** (média do escore de matemática): média = 538,06, desvio padrão = 39,25, resumo dos 5 números: mín=462, Q1=507, mediana=526, Q3=568, máx=613. Variação bem menor que a do PctSAT; média e mediana próximas, distribuição mais simétrica.

**(b)** Análise bidimensional: diagrama de dispersão (`PctSAT` no eixo X, `SAT-Mat` no eixo Y) mostrou associação **negativa** — conforme mais alunos fazem o SAT num estado, menor tende a ser a média de matemática. Correlação de Pearson: **r = -0,87** (negativa forte).

**Resposta à pergunta do enunciado:** sim, o percentual de estudantes que fazem o SAT ajuda a explicar as diferenças entre os estados na média do escore de matemática — existe uma correlação negativa forte entre as duas variáveis. Isso provavelmente acontece porque, em estados onde poucos alunos fazem a prova, geralmente são só os mais preparados/motivados que se candidatam (puxando a média pra cima); já onde quase todos fazem, a média reflete o desempenho de toda a população estudantil, incluindo alunos mais fracos, o que puxa a média pra baixo.

---

## Questão 11 — Índice de Desenvolvimento da Educação Básica (Ideb)

> O Índice de Desenvolvimento da Educação Básica (Ideb) foi criado em 2007 com a união de dois indicadores: o fluxo escolar e a nota padronizada em testes de desempenho. Tecnicamente, o Ideb é estimado com base em informações secundárias do Censo Escolar, do Sistema de Avaliação da Educação Básica (Saeb) e da Prova Brasil no site do Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira (Inep).
>
> Identifique o valor do Ideb no seu estado e indique a posição que ele ocupa no ranking nacional.

*(Sem código — consulta direta à fonte indicada no próprio enunciado, a [reportagem do Poder360](https://www.poder360.com.br/educacao/conheca-os-estados-com-as-notas-mais-altas-e-mais-baixas-no-ideb/), que traz uma tabela com a nota de cada estado.)*

**Importante:** o Ideb é calculado separadamente por etapa de ensino (anos iniciais, anos finais e ensino médio) — os números abaixo são dos **anos iniciais**, que é a tabela trazida pelo Poder360.

**Resposta (Rio de Janeiro):** Ideb dos anos iniciais em 2023 = **5,7**, com meta de **5,9** para 2030 e avanço de **1,6** ponto desde 2005. Na tabela do ranking (estados ordenados da maior pra menor nota), o RJ aparece na parte de baixo, abaixo da média nacional — entre os estados com desempenho mais fraco, embora não seja o pior do país.

*(Se a prova pedir uma etapa específica diferente — anos finais ou ensino médio — o caminho é o mesmo: voltar na fonte indicada e localizar a coluna/tabela daquela etapa.)*

Fonte: [Poder360](https://www.poder360.com.br/educacao/conheca-os-estados-com-as-notas-mais-altas-e-mais-baixas-no-ideb/)

---

## Questão 6 — Emissão CO2 (arquivo EMISSAOCO2.xls)

> A queima de combustíveis em fábricas ou nos motores dos veículos emite dióxido de carbono (CO2), o que contribui para o aquecimento global.
>
> O arquivo EMISSAOCO2.xls apresenta as emissões anuais de CO2, por pessoa em 2010 em países com populações de, no mínimo, 30 milhões naquele ano.
>
> - (a) Por que você acha que escolhemos medir emissões por pessoa em vez do total de emissões de CO2 para cada país?
> - (b) Faça um histograma a partir desses dados. Descreva a forma, o centro e a dispersão da distribuição.
> - (c) Quais países são valores atípicos?
> - (d) Ache a média e a mediana para esses dados. Quais características da distribuição (descrita no item b) explicam a diferença entre a média e a mediana?

**Roteiro (repete o padrão da Questão 4 — histograma/describe/AIQ):**
- **(a)** Resposta conceitual, sem código: medir por pessoa (per capita) permite **comparar países de tamanhos diferentes** de forma justa — um país populoso naturalmente emite mais no total só por ter mais gente, mesmo que cada pessoa emita pouco. Per capita mostra o impacto individual médio, que é o que de fato queremos comparar entre países.
- **(b)** `df['NOME_COLUNA'].plot(kind='hist', bins=...); plt.show()` → descrever forma (simétrica/assimétrica), centro (média/mediana do `.describe()`) e dispersão (desvio padrão ou AIQ). *(preencher com os números reais depois de rodar)*
- **(c)** Calcular limite superior (e/ou inferior) com a regra 1,5×AIQ e usar `df[(df['NOME_COLUNA'] > limite_superior)]` pra listar os países atípicos. *(preencher)*
- **(d)** `df['NOME_COLUNA'].mean()` e `.median()` — se a distribuição for assimétrica à direita (cauda de países com emissão bem alta), a média fica **maior** que a mediana (os valores extremos puxam a média pra cima, mas não afetam tanto a mediana). *(preencher com os valores reais e confirmar a direção da assimetria)*

---

## Questão 12 — Análise de renda (arquivo InfoFamiliasEntrevistadas.csv)

> Considere os dados do arquivo InfoFamiliasEntrevistadas.csv, correspondente ao resultado de entrevistas realizadas com uma amostra de 120 famílias de uma certa localidade.
>
> Variáveis: Local (localidade da moradia), P.a.p. (uso de programa de alimentação popular: 0-não, 1-sim), Instr. (nível de instrução: 1-nenhum, 2-fundamental, 3-médio), Tam. (nº de pessoas no domicílio), Renda (renda familiar mensal, em salários mínimos).
>
> - (a) Classifique as famílias com renda mensal de até 5 salários mínimos como *renda baixa* e famílias com rendimentos acima de 5 salários mínimos como *renda alta*.
> - (b) A amostra sugere alguma associação entre *renda familiar* e *uso de programas de alimentação popular*? Justifique através da construção e interpretação de uma tabela de dupla entrada.

**Roteiro:**
- **(a)** Novo, mas simples — criar uma coluna nova classificando cada linha:
  ```python
  df['Faixa_Renda'] = df['Renda'].apply(lambda x: 'Renda baixa' if x <= 5 else 'Renda alta')
  ```
  **O que faz:** olha o valor de `Renda` linha por linha; se for ≤ 5, escreve "Renda baixa" numa coluna nova chamada `Faixa_Renda`; senão, escreve "Renda alta".
  **O que trocar:** `'Renda'` → nome da coluna de renda (confirmar no `df.head()`); o valor `5` → o corte que o enunciado pedir.
- **(b)** Repete exatamente o padrão da **Questão 9** (tabela de dupla entrada): `Faixa_Renda` explica o uso do programa, então vai nas linhas; `P.a.p.` vai nas colunas.
  ```python
  tabela = df.pivot_table(index='Faixa_Renda', columns='P.a.p.', values='COLUNA_DE_CONTAGEM_OU_ID')
  percentual = tabela.div(tabela.sum(axis=1), axis=0) * 100
  ```
  *(Atenção: aqui os dados provavelmente vêm um por família, não já contados — pode ser preciso usar `pd.crosstab(df['Faixa_Renda'], df['P.a.p.'])` em vez de `pivot_table`, se não houver uma coluna de contagem pronta. `crosstab` conta automaticamente quantas linhas caem em cada combinação.)* Depois é só comparar o percentual condicional entre "Renda baixa" e "Renda alta" pra ver se o uso do programa varia entre os grupos. *(preencher com os números reais)*

---

## Questão 13 — IDH OECD (arquivo OECD_IDH_data.csv)

> A OECD consiste em países desenvolvidos e industrializados que aceitam os princípios de democracia representativa e uma economia de mercado livre.
>
> O arquivo OECD_IDH_data.csv mostra dados das Nações Unidas para os países da OECD em várias variáveis: PIB per capita (US$), % de desempregados, uma medida de desigualdade (comparação entre os 10% mais ricos e os 10% mais pobres), gasto público em saúde (% do PIB), médicos por 100.000 pessoas, emissão de CO2 per capita (toneladas métricas), % de mulheres no parlamento, e atividade econômica feminina (% da taxa masculina).
>
> - (a) Construa um histograma do PIB.
> - (b) Identifique o valor atípico no histograma.
> - (c) Escolha outras duas variáveis para fazer a análise unidimensional da sua distribuição, interpretando o resultado.
> - (d) Faça uma análise bidimensional das variáveis escolhidas em (c) e interprete essa relação.

**Roteiro:**
- **(a)** Repete o padrão da Questão 4/6: `df['PIB'].plot(kind='hist'); plt.show()`.
- **(b)** Calcular a regra 1,5×AIQ pra confirmar visualmente qual país é atípico (o de PIB bem mais alto que o resto). *(preencher)*
- **(c)** Escolher livremente 2 variáveis quantitativas da lista (ex: gasto público em saúde e médicos por 100k) e repetir o `.describe()` + histograma de cada uma, como já feito em outras questões.
- **(d)** Repete exatamente o padrão da Questão 10 (correlação de Pearson): diagrama de dispersão das 2 variáveis escolhidas + `.corr()` entre elas, e interpretar a força/direção. *(preencher com os valores reais depois de escolher as variáveis e rodar)*

---

## Questão 14 — Censo Demográfico dos Estados Brasileiros em 2000 (arquivo Censo_estados.xlsx)

> O arquivo Censo_estados.xlsx possui informações sobre o Censo Demográfico de 2000, contendo indicadores sociais dos estados brasileiros.
>
> Realize análises bivariadas e interprete-as, para cada par de variáveis.

**Roteiro:** questão mais aberta — não tem uma única resposta certa. Pra cada par de variáveis do arquivo:
1. Ver o tipo de cada variável do par (`df.dtypes` ou olhar os valores no `df.head()`).
2. Se as **2 forem quantitativas** → diagrama de dispersão + correlação de Pearson (padrão da Questão 10).
3. Se as **2 forem qualitativas** → tabela de dupla entrada com percentual condicional (padrão da Questão 9).
4. Se for **1 quantitativa + 1 qualitativa** → boxplot lado a lado, comparando a variável quantitativa entre as categorias da qualitativa (padrão da Questão 7).
5. Em cada par, sempre fechar com uma frase de interpretação: qual a direção/força da associação (ou se não há associação nenhuma).

*(Fazer por último, com calma — usar o "Códigos Prontos" pra escolher a ferramenta certa conforme o tipo de cada par de variáveis.)*

