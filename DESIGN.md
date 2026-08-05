---
name: Agenda Administrativa (CHN-4)
description: Painel operacional denso para gestão logística naval — a cor comunica situação, o resto fica neutro.
colors:
  action-blue: "#3f6cae"
  status-red: "#bb4f3f"
  status-amber: "#ad8226"
  status-teal: "#47906c"
  status-purple: "#7758c9"
  status-gold: "#9c7a2e"
  header-slate: "#2f3a44"
  ink-900: "#262a2e"
  ink-700: "#474d54"
  ink-500: "#767c83"
  text-2: "#3d444b"
  text-3: "#4e565f"
  border-200: "#e4e3df"
  border-strong: "#cdccc5"
  neutral-100: "#efeee9"
  neutral-50: "#f8f7f3"
  surface: "#ffffff"
typography:
  brand:
    fontFamily: "Josefin Sans, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    fontSize: "25px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "2px"
  headline:
    fontFamily: "Josefin Sans, sans-serif"
    fontSize: "16px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "1px"
  title:
    fontFamily: "Josefin Sans, sans-serif"
    fontSize: "14px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "normal"
  body:
    fontFamily: "Josefin Sans, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
    letterSpacing: "normal"
  label:
    fontFamily: "Josefin Sans, sans-serif"
    fontSize: "10px"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0.4px"
  data:
    fontFamily: "Josefin Sans, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    lineHeight: 1.3
    letterSpacing: "normal"
rounded:
  sm: "4px"
  md: "8px"
  lg: "12px"
  xl: "16px"
  pill: "99px"
spacing:
  xs: "4px"
  sm: "7px"
  md: "12px"
  lg: "18px"
components:
  button:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-2}"
    rounded: "{rounded.md}"
    padding: "7px 12px"
    typography: "{typography.data}"
  button-hover:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.action-blue}"
  button-primary:
    backgroundColor: "{colors.action-blue}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "7px 12px"
  chip:
    backgroundColor: "{colors.neutral-100}"
    textColor: "{colors.text-2}"
    rounded: "{rounded.pill}"
    padding: "4px 9px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink-900}"
    rounded: "{rounded.lg}"
    padding: "12px"
  table-header:
    backgroundColor: "{colors.neutral-100}"
    textColor: "{colors.text-2}"
    typography: "{typography.label}"
    padding: "7px 6px"
---

# Design System: Agenda Administrativa (CHN-4)

## 1. Overview

**Creative North Star: "O Quadro de Situação"**

A interface é um quadro de situação da OM: quem abre precisa ler o estado real — o que está vencido, o que está a vencer, o que está no prazo — na primeira passada de olho. A cor faz esse trabalho e quase só ele. O corpo do sistema é neutro e quieto (cinzas quentes sobre branco), e cada status pinta a linha, o chip ou o ponto com uma cor de significado fixo: vermelho é crítico, âmbar é atenção, verde é resolvido, azul é ação/andamento. Onde não há situação a comunicar, não há cor.

O sistema é denso por vocação. É uma ferramenta de trabalho para quem consolida dados de sete áreas todo dia, então prioriza informação útil por tela acima de respiro decorativo: tabelas com cabeçalho fixo, cartões compactos, uma barra de navegação lateral estreita e permanente. Densidade, porém, nunca vira o mar de células cinzas sem hierarquia que o produto explicitamente rejeita — o peso tipográfico (rótulos em maiúsculas espaçadas, títulos em 700, corpo em 400) e o uso disciplinado da cor de status dão relevo ao que importa.

O tom é institucional e preciso, sem enfeite de marketing e sem o ar engessado de sistema legado. Josefin Sans — uma única família, com peso variando de 300 a 700 — carrega tudo, de manchetes a dados. A confiança vem da clareza e da consistência tela a tela, não do estilo.

