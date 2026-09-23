"""Roda o prova-template.ipynb célula por célula e avisa o que quebrou.

Use no dia da prova (ou antes) para conferir se tudo funciona na versão
de pandas / scikit-learn / matplotlib instalada:

    python 99-testar-a-cola.py

No Colab:
    !git clone https://github.com/BeAmara1/prova-pestana.git
    %cd prova-pestana
    !python 99-testar-a-cola.py
"""
import json
import sys
import time
import traceback
import warnings
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # sem janela de gráfico
import matplotlib.pyplot as plt  # noqa: E402

NOTEBOOK = Path(__file__).with_name("prova-template.ipynb")


def secao_de(celulas, indice):
    """Título da seção (## ...) mais próxima acima da célula."""
    for c in reversed(celulas[:indice]):
        if c["cell_type"] == "markdown":
            for linha in "".join(c["source"]).splitlines():
                if linha.startswith("## "):
                    return linha[3:].strip()
    return "início"


def main():
    if not NOTEBOOK.exists():
        print(f"não achei {NOTEBOOK.name} na mesma pasta deste script")
        return 1

    with open(NOTEBOOK, encoding="utf-8") as f:
        celulas = json.load(f)["cells"]

    import pandas as pd
    import sklearn
    print(f"python {sys.version.split()[0]} | pandas {pd.__version__} | "
          f"scikit-learn {sklearn.__version__} | matplotlib {matplotlib.__version__}")
    print("-" * 70)

    ns = {"__name__": "__template__", "display": lambda *a, **k: None}   # display só existe no Jupyter
    falhas, avisos, total = [], [], 0
    inicio = time.time()

    for i, c in enumerate(celulas):
        if c["cell_type"] != "code":
            continue
        total += 1
        codigo = "".join(c["source"]).replace("plt.show()", "plt.close('all')")
        # a última linha "solta" de uma célula é só exibição no notebook; aqui não precisa
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            try:
                import contextlib
                import io
                with contextlib.redirect_stdout(io.StringIO()):
                    exec(compile(codigo, f"<célula {i}>", "exec"), ns)
            except Exception as e:  # noqa: BLE001
                falhas.append((i, secao_de(celulas, i), f"{type(e).__name__}: {e}",
                               traceback.format_exc(limit=1)))
            for aviso in w:
                if issubclass(aviso.category, (DeprecationWarning, ResourceWarning)):
                    continue
                avisos.append((i, secao_de(celulas, i), f"{aviso.category.__name__}: {aviso.message}"))
        plt.close("all")

    print(f"{total} células de código em {time.time() - inicio:.1f}s")

    # "não quebrou" não basta: confere se os resultados da base de exemplo estão certos
    # (erros silenciosos, como data virando vazio numa versão antiga do pandas)
    checagens = [
        ("limpeza: tema com 4 categorias", lambda: ns["df"]["tema"].nunique() == 4),
        ("limpeza: nenhuma data perdida na conversão", lambda: ns["df"]["data_publicacao"].notna().all()),
        ("limpeza: datas dentro de ago-set/2026 (sem inverter dia e mês)",
         lambda: ns["df"]["data_publicacao"].between("2026-08-01", "2026-09-30 23:59").all()),
        ("limpeza: duplicatas removidas", lambda: not ns["df"]["id_publicacao"].duplicated().any()),
        ("taxa: sem infinito nem ausente", lambda: ns["df"]["taxa_utilidade_pct"].notna().all()
         and (ns["df"]["taxa_utilidade_pct"].abs() < float("inf")).all()),
        ("tabela diária com dias", lambda: len(ns["diario"]) > 30),
        ("regressão: tabela só com os 2 modelos pedidos", lambda: len(ns["tabela_reg"]) == 2),
        ("regressão: melhor modelo bate o modelo bobo", lambda: ns["tabela_reg"]["MAE"].min() < ns["mae_bobo"]),
        ("classificação: tabela só com 3 modelos e precisão/recall/F1",
         lambda: len(ns["tabela_clf"]) == 3 and list(ns["tabela_clf"].columns) == ["modelo", "precisao", "recall", "f1"]),
        ("classificação: 5 importâncias", lambda: len(ns["top5"]) == 5),
        ("base de exemplo não escreve em dados/", lambda: ns["PASTA"] == "dados_exemplo"),
        ("classificação: ~25% de classe 1", lambda: 0.2 < ns["y"].mean() < 0.3),
        ("classificação: corte menor aumenta o recall",
         lambda: ns["tabela_cortes"]["recall"].iloc[-1] >= ns["tabela_cortes"]["recall"].iloc[0]),
        ("clusterização: silhueta calculada", lambda: len(ns["silhuetas"]) > 0),
        ("scraping: 2 linhas extraídas", lambda: len(ns["coletado"]) == 2),
    ]
    erradas = []
    for nome, teste in checagens:
        try:
            ok = bool(teste())
        except Exception as e:  # noqa: BLE001
            ok, nome = False, f"{nome} ({type(e).__name__}: {e})"
        if not ok:
            erradas.append(nome)
    if erradas:
        falhas.extend((-1, "resultado", f"resultado errado: {n}", "") for n in erradas)
    if avisos:
        print(f"\n{len(avisos)} aviso(s) — funciona, mas vale saber:")
        for i, sec, msg in avisos[:15]:
            print(f"  célula {i} [{sec}]: {msg[:160]}")
    if falhas:
        print(f"\n{len(falhas)} problema(s):")
        for i, sec, msg, _ in falhas:
            onde = f"célula {i}" if i >= 0 else "checagem"
            print(f"  {onde} [{sec}]: {msg[:200]}")
        print("\nA primeira falha costuma causar as seguintes (variável que não foi criada).")
        return 1
    print(f"{len(checagens)} checagens de resultado: todas certas")
    print("\nTUDO OK — o template roda inteiro nesta versão e dá os resultados esperados.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
