# Guia de Consulta — Extração e Análise de Dados

Material de consulta para a A1 de E&AD (Prof. Matheus Pestana, FGV 2026.2) — prova prática, **conteúdo até a Aula 13** (a Aula 14, de API e persistência, não cai).
Organizado por **técnica**, não por questão: serve mesmo que a prova mude o tema, os nomes das colunas ou a ordem das perguntas.

Baseado no simulado "Festival ViraBairro" e no código das aulas do [repositório da matéria](https://github.com/mateuspestana/extracao_analise_2026). Todo o código foi executado e testado com pandas 1.5, 2.2 e 3.0.

---

## Para a prova (deixe aberto)

1. **`prova-template.ipynb`** — comece por aqui. Uma seção por tipo de questão. Células **`# [COLE]`** são código de prova: copie a célula inteira e troque o que tem `# <-- troque` — ela produz só o que o enunciado pede. Células **`# [NÃO COLE]`** são conferência para você (imprimem `>>> PARA A RESPOSTA` com os números para o texto). Nenhuma célula precisa ser copiada pela metade. Roda inteiro de cara com uma base de exemplo; na prova, troque `PASTA` na seção 1.
   [Abrir no Colab](https://colab.research.google.com/github/BeAmara1/prova-pestana/blob/main/prova-template.ipynb)
2. **`00-fluxograma.md`** — quando não souber por onde começar: qual seção do template, qual modelo, em que ordem limpar, qual gráfico.
3. **`10-frases-prontas.md`** — para escrever as respostas sem travar.
4. **`12-erros-por-questao.md`** — antes de fechar cada questão, a lista do que costuma custar ponto.
5. **`11-erros-comuns.md`** — quando der erro (ou quando o resultado parecer estranho sem dar erro).

## Roteiro de 30 segundos (toda questão)

1. **Que arquivo?** `*_brutas.csv` → precisa limpar. `*_analise.csv` → usar direto, em variável nova.
2. **Que tipo de tarefa?** Ache a seção na tabela abaixo (ou siga o `00-fluxograma.md`).
3. **Copie as células `[COLE]` da seção**, inteiras, e troque o que está marcado com `# <-- troque`.
4. **Rode e confira o resultado** — não confie só porque não deu erro.
5. **Escreva a resposta** com os números da célula `[NÃO COLE]` da seção e uma frase do `10-frases-prontas.md`.

---

## Índice: "o enunciado pede isso" → "vá para"

| O enunciado pede... | Template | Explicação |
|---|---|---|
| head, shape, ausências, tipos, valores únicos, "conhecer a base" | seção 3 | `01-diagnostico.md` |
| tirar duplicata, padronizar texto, converter data/número, tratar ausente/inválido | seção 4 | `02-limpeza.md` |
| criar uma taxa com fórmula; features a partir de legenda/hashtags/data | seção 5 | `02-limpeza.md`, `06-regressao.md` |
| tabela por grupo, contagem + média/mediana, cruzar duas categorias, hashtags | seção 6 | `03-agrupar-e-tabelas.md` |
| gráfico de barras / linha / dispersão / horizontal, título, eixos, fonte | seção 7 | `04-graficos.md` |
| "por dia", recorte por hora/formato, top 5 | seção 8 | `05-datas-e-recortes.md` |
| **prever um número** (taxa esperada) — MAE, R², modelo bobo | seção 9 | `06-regressao.md` |
| **prever uma categoria** (merece/não merece) — precisão, recall, F1, matriz, cortes, importâncias | seção 10 | `07-classificacao.md` |
| **agrupar sem rótulo** — KMeans, escolher k, perfis | seção 11 | `08-clusterizacao.md` |
| extrair de HTML (BeautifulSoup, requests) | seção 12 | `09-scraping-e-apis.md` |
| a **resposta escrita** (causalidade, limitação, interpretação) | blocos "Para a resposta" | `10-frases-prontas.md` |
| não sei qual técnica / qual modelo / qual gráfico | — | `00-fluxograma.md` |
| só quero o snippet, rápido | — | `00-COLA-RAPIDA.md` |

**Dica de velocidade:** no GitHub, `t` busca arquivo e `Ctrl+F` busca dentro dele. Os títulos usam as palavras do enunciado ("mediana por tema", "matriz de confusão", "vazamento") de propósito.

---

## Checklist — as 10 coisas que mais custam nota

1. **Recarregue o CSV** quando o enunciado disser "em uma nova variável" ou "use somente o arquivo X".
2. **Gráfico sem título, sem nome de eixo ou sem a fonte dentro da figura** é ponto perdido. Se o enunciado escreve "Fonte: ...", isso tem que aparecer no gráfico.
3. **Mediana ≠ média**, e **taxa de utilidade ≠ taxa de engajamento**. Leia a palavra no enunciado.
4. **Nunca afirme causalidade.** "Associado a", "tende a", "nesta base". Nunca "causa", "prova que", "garante".
5. **Vazamento de dados:** para prever algo *antes* da publicação, nada de `alcance`, interações, curtidas, compartilhamentos, salvamentos, nem a coluna que gerou o rótulo. R² ou F1 perto de 1 de primeira = vazamento quase certo.
6. **`random_state=42`** em tudo que sorteia (split, árvore, floresta, KMeans).
7. **`stratify=y`** no split de classificação; **padronize** (`StandardScaler`) antes da regressão logística e do KMeans.
8. **Categoria vira número** com `pd.get_dummies(..., drop_first=True, dtype=int)` antes de qualquer modelo.
9. **Confira as datas depois de converter.** No pandas 3 (o que o `uv pip install` do curso instala hoje), o jeito da Aula 10 (`format="mixed", dayfirst=True`) inverte dia e mês das datas ISO com dia ≤ 12, sem dar erro. O `converter_data` do template acerta em todas as versões; veja `02-limpeza.md`.
10. **Respeite o limite de frases.** Uma frase por item pedido (indicação, explicação, limitação).

---

## Estrutura

```
.
├── README.md
├── prova-template.ipynb               ← o notebook para a prova
├── solucao-simulado-virabairro.ipynb  ← o simulado inteiro resolvido
├── 00-fluxograma.md                   ← decisão rápida: seção, modelo, limpeza, gráfico
├── 00-COLA-RAPIDA.md                  ← os snippets mais usados, numa página
├── 01-diagnostico.md
├── 02-limpeza.md
├── 03-agrupar-e-tabelas.md
├── 04-graficos.md
├── 05-datas-e-recortes.md
├── 06-regressao.md
├── 07-classificacao.md
├── 08-clusterizacao.md
├── 09-scraping-e-apis.md
├── 10-frases-prontas.md
├── 11-erros-comuns.md
├── 12-erros-por-questao.md
└── 99-testar-a-cola.py                ← confere se o template roda na versão de hoje
```

## Conferir antes da prova

Roda o template inteiro e confere os resultados (não só se deu erro):

```bash
python 99-testar-a-cola.py
```

No Colab:

```python
!git clone https://github.com/BeAmara1/prova-pestana.git
%cd prova-pestana
!python 99-testar-a-cola.py
```
