#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carga inicial do app do AvHoFlu Rio Tocantins a partir de um backup do CHN-4.

Lê um backup do Supabase do CHN-4 (lista de {key, value, updated_at}), descarta
tudo que é de outro meio ou da aba Garagem (removida deste app) e grava um
arquivo de carga com a MESMA forma do backup — pronto para subir no projeto
Supabase novo do navio.

Uso:
    # 1) gerar e conferir o arquivo de carga
    python3 scripts/migrar_rio_tocantins.py backups/backup-2026-07-17.json

    # 2) subir para o Supabase novo (só depois de conferir o arquivo)
    python3 scripts/migrar_rio_tocantins.py backups/backup-2026-07-17.json \
        --push https://SEU-PROJETO.supabase.co CHAVE_SERVICE_ROLE

Opções:
    --saida ARQ           caminho do arquivo de carga (padrão: backups/carga-inicial-rio-tocantins.json)
    --incluir-pessoal     migra também a aba Pessoal. Por padrão ela NÃO vem: o
                          backup traz os militares do Departamento de Logística
                          do CHN-4, que não são a tripulação do navio.
    --push URL CHAVE      faz upsert na tabela agenda_data do projeto informado.
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request

NAVIO = "AvHoFluRioTocantins"
HORAS_KEY = "tocantins"          # sufixo das chaves aa_horas_<key>_*
HORAS_OUTROS = ["nsampaio", "castelo", "xingu", "vega", "denebola", "regulus", "boto"]

# chaves que não têm razão de existir no app do navio
DESCARTE = {
    "__probe_readonly_test", "_meta", "teste_diag",
    "ag_config",                                    # config congelada no código desde 17/07/2026
    "aa_vtr_v1", "aa_vtr_cols_v1", "aa_vtr_cards_v1",   # aba Garagem, removida
}
PESSOAL_KEYS = {"aa_pessoal_v1", "aa_pessoal_cols_v1", "aa_pessoal_cards_v1",
                "aa_pessoal_cycles_v1", "aa_pessoal_ferias_v1", "aa_pessoal_ferias_2025_v1"}


