**Projeto 3**

## Rascunho da descrição dos segmentos

> Segmento 0 (121 posts): escreve legenda bem grande (mais ou menos 300 caracteres) e usa bastante hashtag, geralmente postando à noite. Segmento 1 (115 posts): escreve bem poucon (mais ou menos 53 caracteres), quase não usa hashtag e costuma postar de madrugada. Segmento 2 (794 posts, a maioria): legenda de tamanho médio (mais ou menos 56 caracteres), poucas hashtags, e também posta à noite (só que escreve bem menos que o Segmento 0).

## Parte D — README 

Crie `README.md` dentro de `projetos/13-segmentacao-clusterizacao/` na sua pasta de entregas:

**Fonte, período e tamanho da coleta:**

> Tiktok. Coleta realizada dia 26 de agosto de 2026. Tamanho: 1030 posts.

**As duas variáveis que você criou (a contínua da Parte A e o rótulo da Parte B), com a fórmula/critério de cada uma:**

> Taxa de engajamento (parte A): (likes + comments + shares) / plays. Viralizou (parte B): considerei viral o que ficou acima do percentil 90 de plays.

**As features usadas nas Partes A e B, e quais colunas você descartou por vazamento:**

> Usei tamanho da legenda, número de hashtags e hora do post. As colunas que descartei foram os likes, comments, shares e plays.

**Parte A — resultado:** MAE e R² do modelo bobo, da linear e da árvore. O seu melhor modelo bateu o bobo?

> O modelo bobo deu MAE 0,032 e R² -0,005. A regressão linear: MAE 0,028 e R² 0,217. A árvore ficou: MAE 0,029 e R² 0,098. Ou seja, a linear bateu o bobo e foi a melhor das três.

**Parte B — resultado:** a matriz de confusão e uma leitura: a favor de quem o modelo erra?

> Com o threshold padrão de 0,5, o modelo classificou todos os posts como "não viral". Deu 90% de acurácia, mas ele não acertou nenhum viral de verdade (precisão e recall zerados). Só baixando o threshold pra 0,15 ele começou a pegar alguns virais (4 de 25), mas ainda errou.

**Parte C — resultado:** quantos segmentos, como você escolheu `k`, e a descrição de cada segmento (uma frase com número).

> Escolhi 3 clusters (k=3), porque foi onde a silhueta deu o valor mais alto. Ficou um grupo pequeno (121 posts) que escreve legendas gigantes e usa muita hashtag à noite, outro grupo pequeno (115 posts) que escreve pouco e posta de madrugada, e o grupo grande (794 posts, a maioria) que escreve médio e também posta à noite.

**Uma conclusão que os seus dados sustentam** (sem extrapolar para além da sua coleta):

> Com essa coleta, não dá pra prever direito quem vai viralizar só olhando hora do post, tamanho da legenda e hashtags, os modelos não foram muito bem nisso. 

**Revisão por pares:** nome do colega **da turma** que revisou, o que ele apontou, e o que você mudou (ou por que não mudou).

> Nome: Giovanna Couto. Revisão: Ela apontou que nanparte B o modelo não conseguiu identificar nenhum post viral e isso é uma limitação. E também apontou que usei o mínimo de features que foram cobrados e que eu poderia ter colocado mais. Não alterei pois são informações mais simples de extrair e acho que fica mais fácil de interpretar, menos bagunçado. Não achei necessário colocar mais de 3. Também não alterei a parte do modelo por que não sei o motivo de ter dado errado para eu conseguir mudar.

**Declaração de uso de IA:** ferramenta usada, em que trecho ou decisão, e o que você conferiu ou alterou depois (mesmo que seja "não usei IA nesta entrega"). Lembre: nesta entrega, IA não pode ser usada para gerar o código de análise.

> Declaração de uso de IA: usei o Claude pra me ajudar na Parte C (Segmentação), porque eu tava com dificuldade de entender a lógica do K-Means e da clusterização. Também usei pra corrigir uns erros no código, eu peguei todos os código das aulas, mas tinha que adaptar algumas coisas pra minha base de dados e ficava dando erro, e eu não sabia resolver sozinha. Fui testando no notebook e entendendo o porquê de cada correção antes de aceitar, não usei pra gerar a análise do zero.