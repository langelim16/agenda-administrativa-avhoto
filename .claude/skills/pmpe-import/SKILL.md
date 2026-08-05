---
name: pmpe-import
description: Importa as comissões em andamento/previstas (nunca passadas) dos PMPE em PDF para a tabela Comissões da aba CONDEF do artefato, gravando no Supabase. Usar quando o usuário pedir para ler/lançar/importar o PMPE ou atualizar a tabela Comissões do CONDEF.
---

# Importação de Comissões do PMPE (PDF → tabela Comissões do CONDEF)

Processo **independente** do `clg-import`: ambos leem os mesmos PDFs do
PMPE, mas o `clg-import` usa o período de comissão como insumo pra cruzar
com consumo de CLG (inclusive de meses passados). Aqui o objetivo é outro —
manter a tabela **Comissões** da aba CONDEF (`aa_navios_comissoes_v1`)
com o que está em andamento ou previsto. Não duplicar lógica de parsing de
PDF entre os dois: os dois usam `scripts/pmpe_extrair.py`.

Sem etapa de confirmação — a leitura do PMPE já se mostrou confiável.
Extrai e grava direto no Supabase.

**Permissão de escrita**: só incluir comissões novas e atualizar campos de
comissões já lançadas (ver "Duplicatas/atualizações" abaixo). Nunca remover
uma linha da tabela direto — se uma comissão lançada não aparecer mais no
PMPE mais recente (cancelada, incorporada a outro evento etc.), isso é
**sugestão** de remoção apresentada ao usuário, mediante aprovação explícita
antes de excluir.

## Fonte

PMPE em PDF em `1. leituras/2. pmpe/AAAA/PMPE MES-AAAA PARTE I.pdf` — usar
sempre o **PDF mais recente disponível** (é a fonte de verdade; PMPEs de
meses anteriores só interessam ao `clg-import`, não a este skill).
Extração: `python3 scripts/pmpe_extrair.py "1. leituras/2. pmpe" --desde AAAA-MM-DD`
(data de hoje — descarta comissões já encerradas; JSON no stdout, avisos de
parsing no stderr).

**Atenção**: o parser tropeça em páginas com dois eventos lado a lado
(colunas), podendo trocar campos de período/propósito entre eventos
vizinhos. Ler o PDF diretamente (`extract_text`) pra conferir os campos de
cada evento do Rio Tocantins antes de gravar — não copiar o JSON do script
sem olhar o texto bruto do evento correspondente.

## Sem filtro de data — lançar todas as comissões

**Não descartar nenhuma comissão do PMPE por causa da data.** Comissões já
encerradas fazem parte do histórico (o app as pinta de verde como "Concluída"
e tacha o texto), e há comissões no PMPE com data já passada que ainda não
ocorreram e podem ter a data retificada num PMPE seguinte. Extrair e conciliar
todas — o `status` automático (ver abaixo) marca "Concluída" as de data
passada; qualquer ajuste fino fica a cargo do usuário (e vira `manualFields`).

## Schema real da tabela (`aa_navios_comissoes_v1`)

Lida via REST do Supabase: `agenda_data(key,value,updated_at)`, linha
`key=aa_navios_comissoes_v1`, `value` = JSON array de objetos:

```json
{"id": "cms_pmpeNN_NN", "meio": "AvHoFluRioTocantins", "pmpe": "07.07",
 "comissao": "RIO AMAZONAS VIII (PARTE I)", "status": "Em andamento",
 "inicio": "22/06/2026", "fim": "24/07/2026",
 "localizacao": "Rio Amazonas",
 "clg": "ODM: 23.000L\nOL: 300L\nGAS: 100L",
 "manualFields": []}
```

Linhas antigas sem `manualFields` são tratadas como `[]` (nada travado).

- **`meio`**: sempre `AvHoFluRioTocantins` (chave curta do artefato, mapeada
  de "AvHoFlu Rio Tocantins" no PDF). É o único valor válido nesta tabela —
  linha com qualquer outro `meio` é erro de extração, não dado a gravar.
