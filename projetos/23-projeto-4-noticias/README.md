# Projeto 4 — Clipping comparativo

## Objetivo e pergunta

Pergunta: O que este recorte de notícias da Agência Brasil e da CNN Brasil mostra sobre a cobertura de Lula e Flávio Bolsonaro?

Objetivo: Transformar textos de notícias em dados que dá para conferir e escrever conclusões do tamanho da amostra. Este trabalho fala só destas 40 matérias, e não da cobertura total dos veículos.

## Preparação

- **Fonte:** tabela `noticias_lula_flavio_2026.csv`, do repositório da disciplina.
- **Janela temporal:** matérias de outubro de 2026.
- **Regra de seleção:** 40 matérias, 10 por combinação de veículo (Agência Brasil e CNN Brasil) e foco (Lula e Flávio Bolsonaro). Não é uma amostra aleatória. Usei só título e resumo (`texto_analise`).
- **Denominadores:** cada grupo tem 10 matérias, e 4 de cada grupo foram para a extração com a Groq (16 no total). Menções a Lula e a Flávio por grupo:
  - Agência Brasil, foco Flávio: 6 a Lula e 13 a Flávio
  - Agência Brasil, foco Lula: 13 a Lula e 4 a Flávio
  - CNN Brasil, foco Flávio: 6 a Lula e 11 a Flávio
  - CNN Brasil, foco Lula: 10 a Lula e 2 a Flávio

## Revisão das aulas 21 e 22

Na aula 21 vimos como limpar texto com regex (minúsculas, tirar links, ficar só com letras e tirar stopwords) sem perder informação importante, como as negações. Na aula 22 vimos TF-IDF e NMF para achar tópicos. O nome do tópico é interpretação minha, feita depois de ler as manchetes.

## Roteiro de análise

1. Carregar a base e conferir as 40 linhas.
2. Limpar o texto e conferir vazios, duplicatas e tokens antes e depois.
3. Rodar TF-IDF e NMF (4 tópicos) e contar as menções a Lula e Flávio.
4. Extrair fichas com a Groq em 16 matérias, com uma chamada de teste antes do lote.
5. Auditar 4 fichas, uma por combinação de veículo e foco.
6. Comparar a busca por palavra e a busca semântica.

## Prática aplicada

- **Preparação:** Os tokens foram de 1279 para 895, sem textos vazios nem duplicados. Mantive "não" e "sem" para não inverter o sentido (como em "sem áudio", na P33). Um problema que apareceu: "São Paulo" virou "paulo", porque "são" estava na minha lista de stopwords (P11).
- **Tópicos:** Os quatro nomes provisórios foram "segundo turno e conselhos de Bolsonaro a Flávio", "canal Exército do Lula e TSE", "atos e apoios no Rio" e "campanha e custo de vida".
- **Extração:** Das 16 fichas, todas voltaram com a evidência literal (True).
- **Busca:** Usei a pergunta "Quais notícias tratam de apoio de lideranças políticas a candidatos?". A busca por palavra trouxe P21, P04 e P37. A busca semântica trouxe P14, P21 e P40.

## Resultados do desafio

### Descrição dos dados

- Nos quatro grupos, o candidato do foco é o mais citado nos títulos e resumos.
- O tópico 0 concentra a CNN com foco em Flávio. O tópico 2 concentra a Agência Brasil.
- As 16 fichas tiveram evidência literal, mas as 4 que auditei tinham problemas.

### Achados com IDs e links

**Achado 1:** o mesmo episódio aparece nos dois veículos. O P09 ([Agência Brasil](https://agenciabrasil.ebc.com.br/politica/noticia/2026-10/campanha-registra-canal-exercito-do-lula-na-justica-eleitoral)) e o P27 ([CNN Brasil](https://www.cnnbrasil.com.br/blogs/gustavo-uribe/eleicoes/canal-exercito-do-lula-e-registrado-junto-ao-tse/)) falam do registro do canal "Exército do Lula". Interpretação: O tópico 1 parece ser um episódio específico e não um tema geral da campanha.

**Achado 2:** o foco da amostra não é quem faz a ação. No P40 ([CNN Brasil](https://www.cnnbrasil.com.br/blogs/gustavo-uribe/eleicoes/michelle-sinaliza-preferencia-por-exercer-mandato-caso-flavio-seja-eleito/)), que está no foco Flávio, quem sinaliza a preferência é Michelle. Interpretação: O foco diz por que a matéria entrou na base, e não quem é o agente.

**Achado 3:** a busca semântica achou a P14 ([Agência Brasil](https://agenciabrasil.ebc.com.br/politica/noticia/2026-10/flavio-bolsonaro-recebe-apoios-de-governadores-eleitos-e-cury)), sobre apoio de governadores a Flávio, e a busca por palavra não achou. Interpretação: Para essa pergunta, a semântica deu um resultado mais direto.

### Quatro fichas auditadas

- **P11 (Agência Brasil, foco Flávio):** O fato só repete a manchete. Ficaram de fora as críticas a Lula, as promessas econômicas e a afirmação de que os cortes não virão da área social. Marcação: ausência.
- **P09 (Agência Brasil, foco Lula):** A pessoa central veio vazia e a ficha não diz quem é o agente. O prazo de 48 horas foi parar no campo `limite`. Marcação: ausência e campo usado errado.
- **P40 (CNN Brasil, foco Flávio):** A pessoa central é Michelle, e "exercer mandato" ficou vago. O `limite` é um pedaço do texto. Marcação: ambiguidade e campo usado errado.
- **P27 (CNN Brasil, foco Lula):** O fato só fala do registro do canal. Janones aparece só como criador do canal, e o texto não diz quem fez o registro. Marcação: atribuição ambígua e campo usado errado.

### Tópico confuso

O tópico 3 ("campanha e custo de vida") juntou assuntos diferentes. As palavras "casa" e "vida" vêm de matérias sem relação: a P26 fala de custo de vida e de gravar em casa de apoiadores, e a P01 fala de religião e do Minha Casa, Minha Vida.

### Comparação das buscas

A P21 apareceu nas duas buscas. Só a semântica trouxe a P14 (relevante) e só a de palavras trouxe P04 e P37. Pela minha avaliação, a P21 e a P14 são relevantes, a P04 e a P40 são parciais e a P37 é pouco relevante. A semântica teve 2 relevantes entre 3, e a de palavras teve 1.

### Limitações

- São 40 matérias escolhidas, 10 por grupo, e não uma amostra aleatória.
- Usei só título e resumo, nunca a matéria inteira.
- Menções são contagens de palavras, e não de matérias.
- A extração foi feita em 16 matérias, com um modelo e uma execução, e só 4 fichas foram auditadas.
- A avaliação de relevância foi minha, só para o top 3 de uma pergunta.

## Declaração de uso de IA

Usei o Claude para ajudar em algumas interpretações que não estava conseguindo entender. Os códigos são os das aulas 21, 22 e 23.