**Key Characteristics:**
- A cor comunica situação; o cromo neutro é o padrão de repouso.
- Densidade com hierarquia: muita informação, nunca com peso uniforme.
- Uma única família tipográfica em pesos variados.
- Azul de ação reservado à ação primária e à seleção corrente.
- Tema claro e escuro completos, mesma gramática visual.

## 2. Colors

Uma base neutra quente e silenciosa sobre a qual um léxico fixo de cores de status carrega todo o significado.

### Primary
- **Azul de Comando** (`#3f6cae`): a única cor de "ação" do sistema. Botão primário, item de navegação ativo, seleção corrente, anel de hover interno em cartões e linhas, comissões em andamento. Nunca é decoração — sua presença significa "aja aqui" ou "este é o item ativo".

### Secondary — o léxico de status
Cada cor tem um significado fixo e aparece tanto sólida (texto/borda) quanto como tinta de fundo via `color-mix` (linhas de tabela, chips).
- **Vermelho de Alerta** (`#bb4f3f`): crítico. Vencido, restrição impeditiva, cancelado, ação destrutiva.
- **Âmbar de Atenção** (`#ad8226`): a vencer, adiado, aviso — pendência que ainda dá tempo.
- **Verde de Resolvido** (`#47906c`): concluído, disponível, no prazo. Linhas concluídas ganham verde + tachado.
- **Roxo** (`#7758c9`): categoria auxiliar/agrupamento, usada com parcimônia.
- **Ouro** (`#9c7a2e`): marca ações de desfazer/histórico (undo) e itens editados.

### Neutral
- **Tinta 900** (`#262a2e`): texto principal (`--text`).
- **Tinta 700 / Texto-2 / Texto-3** (`#474d54` · `#3d444b` · `#4e565f`): rótulos, texto secundário, legendas — sempre escuros o bastante para leitura confortável, nunca cinza-claro decorativo.
- **Ardósia do Cabeçalho** (`#2f3a44`): fundo do cabeçalho principal e da navegação; ancora a identidade naval.
- **Bordas** (`#e4e3df` padrão · `#cdccc5` forte): traços finos de 1–1.5px que separam sem pesar.
- **Neutros de superfície** (`#f8f7f3` fundo · `#efeee9` fundo de cabeçalho de tabela/chip · `#ffffff` superfície): a colcha quente e quieta sobre a qual tudo repousa.

### Named Rules
**A Regra do Silêncio Neutro.** Se um elemento não comunica situação nem ação, ele é neutro. Cor com significado (status ou azul de ação) nunca é usada para "dar vida" a um componente inerte.

**A Regra do Léxico Fixo.** Vermelho = crítico, âmbar = atenção, verde = resolvido, azul = ação/atual. Um mesmo tom nunca significa duas coisas em telas diferentes. O usuário aprende o código de cores uma vez.

## 3. Typography

**Família única:** Josefin Sans (com fallback `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`). Pesos embutidos: 300, 400, 700. Não há pareamento display/corpo — e não deve haver; o mono também aponta para Josefin Sans.

**Character:** uma geométrica humanista de contadores altos, discreta em corpo pequeno e com boa presença em maiúsculas espaçadas. A hierarquia nasce de peso, tamanho e caixa — não de troca de família.

### Hierarchy
- **Brand** (700, 25px, `letter-spacing: 2px`, MAIÚSCULAS): título da OM no cabeçalho ardósia. Aparece uma vez.
- **Headline** (700, 16px, `letter-spacing: 1px`, MAIÚSCULAS): títulos de seção em destaque (ex.: cabeçalho da spotlight).
- **Title** (700, 13–14px): títulos de cartão e de tabela, centrados.
- **Body** (400–500, 14px, `line-height: 1.5`): texto de conteúdo e controles de formulário. Base do sistema.
- **Label** (600–700, 9–10px, `letter-spacing: 0.3–0.5px`, MAIÚSCULAS): cabeçalhos de coluna (`th`), rótulos de campo, kickers de seção. O rótulo em caixa alta é a assinatura tipográfica do sistema.
- **Data** (600, 10–11px): valores numéricos e códigos densos em tabelas.

