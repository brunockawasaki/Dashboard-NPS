# -*- coding: utf-8 -*-
"""Gera o dashboard da Pesquisa de Satisfação (Processos) com os dados já dentro.

Lê a planilha MAIS RECENTE (.xlsx ou .csv) da pasta NPS e grava "Dashboard NPS.html" na mesma pasta.
Uso:  python gerar_dashboard_nps.py            (usa a pasta NPS padrão)
      python gerar_dashboard_nps.py "caminho da outra pasta"
"""
import csv, json, os, sys, datetime
from pathlib import Path

PASTA_PADRAO = Path(os.environ.get("PASTA_NPS", "NPS"))  # defina a variável PASTA_NPS ou passe a pasta como argumento
MODELO = Path(__file__).with_name("index.html")
SAIDA = "Dashboard NPS.html"
fmt = lambda d: d.strftime("%d/%m/%Y %H:%M")


def mais_recente(pasta):
    achados = [p for p in pasta.iterdir()
               if p.is_file() and not p.name.startswith("~$") and p.suffix.lower() in (".xlsx", ".csv")]
    return max(achados, key=lambda p: p.stat().st_mtime) if achados else None


def ler_linhas(arq):
    if arq.suffix.lower() == ".csv":
        with open(arq, encoding="utf-8-sig", newline="") as f:
            return list(csv.DictReader(f))
    import openpyxl
    wb = openpyxl.load_workbook(arq, read_only=True, data_only=True)
    linhas = wb.worksheets[0].iter_rows(values_only=True)
    cab = next(linhas, None)
    if not cab:
        return []
    nomes, vistos = [], set()
    for i, c in enumerate(cab):
        n = str(c).strip() if c is not None else ""
        nomes.append(n if n and n not in vistos else None)
        vistos.add(n)
    saida = []
    for lin in linhas:
        reg = {}
        for n, v in zip(nomes, lin):
            if n is None or v is None:
                continue
            reg[n] = v.isoformat(sep=" ") if hasattr(v, "isoformat") else v
        if reg:
            saida.append(reg)
    return saida


def main():
    pasta = Path(sys.argv[1]) if len(sys.argv) > 1 else PASTA_PADRAO
    agora = fmt(datetime.datetime.now())
    dados = {"gerado": agora, "linhas": []}
    if not pasta.is_dir():
        dados["erro"] = f"Não encontrei a pasta {pasta}."
    else:
        arq = mais_recente(pasta)
        if not arq:
            dados["erro"] = "Não há nenhuma planilha (.xlsx ou .csv) na pasta NPS."
        else:
            dados["nome"] = arq.name
            dados["salvo"] = fmt(datetime.datetime.fromtimestamp(arq.stat().st_mtime))
            dados["linhas"] = ler_linhas(arq)
            if not dados["linhas"]:
                dados["erro"] = f"A planilha {arq.name} ainda não tem respostas."
    bloco = "<script>window.DADOS_FORMS=" + json.dumps(dados, ensure_ascii=False, default=str).replace("</", "<"+chr(92)+"/") + ";</script>\n"
    html = MODELO.read_text(encoding="utf-8")
    marca = "<script>\nconst FRASES="
    if marca not in html:
        sys.exit("Modelo do dashboard mudou: não achei o ponto de inserção dos dados.")
    html = html.replace(marca, bloco + marca, 1)
    destino = (pasta if pasta.is_dir() else MODELO.parent) / SAIDA
    destino.write_text(html, encoding="utf-8")
    print(f"Planilha: {dados.get('nome', '-')}")
    print(f"Respostas: {len(dados['linhas'])}")
    if dados.get("erro"):
        print("Aviso:", dados["erro"])
    print(f"Dashboard gravado em: {destino}")


if __name__ == "__main__":
    main()
