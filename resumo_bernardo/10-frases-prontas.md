# 10 — Frases prontas para as respostas escritas

As respostas em Markdown valem tanto quanto o código, repetem os mesmos
temas e têm limite de frases. Aqui está o banco pronto — **adapte com os seus
números**, não copie cru.

## A estrutura que sempre funciona

Quase toda resposta pede a mesma tríade:

1. **O que os dados mostram** (com o número que saiu)
2. **O que isso significa** (interpretação da métrica)
3. **Limitação** (por que não dá pra concluir mais que isso)

Se o enunciado pede 3-5 frases, é uma frase por item + uma de recomendação.

---

## Causalidade — a ressalva mais cobrada

Use uma destas, adaptando ao contexto:

> Os dados mostram uma **associação** entre [X] e [Y] nas publicações
> observadas, mas não permitem afirmar que [X] **cause** [Y]: as peças também
> diferem em tema, formato, horário e perfil de autor, e não houve comparação
> controlada.

> Trata-se de uma escolha de comunicação apoiada em evidência descritiva, não
> de uma relação causal demonstrada.

> Um recorte com bom desempenho não demonstra que a característica usada no
> recorte seja a responsável pelo resultado — fatores não medidos podem
> explicar a diferença.

**Palavras seguras:** associado a, relacionado a, tende a, nos dados
observados, apresenta maior/menor.
**Palavras proibidas:** causa, provoca, garante, prova que, faz com que.

## Mediana (e por que não a média)

> A mediana representa o valor típico da taxa entre as publicações do grupo:
> metade ficou acima e metade abaixo desse valor. Ela é menos sensível a
> publicações com desempenho excepcional do que a média, o que evita que um
> único pico distorça a leitura do tema.

## Limitações da base — cardápio

Escolha a que couber:

- **Recorte temporal:** "A base cobre apenas oito semanas de campanha, período
  curto demais para caracterizar tendência."
- **Dados sintéticos / fonte única:** "Os dados são sintéticos e referem-se a
  um único festival fictício, o que impede generalizar para outras redes,
  públicos ou bairros."
- **Grupos pequenos:** "Algumas combinações têm poucas publicações, o que
  torna a mediana instável e pouco confiável para esses grupos."
- **Variáveis não observadas:** "A base não registra o conteúdo da peça, o
  investimento em impulsionamento nem o contexto da data, fatores que podem
  explicar parte das diferenças."
- **Mudança de plataforma:** "Alterações no algoritmo de distribuição das
  redes podem alterar os resultados observados, limitando a validade do
  padrão para o futuro."
- **Não é amostra aleatória:** "As publicações não constituem amostra
  aleatória de nada — foram as peças que a equipe decidiu publicar."

## Recomendação editorial (questões de escolha de tema/formato)

> Recomendo destacar **[TEMA]**, que apresentou a maior mediana de taxa de
> utilidade ([VALOR]%) entre os quatro temas — ou seja, foi o conteúdo que as
> pessoas mais tenderam a salvar ou compartilhar, e não apenas o mais visto. A
> mediana indica o comportamento típico do tema, sendo menos afetada por picos
> isolados que a média. Vale observar que [TEMA] também pode estar associado a
> formatos ou horários específicos, então a diferença não isola o efeito do
> tema. Como o festival tem poucos espaços de divulgação, a sugestão é testar
> esse destaque e acompanhar o resultado antes de consolidar a decisão.

## Análise multivariada (tema × formato)

> Analisar tema e formato **juntos** revela diferenças que a média de cada
> variável isolada esconde: um tema pode ter desempenho forte em um formato e
> fraco em outro, e olhar só o tema produziria um valor médio que não
> corresponde a nenhuma das duas situações. A combinação **[TEMA – FORMATO]**
> apresentou a maior mediana ([VALOR]%) e merece ser testada pela equipe.
> Ainda assim, algumas combinações têm poucas publicações, o que torna a
> comparação frágil nesses casos.

## Vazamento de dados

> Não utilizei `alcance`, `interacoes` nem variáveis derivadas da taxa como
> características, porque esses valores só existem **depois** que a
> publicação foi ao ar. Usá-los produziria um modelo com desempenho
> artificialmente alto, incapaz de apoiar uma decisão tomada **antes** da
> publicação — isso caracteriza vazamento de dados.

## Métricas — explicações curtas

- **MAE:** "mede o erro médio absoluto entre valor previsto e observado, na
  mesma unidade do alvo; quanto menor, mais próxima a estimativa."
- **R²:** "indica quanto da variação do alvo o modelo explica; valores
  próximos de zero ou negativos indicam baixo poder preditivo com as
  variáveis disponíveis."
- **Precisão:** "das publicações que o modelo indicou, quantas realmente
  mereciam — protege contra desperdício de espaço."
- **Recall:** "das publicações que realmente mereciam, quantas o modelo
  encontrou — protege contra oportunidade perdida."
- **F1:** "combina precisão e recall em um único número, útil quando se busca
  equilíbrio entre os dois erros."
- **Silhueta:** "mede o quão bem separados estão os grupos; quanto mais
  próximo de 1, melhor a separação."

## Modelo bobo (baseline) — Aulas 11 e 12

> Comparei os modelos com um **modelo bobo**, que prevê sempre a média do treino (regressão) ou sempre a classe mais comum (classificação). [MODELO] teve MAE [X] contra [Y] do modelo bobo, então aprendeu algum padrão além de "chutar a média" — ainda que modesto.

> Um modelo que respondesse sempre "não merece" teria acurácia de ~75% nesta base, porque só um quarto das publicações está acima do percentil 75 — e não encontraria nenhuma. Por isso a comparação usa precisão, recall e F1, e não acurácia.

## Clusters (Aula 13)

> O grupo [A] reúne [N] publicações de perfis com poucos seguidores (mediana [X]) e legendas longas ([Y] caracteres, contra [Z] na média geral); o grupo [B] [...]. Os nomes descrevem a tabela de médias por cluster; não são categorias que existiam antes na base.

## Importância de variável

> Uma importância alta indica apenas que o modelo usou muito aquela
> característica para separar as classes **nesta base**, o que não demonstra
> relação causal: a variável pode estar correlacionada a outro fator não
> observado. Uma mudança na composição da base — entrada de um formato novo,
> concentração de publicações em um tema, ou alteração no alcance orgânico da
> plataforma — poderia alterar completamente esse ranking.

## Falso positivo / falso negativo (contexto do festival)

> Um **falso positivo** significa destinar um dos poucos espaços de
> divulgação a uma publicação que não traria retorno relevante, desperdiçando
> um recurso escasso. Um **falso negativo** significa deixar de impulsionar
> uma publicação que teria bom desempenho, resultando em oportunidade
> perdida.

## Escolha de corte

> Baixar o corte de 0,50 para 0,30 elevou o recall de [X] para [Y], mas
> reduziu a precisão de [A] para [B]: o modelo passa a indicar mais
> publicações, encontrando mais peças realmente boas e também mais peças que
> não mereciam. Como [os espaços são muito limitados / há capacidade de
> divulgar mais peças], optei pelo corte de **[VALOR]**, priorizando
> **[precisão/recall]**.

---

## Erros de escrita que custam ponto

- Passar do limite de frases pedido.
- Responder o que não foi perguntado e esquecer o que foi (o enunciado
  costuma pedir **três coisas**: indicação + explicação + limitação — confira
  uma a uma).
- Deixar `[VALOR]` genérico sem colocar o número que saiu no seu código.
- Afirmar causalidade.
- Descrever o código em vez de interpretar o resultado ("usei o groupby e
  ordenei" não é análise).