### Named Rules
**A Regra da Etiqueta Maiúscula.** Rótulos estruturais (colunas, campos, seções) vão em maiúsculas espaçadas de peso 600–700, tamanho 9–10px. É o que dá relevo à densidade sem recorrer a mais uma cor.

## 4. Elevation

O sistema é essencialmente plano. Superfícies brancas separam-se do fundo quente por bordas finas (1–1.5px), não por sombra. As sombras existem, mas são leves e situacionais: uma sombra `xs` quase imperceptível assenta tabelas e botões, e a `lg` só aparece em camadas realmente flutuantes (drawer, menus dropdown).

O gesto de profundidade característico não é sombra e sim um **anel interno azul**: cartões, linhas clicáveis e itens de lista respondem ao hover com `box-shadow: 0 0 0 2px var(--c-blue) inset` — foco sem deslocamento, coerente com a densidade.

### Shadow Vocabulary
- **xs** (`0 1px 2px rgba(38,42,46,.06)`): repouso de tabelas, botões e cartões. Quase só um assentamento.
- **sm** (`0 2px 8px rgba(38,42,46,.09)`): hover de tarefas/cartões que sobem um degrau.
- **lg** (`0 14px 40px rgba(38,42,46,.13)`): camadas flutuantes — drawer lateral e menus dropdown.

### Named Rules
**A Regra do Anel Interno.** Estado de hover/foco em elementos clicáveis é comunicado por anel azul interno de 2px, não por elevação ou deslocamento. A grade não "pula".

## 5. Components

Componentes densos e funcionais: compactos, de cromo mínimo, com feedback discreto. A mesma gramática se repete tela a tela — mesma forma de botão, mesmo vocabulário de controle.

### Buttons
- **Shape:** cantos suaves de 8px (`--r-md`); ações em pílula usam raio 99px.
- **Default (ghost):** superfície branca, texto `text-2`, borda 1.5px, sombra `xs`, `padding: 7px 12px`, peso 500. Hover: borda e texto viram azul de comando.
- **Primary:** fundo azul de comando, texto branco, borda transparente, sombra azul suave (`0 2px 8px rgba(65,97,140,.25)`). Hover: `filter: brightness(1.07)`.
- **Undo:** borda e texto em ouro; hover com fundo âmbar-claro. Marca visualmente a família desfazer/histórico.

### Chips
- **Style:** pílula (raio 99px), fundo `neutral-100`, texto `text-2`, borda 1.5px, peso 700, 9.5px em maiúsculas.
- **State:** selecionado adota o azul de comando (ou a cor de status pertinente); não-selecionado fica neutro.

### Cards / Containers
- **Corner Style:** 12px (`--r-lg`).
- **Background:** superfície branca sobre fundo `neutral-50`.
- **Shadow Strategy:** plano no repouso (sombra `xs`); hover usa o anel interno azul (ver Elevation), não elevação.
- **Border:** 1–1.5px `border-200`.
- **Internal Padding:** 10–12px.
- **Marcador de categoria:** tarefas usam uma tarja lateral colorida (`border-left: 4px`) como código de tipo (azul = diverso, âmbar = navio) — marcador funcional de categoria, não ornamento; restrito a este componente.

### Inputs / Fields
- **Style:** fundo superfície ou `neutral-50`, borda 1–1.5px `border-200`, raio 4–8px, herdam a família e o corpo do texto.
- **Focus:** deslocamento de borda para o azul de comando.
- **Densidade:** campos de célula de tabela encolhem para 10–11px e padding mínimo, mantendo alvo clicável de linha inteira.