def norm(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return "".join(c for c in s.lower() if c.isalnum())


def do_navio(valor):
    """True se o texto identifica o Rio Tocantins."""
    return "tocantins" in norm(valor)


# Designações dos OUTROS meios do CHN-4. Só formas de NOME DE NAVIO — nunca nomes de
# rio soltos ("Rio Xingu", "Baía de Guajará" aparecem em comissões do próprio Tocantins).
RX_OUTRO_MEIO = re.compile(
    r"nhog|garnier\s*sampaio|nhib|tenente\s*castelo"
    r"|avhoflu\s*rio\s*xingu|avb|balizador|denebola|regulus|lhai")


def outro_meio(texto):
    """True se o texto nomeia um meio que não é o Rio Tocantins."""
    n = norm_txt(texto)
    return bool(RX_OUTRO_MEIO.search(n)) and "tocantins" not in n


def norm_txt(s):
    s = unicodedata.normalize("NFD", str(s or ""))
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("backup")
    ap.add_argument("--saida", default="backups/carga-inicial-rio-tocantins.json")
    ap.add_argument("--incluir-pessoal", action="store_true")
    ap.add_argument("--push", nargs=2, metavar=("URL", "CHAVE"))
    args = ap.parse_args()

    registros = json.load(open(args.backup, encoding="utf-8"))
    orig = {r["key"]: r for r in registros}

    def carregar(k):
        try:
            return json.loads(orig[k]["value"])
        except Exception:
            return None

    saida, relatorio = {}, []

    def guardar(k, valor, nota):
        saida[k] = json.dumps(valor, ensure_ascii=False)
        relatorio.append((k, nota))

    # ── listas filtradas por campo de meio ──────────────────────────────────
    LISTAS = [("aa_navios_ships_v1", "nome"), ("aa_navios_comissoes_v1", "meio"),
              ("aa_clg_t1_v1", "meio"), ("aa_clg_t2_v1", "meio"),
              ("aa_clg_t3nav_v1", "meio"), ("aa_ppss_v1", "navio")]
    ids_vivos = set()          # ids de linha que sobreviveram (para histórico e auditoria)
    comissoes_vivas = set()
    for chave, campo in LISTAS:
        linhas = carregar(chave) or []
        mantidas = [r for r in linhas if do_navio(r.get(campo))]
        for r in mantidas:
            if r.get("id"):
                ids_vivos.add(r["id"])
        if chave == "aa_navios_comissoes_v1":
            comissoes_vivas = {r.get("id") for r in mantidas}
        guardar(chave, mantidas, "%d de %d linha(s)" % (len(mantidas), len(linhas)))

    # AvB Vega / Denébola eram embarcações do CHN-4 — a tabela nasce vazia aqui
    guardar("aa_clg_t3emb_v1", [], "zerada (embarcações eram do CHN-4)")

    # ── horas de motor: só o navio ──────────────────────────────────────────
    motores_vivos = set()
    for sufixo in ("v1", "cols_v1", "cards_v1"):
        k = "aa_horas_%s_%s" % (HORAS_KEY, sufixo)
        if k in orig:
            val = carregar(k)
            if sufixo == "v1":
                motores_vivos = {r.get("id") for r in (val or []) if r.get("id")}
            guardar(k, val, "mantida")
    for outro in HORAS_OUTROS:
        for sufixo in ("v1", "cols_v1", "cards_v1"):
            k = "aa_horas_%s_%s" % (outro, sufixo)
            if k in orig:
                relatorio.append((k, "DESCARTADA (outro meio)"))
    if "aa_horas_cols_v1" in orig:
        guardar("aa_horas_cols_v1", carregar("aa_horas_cols_v1"), "mantida (colunas padrão)")

    hist = carregar("aa_horas_readings_v1") or {}
    hist_ok = {k: v for k, v in hist.items() if k in motores_vivos}
    guardar("aa_horas_readings_v1", hist_ok, "%d de %d motor(es)" % (len(hist_ok), len(hist)))

    # ── histórico de estoque de CLG: chaveado pelo id da linha ──────────────
    est = carregar("aa_clg_estoque_hist_v1") or {}
    est_ok = {k: v for k, v in est.items()
              if any(k == i or k.startswith(i + "_") for i in ids_vivos)}
    guardar("aa_clg_estoque_hist_v1", est_ok, "%d de %d série(s)" % (len(est_ok), len(est)))

    # ── agenda: subsídios por meio ──────────────────────────────────────────
    ag_ships = carregar("ag_ships") or {}
    ag_ok = {k: v for k, v in ag_ships.items() if do_navio(k.split(":")[-1])}
    guardar("ag_ships", ag_ok, "%d de %d vínculo(s)" % (len(ag_ok), len(ag_ships)))

    ag_t = carregar("ag_tships") or {}
    ag_t_ok = {}
    for k, v in ag_t.items():
        meios = [m for m in (v or []) if do_navio(m)]
        if meios:
            ag_t_ok[k] = meios
    guardar("ag_tships", ag_t_ok, "%d de %d tarefa(s)" % (len(ag_t_ok), len(ag_t)))

    # ── cartões: linhas nomeadas por outro meio saem do cartão ──────────────
    for chave in ("aa_clg_cards_v1", "aa_navios_cards_v1"):
        cards = carregar(chave) or []
        cortados = 0
        for cd in cards:
            itens = cd.get("items") or []
            fica = [it for it in itens if not outro_meio(it.get("k"))]
            cortados += len(itens) - len(fica)
            cd["items"] = fica
        guardar(chave, cards, "%d cartão(ões), %d linha(s) de outro meio removida(s)"
                % (len(cards), cortados))

    # ── coluna "Navio" do PPSS: a lista suspensa só oferece o Rio Tocantins ──
    cols = carregar("aa_ppss_cols_v1") or []
    for c in cols:
        if c.get("key") == "navio" and c.get("options"):
            c["options"] = [o for o in c["options"] if do_navio(o)] or [NAVIO]
    guardar("aa_ppss_cols_v1", cols, 'opções da coluna "Navio" restritas ao navio')

    # ── agenda: tarefas e demandas avulsas de outro meio ────────────────────
    tarefas = carregar("ag_user") or []
    novas = []
    for t in tarefas:
        units = t.get("subsidioUnits")
        if isinstance(units, list):
            t["subsidioUnits"] = [u for u in units if do_navio(u)]
            if units and not t["subsidioUnits"]:
                continue          # era só para outros meios
        if outro_meio(t.get("tarefa")):
            continue
        novas.append(t)
    guardar("ag_user", novas, "%d de %d tarefa(s)" % (len(novas), len(tarefas)))

    spots = carregar("ag_spots") or []
    spots_ok = [s for s in spots
                if not (outro_meio(s.get("desc")) or outro_meio(s.get("from")))]
    guardar("ag_spots", spots_ok, "%d de %d demanda(s) avulsa(s)" % (len(spots_ok), len(spots)))

    # ── carimbos de última edição ───────────────────────────────────────────
    le = carregar("aa_lastedit_v1") or {}
    mortos = ["vtr_"] + ["horas_%s" % o for o in HORAS_OUTROS] + ["clg_t3emb"]
    le_ok = {k: v for k, v in le.items() if not any(k.startswith(p) for p in mortos)}
    if not args.incluir_pessoal:
        le_ok = {k: v for k, v in le_ok.items() if not k.startswith("pessoal")}
    guardar("aa_lastedit_v1", le_ok, "%d de %d carimbo(s)" % (len(le_ok), len(le)))

    # ── trilha de auditoria ─────────────────────────────────────────────────
    ESCOPO_MORTO = {"vtr_tbl", "clg_t3emb"} | {"horas_%s" % o for o in HORAS_OUTROS}
    aud = carregar("aa_audit_v1") or []

    def audit_ok(e):
        sc, rid = e.get("scope") or "", e.get("rowId") or ""
        if sc in ESCOPO_MORTO:
            return False
        if sc.startswith("pessoal") and not args.incluir_pessoal:
            return False
        if sc.startswith("card:"):
            return do_navio(sc) or not any(t in norm(sc) for t in
                                           ("sampaio", "castelo", "xingu", "vega", "denebola", "regulus", "boto"))
        if sc == "ppss_tbl":
            return do_navio(rid.split("#")[0])
        if sc in ("navios_comissao", "nv_comissao"):
            return rid in comissoes_vivas
        return rid in ids_vivos or do_navio(rid)

    aud_ok = [e for e in aud if audit_ok(e)]
    guardar("aa_audit_v1", aud_ok, "%d de %d evento(s)" % (len(aud_ok), len(aud)))

    # ── pessoal ─────────────────────────────────────────────────────────────
    for k in sorted(PESSOAL_KEYS):
        if k not in orig:
            continue
        if args.incluir_pessoal:
            guardar(k, carregar(k), "mantida (--incluir-pessoal)")
        else:
            relatorio.append((k, "DESCARTADA (militares do CHN-4, não do navio)"))

    # ── o resto passa inteiro ───────────────────────────────────────────────
    for k, r in orig.items():
        if k in saida or k in DESCARTE or k in PESSOAL_KEYS:
            continue
        if k.startswith("aa_horas_") or k in ("aa_audit_v1", "aa_lastedit_v1"):
            continue
        saida[k] = r["value"]
        relatorio.append((k, "mantida integralmente"))
    for k in sorted(DESCARTE):
        if k in orig:
            relatorio.append((k, "DESCARTADA"))

    # ── grava ───────────────────────────────────────────────────────────────
    destino = [{"key": k, "value": v} for k, v in sorted(saida.items())]
    os.makedirs(os.path.dirname(args.saida) or ".", exist_ok=True)
    with open(args.saida, "w", encoding="utf-8") as f:
        json.dump(destino, f, ensure_ascii=False, indent=1)

    print("Carga gerada em %s — %d chave(s)\n" % (args.saida, len(destino)))
    for k, nota in sorted(relatorio):
        print("  %-32s %s" % (k, nota))

    if args.push:
        url, chave = args.push
        alvo = url.rstrip("/") + "/rest/v1/agenda_data"
        corpo = json.dumps(destino, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(alvo, data=corpo, method="POST", headers={
            "apikey": chave, "Authorization": "Bearer " + chave,
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        })
        with urllib.request.urlopen(req) as resp:
            print("\nPush: HTTP %s — %d chave(s) gravada(s) em %s" % (resp.status, len(destino), alvo))


if __name__ == "__main__":
    sys.exit(main())
