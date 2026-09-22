[simulado.md](https://github.com/user-attachments/files/32540874/simulado.md)
# Simulado Festival ViraBairro — enunciado e resolução

22/09/2026

Enunciado das 8 questões e a resolução comentada do monitor. Os números são os da plataforma, mas na prova use só o que aparecer na **sua** tela. Tente fazer cada questão antes de abrir a resolução.

## O caso e os arquivos

O Observatório Conexão Bairro (OCB), organização fictícia, coordena a comunicação do Festival ViraBairro: atividades gratuitas de cultura, mobilidade, saúde e trabalho. Em oito semanas a equipe publicou convites, serviços e guias em formatos diferentes, e registrou o que já sabia antes de publicar (horário, legenda, perfil) e os resultados depois. Faltam duas semanas pro festival e é preciso decidir onde gastar os poucos espaços de divulgação. Todos os dados são sintéticos.

**Regras:** cada questão recarrega o arquivo numa variável nova. Não instale nada. Proibido usar IA. Consulta só a GitHub, noai.duckduckgo.com, documentação oficial (pandas, NumPy, Matplotlib, Altair, scikit-learn), Stack Overflow e YouTube.

| Arquivo | Linhas | Colunas | Usado em |
| --- | --- | --- | --- |
| `dados/publicacoes_brutas.csv` (com problemas de propósito) | 36 | 12 | Q1, Q2 |
| `dados/publicacoes_analise.csv` (já tratada) | 120 | 18 | Q3 a Q8 |

**Bruta:** `id_publicacao`, `data_publicacao`, `tema`, `formato`, `alcance`, `curtidas`, `comentarios`, `compartilhamentos`, `salvamentos`, `seguidores_autor`, `videos_autor`, `duracao_segundos`. **Análise** tem essas e mais `tamanho_legenda`, `n_emojis`, `n_hashtags`, `hora`, `dia_semana` e `taxa_engajamento_pct`. Temas: cultura, mobilidade, saude, trabalho. Formatos: reel, carrossel, imagem (só três, então o `get_dummies` dá 15 colunas).

| Questão | O que cobra | Aula |
| --- | --- | --- |
| 1 | Olhar a base | 5, 10 |
| 2 | Limpeza | **10** |
| 3 | Agrupar + barras | 5, 6 |
| 4 | Tempo + filtro + ranking | 5, 6, 10 |
| 5 | Agrupar por duas variáveis | 5, 6 |
| 6 | Árvore + importâncias | 12 |
| 7 | Regressão | 11 |
| 8 | Classificação + corte | 12 |

**A lição do simulado:** as diferenças entre categorias são minúsculas e os grupos têm poucos casos. A resposta que ganha nota percebe o empate, diz isso e ainda entrega uma decisão. Antes de escrever, pergunte ao número: **quantos casos tem por trás dele?** E **qual a distância pro segundo colocado?**

## Questão 1: diagnóstico inicial da base

### Enunciado

A equipe recebeu uma base sem documentação. Em uma célula de código, carregue `dados/publicacoes_brutas.csv` e mostre: (1) as cinco primeiras linhas; (2) a quantidade de linhas e colunas; (3) a quantidade de valores ausentes por coluna, **mostrando somente as colunas que têm ao menos uma ausência**. Na Markdown, explique em até duas frases uma limitação que impeça tratar esses resultados como retrato de todas as redes, públicos ou bairros.

### Armadilha

"Somente as colunas com ausência": `isna().sum()` puro mostra também as de zero. Guarde numa variável e filtre por ela mesma.

### Código

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

q1 = pd.read_csv("dados/publicacoes_brutas.csv")
linhas, colunas = q1.shape
print(f"A base tem {linhas} linhas e {colunas} colunas.")
ausentes = q1.isna().sum()
print(ausentes[ausentes > 0])
q1.head()
```

### Resultado

36 linhas e 12 colunas. Ausentes: `alcance` 1, `comentarios` 1, `salvamentos` 1.

### Resposta

> A base traz apenas 36 registros de uma única organização fictícia, referentes a uma campanha específica, e não tem nenhuma coluna que identifique a rede social, o público ou o bairro alcançado por cada publicação. Com esse tamanho e sem essas informações, os resultados descrevem só este conjunto de publicações e não podem ser lidos como retrato de todas as redes, públicos ou bairros do festival.

Dá ponto porque aponta limitações que se enxergam na própria base (36 registros, sem coluna de rede ou bairro), não uma limitação genérica.

## Questão 2: tratamento dos registros

Foco da monitoria. É a questão mais longa e a nota vem tanto do código quanto das 4 frases de justificativa.

### Enunciado

A base tem nomes de temas escritos de formas diferentes, datas em formatos distintos, um registro duplicado e alguns valores ausentes. Prepare os dados sem criar informação que não esteja nos arquivos. Parta novamente de `dados/publicacoes_brutas.csv`, **em uma nova variável**, e faça o tratamento para:

1. remover duplicidade por `id_publicacao`;
2. padronizar os valores de `tema` para uma forma consistente;
3. converter `data_publicacao` e as colunas numéricas usadas no cálculo para tipos adequados;
4. tratar ausências ou valores inválidos de maneira justificada; e
5. criar `taxa_utilidade_pct` = (compartilhamentos + salvamentos) / alcance × 100.

Depois, produza uma tabela por tema com o número de publicações e a **mediana** de `taxa_utilidade_pct`, ordenada da maior para a menor. Não precisa salvar arquivo. Na Markdown, registre as decisões de limpeza em **até quatro frases**; se descartar, preencher ou converter algo, diga por quê.

### Os quatro defeitos plantados na base

| Defeito | Onde |
| --- | --- |
| 1 duplicidade por id | `OCB-018` aparece 2 vezes, igual nas 12 colunas |
| grafias fora do padrão em `tema` | `Cultura` maiúsculo e `Saúde` com acento: depois de `strip` + `lower` sobram 5 valores pra 4 temas |
| 3 formatos de data | `2026-08-01 12:00` (ISO), `05/08/2026 18:00` (brasileiro) e uma vez `2026/08/04 09:00` (ISO com barra, no `OCB-032`) |
| 3 ausências, uma por coluna | `alcance` (`OCB-021`), `comentarios` (`OCB-025`), `salvamentos` (`OCB-029`) |

A base **não** tem: linha sem tema, alcance zero, contagem negativa, data impossível, nem coluna numérica chegando como texto (elas são `float64` só porque têm ausência). Não diga na resposta que tratou isso.

### As cinco armadilhas

1. **Duplicidade por id, não por linha.** `drop_duplicates()` sem argumento só tira linhas iguais em todas as colunas. Use `subset="id_publicacao"` e olhe as cópias **antes** com `duplicated(..., keep=False)`.
2. **`lower` não une acento.** Rode `value_counts` primeiro: `saude` 11 ao lado de `saúde` 1 é erro de digitação. Resolva com dicionário `{"saúde": "saude"}`.
3. **Data sem `format` morre em silêncio.** O pandas deduz o formato pela primeira linha e transforma em `NaT` o `2026/08/04` do `OCB-032`. Com `format="ISO8601"` a contagem de `NaT` é zero.
4. **`dayfirst=True` na coluna toda troca dia e mês.** Nesta base, 16 datas trocadas e 18 destruídas de 35, sem nenhum erro vermelho. Só afeta datas ISO com dia ≤ 12, então conferir 2 ou 3 linhas não adianta: confira `.min()` e `.max()`.
5. **Mediana, não média.** No `agg` é `"median"`.

### Código

```python
q2 = pd.read_csv("dados/publicacoes_brutas.csv")
print(f"Linhas no bruto: {len(q2)}")

# 1. duplicidade: olhar as cópias ANTES de remover
repetidos = q2.loc[q2.duplicated(subset="id_publicacao", keep=False), "id_publicacao"].unique()
for pid in repetidos:
    bloco = q2[q2["id_publicacao"] == pid]
    divergentes = [c for c in bloco.columns if bloco[c].nunique(dropna=False) > 1]
    print(f"{pid}: aparece {len(bloco)}x | colunas que divergem: {divergentes}")
duplicadas = q2.duplicated(subset="id_publicacao").sum()
q2 = q2.drop_duplicates(subset="id_publicacao", keep="first")
print(f"Duplicadas removidas: {duplicadas} -> restam {len(q2)}")

# 2. tema
q2["tema"] = q2["tema"].str.strip().str.lower()
print(q2["tema"].value_counts(dropna=False))
q2["tema"] = q2["tema"].replace({"saúde": "saude"})
print("Temas:", sorted(q2["tema"].dropna().unique()))

# 3. data em duas passadas
texto_data = q2["data_publicacao"].copy()
comeca_com_ano = q2["data_publicacao"].str[:4].str.isdigit().fillna(False)
datas = pd.to_datetime(q2["data_publicacao"].where(comeca_com_ano), format="ISO8601", errors="coerce")
resto = pd.to_datetime(q2["data_publicacao"].where(~comeca_com_ano), format="mixed", dayfirst=True, errors="coerce")
q2["data_publicacao"] = datas.fillna(resto)
print("Período:", q2["data_publicacao"].min().strftime("%d/%m/%Y"), "a", q2["data_publicacao"].max().strftime("%d/%m/%Y"))
print("NaT:", q2["data_publicacao"].isna().sum())

# prova de que as duas passadas eram necessárias
ingenuo = pd.to_datetime(texto_data, dayfirst=True, errors="coerce")
trocou = (q2["data_publicacao"] != ingenuo) & q2["data_publicacao"].notna() & ingenuo.notna()
sumiu = q2["data_publicacao"].notna() & ingenuo.isna()
print(f"dayfirst em tudo: {trocou.sum()} trocadas, {sumiu.sum()} viraram NaT")

# 4. números: olhar dtype antes
print(q2[["alcance", "compartilhamentos", "salvamentos"]].dtypes)
for coluna in ["compartilhamentos", "salvamentos", "alcance"]:
    q2[coluna] = pd.to_numeric(q2[coluna], errors="coerce")

# 5. ausências e inválidos, contando cada filtro
antes = len(q2)
q2 = q2.dropna(subset=["tema"]);                                        print("sem tema:", antes - len(q2))
parcial = len(q2); q2 = q2.dropna(subset=["alcance", "compartilhamentos", "salvamentos"]); print("sem campo da taxa:", parcial - len(q2))
parcial = len(q2); q2 = q2[q2["alcance"] > 0];                          print("alcance zero:", parcial - len(q2))
parcial = len(q2); q2 = q2[(q2["compartilhamentos"] >= 0) & (q2["salvamentos"] >= 0)]; print("negativos:", parcial - len(q2))
print(f"Descartadas: {antes - len(q2)} -> restam {len(q2)}")

# 6. taxa e tabela
q2["taxa_utilidade_pct"] = (q2["compartilhamentos"] + q2["salvamentos"]) / q2["alcance"] * 100
resumo_q2 = (q2.groupby("tema")
               .agg(publicacoes=("id_publicacao", "count"),
                    mediana_utilidade_pct=("taxa_utilidade_pct", "median"))
               .reset_index().sort_values("mediana_utilidade_pct", ascending=False).round(2))
resumo_q2
```

### Resultado

36 linhas → 1 duplicidade removida (35) → 2 descartadas (33): `OCB-021` sem alcance e `OCB-029` sem salvamentos. `OCB-025` (sem comentário) **fica**, porque comentário não entra na fórmula. Período 01/08/2026 a 28/08/2026, zero `NaT`.

| tema | publicações | mediana da taxa de utilidade (%) |
| --- | --- | --- |
| saude | 11 | 1,18 |
| cultura | 7 | 1,14 |
| mobilidade | 8 | 1,13 |
| trabalho | 7 | 0,86 |

| Conferência | Resultado | O que escrever |
| --- | --- | --- |
| cópias do id repetido | idênticas nas 12 colunas | o `subset` é defensivo |
| `value_counts` do tema | 5 grafias pra 4 temas | a equivalência era necessária |
| `NaT` depois da conversão | 0 | a base não tem data impossível |
| `dayfirst` sem `format` | 16 trocadas, 18 destruídas | as duas passadas não são exagero |
| dtypes antes do `to_numeric` | `float64` e `int64` | as colunas **não** chegaram como texto |
| filtros de tema, alcance zero, negativos | 0 linhas cada | **não** cite como tratamento feito |

### Resposta

> Removi uma duplicidade por `id_publicacao`, mantendo a primeira ocorrência, e conferi antes que as duas cópias de `OCB-018` eram idênticas em todas as colunas, o que torna a remoção segura; usei `subset` mesmo assim porque um `drop_duplicates()` sem ele deixaria a repetição passar caso houvesse qualquer divergência. Rodei `value_counts` em `tema` antes de decidir qualquer coisa e encontrei cinco grafias para quatro categorias, então apliquei `strip` e `lower` e, como isso não une `saude` e `saúde`, acrescentei uma tabela de equivalência manual para as duas contarem como um tema só. Converti `data_publicacao` em duas passadas, com `format="ISO8601"` nas linhas de ano à frente e `dayfirst=True` no restante, porque a coluna mistura três formatos e um `dayfirst=True` aplicado a tudo sem `format` trocaria dia por mês em 16 datas e destruiria outras 18, sem gerar erro; conferi pelo intervalo, que ficou entre 01/08/2026 e 28/08/2026, sem nenhuma data perdida. Conferi os dtypes de `alcance`, `compartilhamentos` e `salvamentos` e os três já chegaram numéricos, então mantive o `pd.to_numeric` com `errors="coerce"` apenas como salvaguarda, e descartei as duas únicas linhas problemáticas, `OCB-021` sem `alcance` e `OCB-029` sem `salvamentos`, já que sem esses campos a taxa não existe e preencher seria inventar dado.

O professor quer **uma decisão explícita com motivo** pra cada problema, sempre na forma "fiz X porque Y". "Limpei os dados e tratei os ausentes" não dá ponto. E não descreva tratamento que não aconteceu: ele tem a base na mão.

## Questão 3: escolha de tema para divulgação

### Enunciado

A equipe trabalha com quatro temas e só consegue dar destaque principal a um. A escolha deve priorizar conteúdo que as pessoas tendem a **salvar ou compartilhar**. Use **somente** `dados/publicacoes_analise.csv`. Crie `taxa_utilidade_pct` com a mesma fórmula da Q2. Depois: (1) monte uma tabela com a mediana da taxa por tema; (2) faça um gráfico de barras comparando os quatro temas, com título que comunique a pergunta, eixos nomeados e "Fonte: dados sintéticos do Festival ViraBairro (2026)" no próprio gráfico. Na Markdown, uma recomendação de **3 a 5 frases**: indique um tema, explique o que a mediana representa e apresente uma limitação. Não afirme causalidade.

### Armadilhas

**Utilidade não é engajamento:** a fórmula só usa compartilhamento e salvamento. E **olhe a altura das barras antes de recomendar**: se estiverem praticamente iguais, apontar a mais alta é resposta fraca.

### Código

```python
q3 = pd.read_csv("dados/publicacoes_analise.csv")
q3["taxa_utilidade_pct"] = (q3["compartilhamentos"] + q3["salvamentos"]) / q3["alcance"] * 100
tabela_q3 = (q3.groupby("tema")
               .agg(publicacoes=("id_publicacao", "count"),
                    mediana_utilidade_pct=("taxa_utilidade_pct", "median"))
               .reset_index().sort_values("mediana_utilidade_pct", ascending=False).round(2))
print(tabela_q3.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tabela_q3["tema"], tabela_q3["mediana_utilidade_pct"], color="#3b6ea5")
ax.set_title("Qual tema as pessoas mais salvam e compartilham?")
ax.set_xlabel("Tema da publicação")
ax.set_ylabel("Mediana da taxa de utilidade (%)")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

### Resultado

| tema | publicações | mediana (%) |
| --- | --- | --- |
| mobilidade | 33 | 1,15 |
| cultura | 26 | 1,13 |
| saude | 35 | 1,10 |
| trabalho | 26 | 0,96 |

As três primeiras barras são praticamente iguais (0,05 ponto entre mobilidade e saúde). A única separação segura é que **trabalho fica atrás**. Repare: na Q2, com a base bruta, quem liderava era saúde. Bases diferentes, vencedores diferentes, porque as diferenças são pequenas.

### Resposta

> Entre os quatro temas, mobilidade tem a maior mediana de taxa de utilidade, com 1,15%, seguida de perto por cultura, com 1,13%, e saúde, com 1,10%, enquanto trabalho fica isolado abaixo, com 0,96%. A mediana é o valor do meio da distribuição, metade das publicações do tema acima e metade abaixo, o que a torna menos sensível do que a média a uma peça isolada de desempenho atípico. A leitura honesta desses números é que os três primeiros temas estão praticamente empatados: a diferença entre mobilidade e saúde é de apenas 0,05 ponto percentual, calculada sobre 26 a 35 publicações por tema, o que é pequeno demais para sustentar uma escolha. O que os dados permitem afirmar com alguma segurança é que trabalho é o tema que menos gera salvamento e compartilhamento, e por isso a decisão defensável é descartar trabalho e escolher entre os outros três por critério editorial, não por esta métrica. Como limitação, os temas não foram publicados nos mesmos formatos nem nos mesmos horários, então a diferença entre eles pode estar refletindo essas outras escolhas da equipe, e em qualquer caso isto é associação observada, não evidência de que o tema cause mais compartilhamento.

## Questão 4: acompanhamento diário

### Enunciado

Use **somente** `dados/publicacoes_analise.csv`, em uma nova variável. (1) Converta `data_publicacao` para data/hora e crie `dia_publicacao`, só com a data. (2) Crie uma tabela por `dia_publicacao` com a quantidade de publicações, a média de `taxa_engajamento_pct` e o alcance total, em ordem cronológica. (3) Faça um gráfico de linhas da taxa média por dia, com título, eixos nomeados e a fonte no gráfico. (4) Crie um recorte só de `reel` publicados a partir das 18h e mostre as cinco com maior `taxa_engajamento_pct`, com `id_publicacao`, `dia_publicacao`, `hora`, `tema` e `taxa_engajamento_pct`. Na resposta, descreva a variação diária **sem afirmar tendência de longo prazo** e explique por que o recorte de reels noturnos não prova que horário ou formato causam engajamento.

### Armadilhas

Filtro com duas condições: parênteses em cada uma e `&`, nunca `and`. Três agregações no mesmo `agg`: `count`, `mean`, `sum`.

### Código

```python
q4 = pd.read_csv("dados/publicacoes_analise.csv")
q4["data_publicacao"] = pd.to_datetime(q4["data_publicacao"])
q4["dia_publicacao"] = q4["data_publicacao"].dt.date

tabela_diaria = (q4.groupby("dia_publicacao")
                   .agg(publicacoes=("id_publicacao", "count"),
                        media_engajamento_pct=("taxa_engajamento_pct", "mean"),
                        alcance_total=("alcance", "sum"))
                   .reset_index().sort_values("dia_publicacao").round(2))
print(f"Dias com publicação: {len(tabela_diaria)}")

fig, ax = plt.subplots(figsize=(11, 4.5))
ax.plot(tabela_diaria["dia_publicacao"], tabela_diaria["media_engajamento_pct"], marker="o", markersize=3, color="#3b6ea5")
ax.set_title("Como a taxa média de engajamento variou dia a dia na campanha")
ax.set_xlabel("Dia da publicação")
ax.set_ylabel("Taxa média de engajamento (%)")
ax.tick_params(axis="x", rotation=45)
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()

reels_noturnos = q4[(q4["formato"] == "reel") & (q4["hora"] >= 18)]
print(f"Reels a partir das 18h: {len(reels_noturnos)}")
top5_reels = reels_noturnos.nlargest(5, "taxa_engajamento_pct")[
    ["id_publicacao", "dia_publicacao", "hora", "tema", "taxa_engajamento_pct"]]
top5_reels
```

### Resultado

56 dias (01/08 a 28/09/2026), 120 publicações: cerca de 2 por dia. 21 reels a partir das 18h.

| id | dia | hora | tema | taxa (%) |
| --- | --- | --- | --- | --- |
| OCB-003 | 2026-08-03 | 22 | cultura | 6,82 |
| OCB-107 | 2026-09-23 | 18 | mobilidade | 6,80 |
| OCB-087 | 2026-09-03 | 22 | cultura | 6,15 |
| OCB-097 | 2026-09-13 | 20 | mobilidade | 6,08 |
| OCB-027 | 2026-08-27 | 20 | mobilidade | 5,64 |

Média de 2 ou 3 publicações não é medida estável do dia: o serrilhado do gráfico é em boa parte aritmética de amostra pequena.

### Resposta

> A taxa média de engajamento oscila de um dia para o outro ao longo de quase dois meses de campanha, alternando picos e quedas sem uma direção estável de subida ou descida. Boa parte dessa oscilação é aritmética e não comportamento do público: a base tem 120 publicações distribuídas em 56 dias, ou seja, duas a três por dia, e com esse tamanho uma única peça acima ou abaixo do padrão desloca a média do dia inteiro. Por isso o gráfico não autoriza nenhuma afirmação sobre tendência de longo prazo, apenas sobre variação diária. O recorte dos cinco reels noturnos com maior taxa também não prova que horário ou formato causem engajamento, porque ele seleciona as cinco melhores de um grupo de apenas 21 publicações que já havia sido filtrado justamente por formato e horário: os casos foram escolhidos pelo resultado que se quer explicar. Para sustentar que reel noturno funciona seria preciso comparar reels noturnos com reels publicados em outros horários e com outros formatos no mesmo horário, mantendo o resto parecido, e essa comparação não foi feita.

## Questão 5: tema e formato das publicações

### Enunciado

A equipe quer entender como **tema** e **formato** aparecem juntos; analisar cada variável separadamente pode ocultar diferenças. Use **somente** `dados/publicacoes_analise.csv`. Crie uma tabela com uma linha por combinação de `tema` e `formato`, com (1) número de publicações e (2) mediana de `taxa_engajamento_pct`, ordenada da maior para a menor mediana. Faça um gráfico de barras comparando as combinações, com título informativo, eixos nomeados e a fonte no gráfico. Na Markdown, **4 a 6 frases**: destaque uma combinação que mereça ser testada, explique por que comparar duas variáveis é diferente de analisar uma e registre uma limitação.

### Armadilhas

`groupby` com **lista** de duas colunas. São 12 combinações: use barra horizontal (`barh`) ou gire os rótulos. A coluna de contagem diz em qual linha confiar.

### Código

```python
q5 = pd.read_csv("dados/publicacoes_analise.csv")
tabela_q5 = (q5.groupby(["tema", "formato"])
               .agg(publicacoes=("id_publicacao", "count"),
                    mediana_engajamento_pct=("taxa_engajamento_pct", "median"))
               .reset_index().sort_values("mediana_engajamento_pct", ascending=False).round(2))
print(tabela_q5.to_string(index=False))

tabela_q5["combinacao"] = tabela_q5["tema"] + " / " + tabela_q5["formato"]
fig, ax = plt.subplots(figsize=(9, 7))
ax.barh(tabela_q5["combinacao"][::-1], tabela_q5["mediana_engajamento_pct"][::-1], color="#3b6ea5")
ax.set_title("Quais combinações de tema e formato engajam mais?")
ax.set_xlabel("Mediana da taxa de engajamento (%)")
ax.set_ylabel("Tema / formato")
fig.text(0.01, -0.02, "Fonte: dados sintéticos do Festival ViraBairro (2026)", fontsize=8, color="gray")
fig.tight_layout()
plt.show()
```

### Resultado

| tema | formato | publicações | mediana (%) |
| --- | --- | --- | --- |
| mobilidade | reel | 11 | 5,10 |
| cultura | reel | 8 | 4,82 |
| saude | reel | 12 | 4,67 |
| cultura | carrossel | 10 | 4,54 |
| mobilidade | carrossel | 10 | 4,53 |
| cultura | imagem | 8 | 4,39 |
| saude | carrossel | 11 | 4,29 |
| trabalho | reel | 8 | 4,27 |
| trabalho | carrossel | 10 | 3,73 |
| mobilidade | imagem | 12 | 3,60 |
| saude | imagem | 12 | 3,38 |
| trabalho | imagem | 8 | 3,04 |

O achado real aparece quando você reagrupa por tema: **em todos os quatro temas a ordem é reel > carrossel > imagem**. E o tema que lidera muda com o formato: mobilidade entre os reels, cultura entre carrosséis e imagens.

### Resposta

> A combinação de mobilidade em reel aparece no topo da tabela, com mediana de 5,10%, e é a candidata natural a ser testada, com a ressalva de que ela está a 0,28 ponto de cultura em reel e a 0,43 de saúde em reel, diferenças pequenas para combinações que têm entre 8 e 12 publicações cada. O cruzamento revela um padrão que a análise de uma variável isolada esconderia: dentro de cada um dos quatro temas, sem exceção, a ordem é reel, depois carrossel, depois imagem, o que indica que o formato ordena o resultado de forma bem mais consistente do que o tema. Ao mesmo tempo, o tema que lidera muda conforme o formato, já que mobilidade é o primeiro entre os reels enquanto cultura é o primeiro entre carrosséis e imagens. É por isso que comparar duas variáveis juntas é diferente de analisar cada uma isoladamente: olhando só o tema, a vantagem de mobilidade poderia vir apenas de ela concentrar mais reels, e olhando só o formato, perderíamos essa inversão de liderança entre os temas. Como limitação, nenhuma célula da tabela passa de 12 publicações, e uma mediana calculada sobre esse número é instável o bastante para trocar de posição no ranking por causa de uma única peça atípica. Pelo que a base sustenta, a recomendação mais segura é priorizar reel como formato, decisão que se repete em todos os temas, e tratar a escolha do tema como decisão editorial.

## Questão 6: variáveis mais usadas pela árvore

### Enunciado

Use **somente** `dados/publicacoes_analise.csv`, de modo independente. (1) Crie `mereceu_divulgacao_adicional` pelo percentil 75 de `taxa_engajamento_pct`. (2) Use apenas as características disponíveis antes da publicação listadas na Q8 e transforme categorias em números. (3) Reserve 75% para treino e 25% para teste, com `random_state=42` e preservando a proporção do alvo. Ajuste uma árvore de classificação com profundidade máxima 4, `random_state=42` e pesos balanceados. (4) Produza uma tabela ordenada e um gráfico de barras **horizontal** com as cinco características de maior importância, com título e eixos nomeados. Na resposta, explique por que importância alta não prova causalidade e descreva uma mudança na base que poderia alterar o ranking.

### Traduzindo o enunciado

| Enunciado | Código |
| --- | --- |
| percentil 75 | `.quantile(0.75)` |
| 75% treino, 25% teste | `test_size=0.25` |
| preservando a proporção do alvo | `stratify=y` |
| profundidade máxima 4 | `max_depth=4` |
| pesos balanceados | `class_weight="balanced"` |
| barras horizontal | `ax.barh(...)` |

**Armadilha nº 1 da prova:** `tema` e `formato` são texto, então sem `pd.get_dummies` dá `could not convert string to float`. **Armadilha nº 2:** vazamento. Alcance, interações e a própria taxa só existem depois de publicar, e `id_publicacao` é só um código.

### Código

```python
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error, r2_score, precision_score, recall_score, f1_score, confusion_matrix

q6 = pd.read_csv("dados/publicacoes_analise.csv")
corte_p75 = q6["taxa_engajamento_pct"].quantile(0.75)
q6["mereceu_divulgacao_adicional"] = (q6["taxa_engajamento_pct"] > corte_p75).astype(int)

CARACTERISTICAS = ["tema", "formato", "seguidores_autor", "videos_autor", "tamanho_legenda",
                   "n_emojis", "n_hashtags", "hora", "dia_semana", "duracao_segundos"]
X = pd.get_dummies(q6[CARACTERISTICAS], columns=["tema", "formato"])
y = q6["mereceu_divulgacao_adicional"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

arvore_q6 = DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced")
arvore_q6.fit(X_treino, y_treino)
importancias = (pd.DataFrame({"caracteristica": X.columns, "importancia": arvore_q6.feature_importances_})
                  .sort_values("importancia", ascending=False).reset_index(drop=True))
top5_importancias = importancias.head(5)
print(top5_importancias.to_string(index=False))

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.barh(top5_importancias["caracteristica"][::-1], top5_importancias["importancia"][::-1], color="#3b6ea5")
ax.set_title("O que a árvore mais usou para separar as publicações de destaque")
ax.set_xlabel("Importância na árvore (0 a 1)")
ax.set_ylabel("Característica")
fig.tight_layout()
plt.show()
```

### Resultado

Corte 4,89%: 30 de 120 marcadas com 1 (25%). `X` com 15 colunas. Treino 90 (23 positivas), teste 30.

| característica | importância |
| --- | --- |
| formato\_reel | 0,276 |
| dia\_semana | 0,139 |
| n\_hashtags | 0,139 |
| tema\_cultura | 0,100 |
| videos\_autor | 0,095 |

`formato_reel` no topo bate com a Q5. `dia_semana` e `n_hashtags` empatam: com esse tamanho, trocar o `random_state` provavelmente inverteria os dois.

### Resposta

> A árvore usou principalmente `formato_reel`, com importância 0,28, seguido de `dia_semana` e `n_hashtags`, empatados em 0,14, depois `tema_cultura` com 0,10 e `videos_autor` com 0,09. Importância alta significa apenas que a característica foi útil para dividir os dados que a árvore viu no treino, não que ela cause o desempenho: `formato_reel` pode estar no topo porque os reels desta campanha concentram determinados temas, horários e durações, e a árvore aproveita essa associação sem conseguir separar o que vem de quê. A limitação decisiva aqui é o tamanho da base: a árvore foi treinada com 90 publicações, das quais apenas 23 pertencem à classe positiva, e com esse número o ranking é instável. Uma mudança pequena já o alteraria: trocar o `random_state` do `train_test_split`, acrescentar uma dezena de publicações, ou passar a distribuir formatos e horários de maneira mais equilibrada faria `dia_semana` e `n_hashtags`, que hoje empatam na segunda casa decimal, trocarem de posição sem que nada tenha mudado no fenômeno real.

## Questão 7: estimativa de engajamento

### Enunciado

A equipe precisa estimar, antes da publicação, a `taxa_engajamento_pct` esperada de uma nova peça. Use **somente** `dados/publicacoes_analise.csv`. (1) Na resposta, indique o tipo de aprendizado adequado (regressão, classificação ou clusterização) e explique por que o alvo exige essa escolha. (2) Use como características somente `tema`, `formato`, `seguidores_autor`, `videos_autor`, `tamanho_legenda`, `n_emojis`, `n_hashtags`, `hora`, `dia_semana` e `duracao_segundos`, transformando categorias em números. Não use identificador, alcance, interações nem variáveis calculadas a partir da taxa. (3) 75% treino e 25% teste, `random_state=42`. (4) Ajuste uma regressão linear e uma árvore de regressão com profundidade máxima 4 e compare numa tabela de MAE e R². (5) Para o modelo com menor MAE, faça um gráfico de dispersão entre valores reais e previstos, com uma linha de referência onde previsão e valor real seriam iguais, título e eixos nomeados. Na resposta, explique o que o MAE mede, indique o modelo escolhido e registre uma limitação que impeça interpretar a previsão como causal.

### Armadilhas

Alvo é número contínuo, então **regressão**. Aqui **não** tem `stratify`: copiar o split da Q6 quebra. O modelo bobo (média do treino) não foi pedido, mas custa duas linhas e dá a referência.

### Código

```python
q7 = pd.read_csv("dados/publicacoes_analise.csv")
X = pd.get_dummies(q7[CARACTERISTICAS], columns=["tema", "formato"])
y = q7["taxa_engajamento_pct"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42)   # sem stratify

modelo_linear = LinearRegression().fit(X_treino, y_treino)
previsao_linear = modelo_linear.predict(X_teste)
modelo_arvore = DecisionTreeRegressor(max_depth=4, random_state=42).fit(X_treino, y_treino)
previsao_arvore = modelo_arvore.predict(X_teste)
previsao_boba = np.full(len(y_teste), y_treino.mean())

comparacao_q7 = pd.DataFrame({
    "modelo": ["modelo bobo (média)", "regressão linear", "árvore de regressão (prof. 4)"],
    "MAE": [mean_absolute_error(y_teste, p) for p in (previsao_boba, previsao_linear, previsao_arvore)],
    "R2":  [r2_score(y_teste, p) for p in (previsao_boba, previsao_linear, previsao_arvore)],
}).round(3)
print(comparacao_q7.to_string(index=False))

if mean_absolute_error(y_teste, previsao_linear) <= mean_absolute_error(y_teste, previsao_arvore):
    previsao_escolhida, nome_escolhido = previsao_linear, "regressão linear"
else:
    previsao_escolhida, nome_escolhido = previsao_arvore, "árvore de regressão"

fig, ax = plt.subplots(figsize=(6.5, 6))
ax.scatter(y_teste, previsao_escolhida, alpha=0.5, s=22, color="#3b6ea5")
minimo = float(min(y_teste.min(), previsao_escolhida.min()))
maximo = float(max(y_teste.max(), previsao_escolhida.max()))
ax.plot([minimo, maximo], [minimo, maximo], color="#c0392b", linestyle="--", label="previsão = valor real")
ax.set_title(f"Valor real x valor previsto ({nome_escolhido})")
ax.set_xlabel("Taxa de engajamento real (%)")
ax.set_ylabel("Taxa de engajamento prevista (%)")
ax.legend()
fig.tight_layout()
plt.show()
```

### Resultado

| modelo | MAE | R² |
| --- | --- | --- |
| modelo bobo (média) | 0,603 | -0,025 |
| **regressão linear** | **0,349** | **0,644** |
| árvore de regressão (prof. 4) | 0,516 | 0,129 |

A linear ganhou com folga (erro 42% menor que o chute da média). A árvore mal supera o bobo: com 90 publicações de treino ela não tem volume pra aproveitar a flexibilidade. Na aula 11 foi o contrário: nenhum modelo é sempre melhor.

### Resposta

> O tipo de aprendizado adequado é a regressão, porque a variável-alvo, `taxa_engajamento_pct`, é um número contínuo e a equipe quer estimar o valor esperado dessa taxa, não classificá-la numa categoria. A classificação responderia a uma pergunta diferente, do tipo "esta peça vai ou não passar de determinado patamar", e ainda exigiria um corte arbitrário; a clusterização não se aplica porque não há alvo a prever, já que ela apenas agrupa registros por semelhança sem usar resposta conhecida. O MAE mede o erro absoluto médio na mesma unidade do alvo: o MAE de 0,349 da regressão linear significa que, em média, a previsão erra a taxa de engajamento em cerca de 0,35 ponto percentual, para cima ou para baixo. Escolhi a regressão linear, que teve o menor MAE, 0,349 contra 0,516 da árvore, e o maior R², 0,644 contra 0,129; comparadas ao modelo que sempre chuta a média do treino, com MAE 0,603, a linear reduz o erro em cerca de 42% enquanto a árvore fica bem perto do chute, o que sugere que 90 publicações de treino são poucas para uma árvore aproveitar sua flexibilidade. Como limitação, o modelo descreve associações observadas nesta campanha específica e não relações causais: as características não foram distribuídas de forma controlada entre as publicações, então alterar uma delas numa nova peça não garante o efeito que o modelo estima.

O erro mais comum é explicar o MAE só em abstrato. O que dá ponto é traduzir o número: errar 0,349 é errar cerca de um terço de ponto percentual na taxa.

## Questão 8: priorização de divulgação

### Enunciado

Nos dias finais, a equipe só consegue dar divulgação adicional a poucas publicações. Pergunta: quais peças têm maior chance de receber a classificação "merece divulgação adicional"? Use **somente** `dados/publicacoes_analise.csv`. Crie `mereceu_divulgacao_adicional`: 1 quando `taxa_engajamento_pct` estiver acima do percentil 75, 0 nos demais.

1. Na Markdown, diga qual tipo de aprendizado é adequado e explique brevemente por que os outros dois não respondem a essa decisão.
2. Use apenas as características de antes da publicação (as mesmas da Q7), transformando categorias em colunas numéricas. Nada de identificador, alcance, interações ou `taxa_engajamento_pct` (vazamento).
3. 75% treino e 25% teste, `random_state=42`, preservando a proporção do alvo.
4. Escolha três classificadores: regressão logística, árvore de classificação, Random Forest, Extra Trees, AdaBoost ou Gaussian Naive Bayes.
5. No teste, mostre precisão, recall e F1 dos três numa tabela e a matriz de confusão do modelo com maior F1.
6. Na regressão logística já ajustada, compare os cortes 0,50 e 0,30 com precisão, recall e F1 numa tabela.

Na resposta final, informe o modelo e o corte escolhidos e explique, em **até seis frases**, o que falso positivo e falso negativo significam para a equipe, justificando pelo trade-off entre precisão e recall.

### Armadilhas

A logística é **obrigatória** (a parte 6 mexe no corte dela). `.predict()` usa corte 0,50: pra outro corte precisa de `predict_proba(X_teste)[:, 1]`. O `ConvergenceWarning` é só aviso.

- **Falso positivo:** gastou um dos poucos espaços numa peça que não ia render.
- **Falso negativo:** uma peça que ia render ficou sem apoio.
- **Precisão:** das que o modelo indicou, quantas mereciam. **Recall:** das que mereciam, quantas ele achou.

### Código

```python
q8 = pd.read_csv("dados/publicacoes_analise.csv")
corte_p75 = q8["taxa_engajamento_pct"].quantile(0.75)
q8["mereceu_divulgacao_adicional"] = (q8["taxa_engajamento_pct"] > corte_p75).astype(int)
X = pd.get_dummies(q8[CARACTERISTICAS], columns=["tema", "formato"])
y = q8["mereceu_divulgacao_adicional"]
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

logistica = LogisticRegression(max_iter=5000)
modelos = {"regressão logística": logistica,
           "árvore de classificação": DecisionTreeClassifier(max_depth=4, random_state=42, class_weight="balanced"),
           "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42, class_weight="balanced")}
linhas = []
for nome, modelo in modelos.items():
    modelo.fit(X_treino, y_treino)
    decisao = modelo.predict(X_teste)
    linhas.append({"modelo": nome, "precisão": precision_score(y_teste, decisao, zero_division=0),
                   "recall": recall_score(y_teste, decisao, zero_division=0),
                   "F1": f1_score(y_teste, decisao, zero_division=0)})
comparacao_q8 = pd.DataFrame(linhas).sort_values("F1", ascending=False).round(3)
print(comparacao_q8.to_string(index=False))

nome_melhor = comparacao_q8.iloc[0]["modelo"]
cm = confusion_matrix(y_teste, modelos[nome_melhor].predict(X_teste))
print(f"Maior F1: {nome_melhor}")
print(f"VN={cm[0, 0]}  FP={cm[0, 1]}\nFN={cm[1, 0]}  VP={cm[1, 1]}")

probabilidade = logistica.predict_proba(X_teste)[:, 1]
linhas_corte = []
for corte in [0.50, 0.30]:
    d = (probabilidade >= corte).astype(int)
    linhas_corte.append({"corte": corte, "precisão": precision_score(y_teste, d, zero_division=0),
                         "recall": recall_score(y_teste, d, zero_division=0), "F1": f1_score(y_teste, d, zero_division=0),
                         "VP": int(((d == 1) & (y_teste.values == 1)).sum()),
                         "FP": int(((d == 1) & (y_teste.values == 0)).sum()),
                         "FN": int(((d == 0) & (y_teste.values == 1)).sum())})
print(pd.DataFrame(linhas_corte).round(3).to_string(index=False))
```

### Resultado

| modelo | precisão | recall | F1 |
| --- | --- | --- | --- |
| **regressão logística** | 0,750 | 0,857 | **0,800** |
| Random Forest | 1,000 | 0,429 | 0,600 |
| árvore de classificação | 0,500 | 0,571 | 0,533 |

Matriz da logística: VN 21, **FP 2**, **FN 1**, VP 6. O Random Forest nunca errou quando apostou, mas só achou 3 das 7: precisão sozinha não basta. Atenção: essa linha do Random Forest é a única que muda com a versão do scikit-learn (no 1.9 ele passa a liderar). Na prova, use o que aparecer na sua tela.

| corte | precisão | recall | F1 | VP | FP | FN |
| --- | --- | --- | --- | --- | --- | --- |
| 0,50 | 0,750 | 0,857 | 0,800 | 6 | 2 | 1 |
| 0,30 | 0,700 | **1,000** | **0,824** | 7 | 3 | 0 |

Baixar pra 0,30 pegou a única que escapava ao custo de um alarme falso a mais, e o F1 até subiu: aqui não houve trade-off difícil. Mas com 7 positivos no teste, cada acerto move o recall em cerca de 0,14.

### Resposta 8.1: tipo de modelo

> O aprendizado adequado é a classificação, porque a variável-alvo é binária, indicando apenas se a publicação merece ou não divulgação adicional, e a decisão da equipe também é binária. A regressão não responde diretamente a essa decisão porque estima um valor contínuo, que ainda precisaria de um corte arbitrário para virar ação. A clusterização não responde porque agrupa registros por semelhança sem usar nenhuma resposta conhecida, enquanto aqui a resposta existe e foi definida pela própria equipe a partir do percentil 75.

### Resposta 8: decisão e riscos de erro

> Escolhi a regressão logística, que teve o maior F1 entre os três modelos comparados, com 0,800, e o corte de 0,30 em vez do padrão de 0,50. Um falso positivo significa gastar um dos poucos espaços de divulgação adicional numa publicação que não iria render, desperdiçando um recurso escasso nos dias finais da campanha, e um falso negativo significa deixar sem apoio uma peça que teria bom desempenho, uma oportunidade que não volta antes do festival. No corte padrão de 0,50, o modelo encontrou 6 das 7 publicações que realmente mereciam apoio, com 2 alarmes falsos e 1 deixada passar. Baixando o corte para 0,30, ele passa a encontrar todas as 7, levando o recall a 1,00, ao custo de apenas um alarme falso a mais, e a precisão cai pouco, de 0,75 para 0,70, de modo que o F1 ainda sobe, de 0,800 para 0,824. Como o ganho de recall custou quase nada em precisão, o corte mais baixo é melhor pelos dois critérios ao mesmo tempo, e não um trade-off difícil como normalmente seria. A ressalva importante é que o conjunto de teste tem apenas 30 publicações e 7 positivos, de forma que cada acerto ou erro move o recall em cerca de 0,14 ponto: a vantagem observada para o corte de 0,30 equivale a uma única publicação e não deveria ser tratada como regra estável para as próximas campanhas.

## Os seis erros que mais custam ponto

1. Esquecer `pd.get_dummies` nas Q6, Q7 e Q8.
2. Usar `stratify` na regressão (Q7).
3. `drop_duplicates()` sem `subset="id_publicacao"` (Q2).
4. `dayfirst=True` numa coluna com formatos misturados, sem conferir `.min()` e `.max()` (Q2).
5. Gráfico sem título, nome de eixo ou fonte (Q3, Q4, Q5).
6. Resposta em Markdown genérica ou com o número errado de frases.