### Navigation
- **Rail lateral fixo** sobre a ardósia do cabeçalho: ícone acima de rótulo, 70px de largura. Item em repouso é branco a 55% de opacidade; ativo ganha fundo azul de comando e texto branco pleno.
- **Segmentos/abas internas** em pílula ou aba, rótulo em maiúsculas 11px, item ativo destacado; corrente segue o azul de comando.

### Tabelas (componente-assinatura)
Cabeçalho fixo (`position: sticky`) em `neutral-100` com rótulos-etiqueta em maiúsculas. Corpo denso (padding 7px, corpo 13–14px). O relevo vem das **tintas de linha de status**: `row-ok`/`row-warn`/`row-bad`, `row-vencido`/`row-avencer`, `comissao-andamento`, todas geradas por `color-mix` da cor de status sobre transparente. Linha clicável responde com leve tinta azul no hover.

**Legenda sempre acima dos dados**, nunca abaixo: a legenda decodifica as cores, então precisa ser lida *antes* do conteúdo — embaixo ela só é encontrada depois que o leitor já tropeçou na cor que não entendeu. Ordem canônica da seção: cabeçalho (título + toolbar) → legenda → grade de dados. A regra vale para **tabelas, calendários, timelines e heatmaps** — qualquer grade nova nasce assim. Referências: `.comissao-legend`, `.ferias-legend`, `.cal-legend`, `.tl-legend-top`, `.hm-legend`.

Exceção: **gráficos** (pizza, linha) mantêm a legenda junto à figura (abaixo ou ao lado). Ali ela não é chave de leitura prévia e sim rótulo das séries, e subi-la empurraria o gráfico para baixo sem ganho.

**Frase explicativa (`.dt-note`) também acima**, pela mesma razão: nota de rodapé que define o que a coluna mede ou de onde vem o número chega tarde demais embaixo — quem leu a tabela já interpretou errado. Ordem completa da seção:

```
cabeçalho (título + toolbar)
legenda            ← quando houver
.dt-note           ← frase explicativa, sempre depois da legenda
grade de dados
```

Use a classe `.dt-note`, não estilo inline. Distinga de **estado-vazio** ("Nenhum lançamento registrado ainda"), que continua dentro da grade, e de **anotação de cartão**, que fica colada ao número que ressalva.

## 6. Do's and Don'ts

### Do:
- **Do** deixar a cor comunicar situação: use o léxico fixo (vermelho crítico, âmbar atenção, verde resolvido, azul ação/atual) e nada além disso para status.
- **Do** manter o azul de comando (`#3f6cae`) restrito a ação primária, item ativo e seleção corrente.
- **Do** dar relevo à densidade com peso tipográfico e rótulos em maiúsculas espaçadas, não com mais cor.
- **Do** usar bordas finas (1–1.5px) e o anel interno azul de hover para separar e destacar; mantenha as superfícies planas.
- **Do** manter uma única família (Josefin Sans) em todos os elementos, variando peso e caixa.
- **Do** garantir contraste sólido: texto de conteúdo na faixa `ink-900`/`text-2`, nunca cinza-claro decorativo (o app roda em PCs variados da OM).

### Don't:
- **Don't** deixar a interface virar planilha crua sem hierarquia — um mar de células cinzas de peso uniforme onde achar o dado depende de vasculhar. Densidade sim, ausência de hierarquia não.
- **Don't** usar cor de status ou azul de ação para "dar vida" a um elemento inerte que não comunica situação.
- **Don't** dar dois significados ao mesmo tom em telas diferentes; o código de cores é aprendido uma vez.
- **Don't** introduzir gradientes, brilhos ou cara de site/startup chamativo — nem o ar engessado de sistema governamental legado.
- **Don't** parear uma segunda família tipográfica nem usar fonte de display em rótulos, botões ou dados.
- **Don't** adotar a tarja lateral colorida (`border-left`) fora do marcador de categoria de tarefas; não usá-la como enfeite em cartões, alertas ou listas.
