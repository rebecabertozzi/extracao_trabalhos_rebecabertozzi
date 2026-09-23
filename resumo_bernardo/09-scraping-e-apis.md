# 09 — Scraping (Aulas 8 e 9)

**Aviso:** o simulado diz que *não* há coleta, requisições web nem scraping. Mas a A1 vai "até a Aula 13", então as Aulas 8 (requests + BeautifulSoup) e 9 (Playwright) estão no escopo. Este arquivo é a reserva. No template: **seção 12** (roda com um HTML embutido). A Aula 14 (API e persistência) **não cai** — está no fim só como referência.

## Ler o HTML

```python
from pathlib import Path
html = Path("exemplos/pagina-teste.html").read_text(encoding="utf-8")   # arquivo local
```

Ou da web (Aula 8):

```python
import requests

url = "http://books.toscrape.com/"
resposta = requests.get(url, timeout=20)
print(resposta.status_code)                         # 200 = ok, 404 = não existe, 403 = bloqueado
if resposta.status_code == 200:
    resposta.encoding = resposta.apparent_encoding  # evita "Â£" no lugar de "£"
    html = resposta.text
```

Boas práticas que valem ponto: `timeout`, checar `status_code` antes de seguir, pausa entre requisições (`time.sleep(1)`), respeitar `robots.txt`.

## Extrair com BeautifulSoup (estilo da Aula 8)

```python
from bs4 import BeautifulSoup

sopa = BeautifulSoup(html, "html.parser")
print(sopa.title.get_text())                                  # a tag <title>
primeiro = sopa.find("li", {"class": "post"})                 # o PRIMEIRO que casa
todos = sopa.find_all("li", {"class": "post"})                # TODOS
sopa.find(id="titulo-site")                                   # por id
link = primeiro.find("a", {"class": "link-post"})
link.get_text(strip=True)                                     # texto visível, sem espaços nas pontas
link["href"]                                                  # atributo
```

O padrão da prova: achar o **bloco que se repete** e, dentro dele, cada campo; guardar um dicionário por bloco numa lista; virar DataFrame.

```python
linhas = []
for post in sopa.find_all("li", {"class": "post"}):                        # <-- o bloco
    titulo = post.find("h2", {"class": "titulo-post"})                    # <-- cada campo
    link = post.find("a", {"class": "link-post"})
    linhas.append({
        "titulo": titulo.get_text(strip=True) if titulo else None,        # campo ausente não quebra o laço
        "link": link["href"] if link else None,
    })

df = pd.DataFrame(linhas)
```

O `if ... else None` é o que impede um único bloco incompleto de derrubar o laço inteiro com `AttributeError: 'NoneType' object has no attribute 'get_text'`.

Link relativo (`catalogue/livro_1/index.html`) vira completo com `requests.compat.urljoin(url, link)` (Aula 8). No `books.toscrape.com` o título inteiro está no atributo `title` do `<a>` (o texto visível vem cortado com "...").

### Tabela pronta em HTML

```python
tabelas = pd.read_html(html)      # lista de DataFrames, um por <table>
df = tabelas[0]
```

## Página dinâmica (Aula 9, Playwright)

Quando o `requests` devolve a página "vazia" (o conteúdo só aparece depois do JavaScript), use um navegador de verdade:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)             # a aula usa headless=False para ver o navegador
    page = browser.new_page()
    page.goto("https://exemplo.com", wait_until="domcontentloaded", timeout=45000)   # <--
    page.wait_for_selector('[data-testid="story-item"]', state="attached", timeout=45000)   # <-- espera o conteúdo
    html = page.content()                                  # daqui em diante, BeautifulSoup normal
    browser.close()
```

Botão "carregar mais" (como no `02_listar_com_more_stories.py` da aula), num laço:

```python
botao_more = page.locator('[data-testid="load-more-stories-button"]')    # <-- seletor do botão
botao_more.first.click(timeout=10000)
# ou pelo texto: page.get_by_role("button", name="More stories").first.click()
page.wait_for_timeout(3000)                                              # dá tempo de carregar
```

## Salvar o resultado (Aulas 8 e 10)

```python
df.to_csv("dados/processed/coleta-tratada.csv", index=False)   # index=False: sem coluna extra sem nome
```

Aula 10: **nunca** salve por cima do bruto (`dados/raw/`). Saída sempre com outro nome, em `dados/processed/`.

## Resposta escrita (ética e limites)

> A coleta respeitou o `robots.txt` e usou intervalo entre requisições para não sobrecarregar o servidor. Os dados refletem apenas o que estava publicamente disponível no momento da coleta, num recorte específico de páginas, e podem mudar a qualquer momento — o que limita a reprodutibilidade e impede generalizar para toda a plataforma.

---

## Referência — Aula 14 (NÃO cai na A1)

```python
dados = requests.get("https://api.exemplo.com/dados", params={"limite": 100}, timeout=20).json()
df = pd.json_normalize(dados["resultados"])     # JSON aninhado vira tabela

import sqlite3
con = sqlite3.connect("dados/base.db")
df.to_sql("publicacoes", con, if_exists="replace", index=False)
pd.read_sql("SELECT * FROM publicacoes", con)
df.to_parquet("dados/resultado.parquet")
```