- **`pmpe`**: nº do evento (`NN.NN`).
- **`comissao`**: nome da operação/exercício (campo "OPERAÇÕES/EXERCÍCIO"
  do PDF), não o propósito.
- **`status`**: `"Em andamento"` (hoje ∈ [início, fim]), `"Prevista"` (hoje
  < início), ou `"Concluída"` (hoje > fim). Status como `"A ser adiada"` /
  `"Cancelada"` é **decisão operacional manual** do usuário, nunca inferir/
  sobrescrever automaticamente a partir de datas — o automático só alterna
  entre os três acima e nunca por cima de um status manual (`manualFields`).
- **`inicio`/`fim`**: string `DD/MM/AAAA` (não ISO).
- **`localizacao`**: campo "ÁREA/PORTO" do PDF.
- **`clg`**: texto multi-linha do consumo autorizado (campo "Consumo:" das
  observações), formato `"PRODUTO: valorL\n..."` — um produto por linha.
- **`id`**: `cms_pmpe` + nº do evento sem ponto, ex. `07.15` → `cms_pmpe07_15`
  (conferir padrão contra ids já existentes na tabela).
- **`manualFields`**: array de nomes de campo (`status`, `inicio`, `fim`,
  `localizacao`, `clg`, `comissao`, `meio`, `pmpe`) que o usuário editou
  manualmente pela tabela do app. Presença nesse array é **hierarquicamente
  superior** a qualquer dado do PMPE — ver "Duplicatas/atualizações".

## Escopo

**Somente o AvHoFlu Rio Tocantins**, igual ao `clg-import`. O PMPE continua
trazendo os eventos de todos os meios do CHN-4 — os dos demais navios são
**ignorados** (`MEIOS_ARTEFATO` em `scripts/pmpe_extrair.py` já filtra).
Eventos `ADM` não são comissão operativa — só lançar `PMPE`.

## Duplicatas/atualizações

Se um evento (`meio` + `pmpe`) já lançado aparecer de novo no PDF mais
recente com dados diferentes (datas retificadas, área alterada), o PDF mais
recente é a fonte de verdade para os campos que o usuário **nunca** editou
manualmente pelo app — atualizar a linha existente preservando o `id`.

**Regra hierárquica de `manualFields`**: antes de sobrescrever qualquer campo
de uma linha existente, checar `row.manualFields` (array de nomes de campo).
Se a chave do campo está em `manualFields`, **nunca sobrescrever** —
preservar o valor atual mesmo que o PDF traga algo diferente, sem exceção e
sem perguntar. A leitura do PMPE é puramente cadastral: só grava campos que o
usuário nunca tocou. Editar de volta um campo travado é decisão exclusiva do
usuário pela tabela do app — não há downgrade automático de `manualFields`
por este skill. Isso vale para todos os campos, não só `status`.

## Fluxo de execução

1. Rodar `scripts/pmpe_extrair.py` no PDF mais recente e conferir cada
   evento do Rio Tocantins contra o texto bruto do PDF (ver aviso acima
   sobre colunas).
2. Lançar todas as comissões (nenhuma é descartada por data — ver acima).
3. Ler `aa_navios_comissoes_v1` atual via REST do Supabase.
4. Gravar direto — adicionar linhas novas, atualizar as existentes
   (preservando `id` e nunca sobrescrevendo campos em `manualFields`, ver
   acima). Se alguma linha existente não corresponder a nenhum evento do
   PMPE mais recente, NÃO remover — listar como sugestão de remoção e
   aguardar aprovação.
5. Atualizar `aa_lastedit_v1` (chave `nv_comissao`) com timestamp atual —
   é o que faz o app mostrar "Última edição em…" na tabela Comissões.
6. Bump da chave `_meta` ao final para os dispositivos sincronizarem.

## Notas operacionais

- Ignorar locks (`~$*`) e tratar extensões case-insensitive.
- Pasta nova em `1. leituras/` = criar novo skill + mapeamento em
  `scripts/vigia_leituras.sh` + entrada WatchPaths no plist
  `~/Library/LaunchAgents/com.lucasangelim.agenda-leituras.plist` + reload.
