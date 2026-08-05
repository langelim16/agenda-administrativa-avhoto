# Diretrizes

- Localize código com `graphify query "<pergunta>"`. Leia/grep arquivo bruto só depois disso, ou para editar linhas específicas.
- Rode `graphify update .` após alterar código.
- Responda direto e conciso, focado no código. Sem explicação não solicitada.
- Ao término de cada atualização, SEMPRE commite e pushe — e SOMENTE `index.html`: use `git add index.html`, nunca `git add -A`/`.`. Outros arquivos ficam fora do commit.

## Escopo: um único meio

Este artefato cobre **exclusivamente o AvHoFlu Rio Tocantins**. É um clone da
Agenda Administrativa do CHN-4 (`sftw-gestao-chn-4/sftw-gesta-chn-4`, privado),
com duas diferenças de fundo:

1. **Sem aba Garagem** — removida por completo (DOM, JS, modal de uso de
   viatura e as chaves `aa_vtr_*`).
2. **Um meio só** — os rosters de navios estão restritos a `AvHoFluRioTocantins`
   em `CFG0.subunidades`, `CLG_T3_NAV_ROSTER`, `PPSS_NAVIOS`, `HORAS_SHIP_LIST`,
   `CLG_IMP_SHIPS`, `IMP_SHIP_PATTERNS` e `PMPE_IMP_DISTINTIVO`. Ao mexer em
   qualquer um deles, não reintroduzir os demais meios.

As planilhas de origem (CLG, Horas, PPSS) e os PMPE **continuam chegando
consolidados do CHN-4**, com todos os meios. Por isso as referências a `"CHN-4"`
(coluna OM da planilha de CLG) e à aba `"CHN4"` (planilha de Horas) nos
importadores descrevem o formato do arquivo de entrada e **não devem ser
renomeadas** — os extratores em `scripts/` é que filtram as linhas do navio.

## Repositório e deploy

Um remote só: `origin` = `langelim16/agenda-administrativa-avhoto` (público),
que também serve o app pelo GitHub Pages. `git push` sem argumentos basta.

**Nunca commitar `backups/*.json` aqui.** O repositório é público, e os dumps
do Supabase contêm dados de pessoal e orçamento. Foi por isso que o repo do
CHN-4 é privado — este não tem esse tipo de conteúdo no histórico e deve
continuar assim.

## Backend

Projeto Supabase **próprio do navio**, separado do CHN-4. `SB_URL`/`SB_KEY`
ficam no topo do bloco de script em `index.html`. Nunca apontar para o projeto
do CHN-4: os dados dos dois apps se misturariam.

A carga inicial foi gerada por `scripts/migrar_rio_tocantins.py`, que filtra um
backup do CHN-4 para as linhas do Rio Tocantins.
