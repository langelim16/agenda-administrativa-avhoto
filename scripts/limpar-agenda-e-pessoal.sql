-- ═══════════════════════════════════════════════════════════════════════════
-- Zera a aba Agenda e a aba Pessoal — os dados que vieram do CHN-4 e não
-- pertencem ao navio.
--
-- Rodar em: Painel Supabase → SQL Editor → New query → colar tudo → Run.
--
-- REVERSÍVEL: o backup de 2026-08-06 no repositório privado
-- agenda-rio-tocantins-backups tem tudo o que está sendo apagado aqui.
-- Para voltar atrás, use o --push do scripts/migrar_rio_tocantins.py com
-- aquele arquivo.
--
-- NÃO mexe em: CONDEF, CLG, Horas de Motores, PPSS, nem nas preferências
-- (tema, perfil, anos). Só Agenda e Pessoal.
-- ═══════════════════════════════════════════════════════════════════════════


-- ── ANTES: veja o que vai ser zerado ───────────────────────────────────────
-- Rode só este bloco primeiro, se quiser conferir os tamanhos atuais.
select key, length(value) as bytes
  from public.agenda_data
 where key in ('ag_base','ag_user','ag_status','ag_done','ag_hist','ag_nup',
               'ag_order','ag_edits','ag_subtasks','ag_ships','ag_tships',
               'ag_subsids','ag_instedit','ag_spots')
 order by key;


-- ── AGENDA ─────────────────────────────────────────────────────────────────
-- ag_base guarda o catálogo de tarefas recorrentes ({MT, MO}); ag_user, as
-- tarefas criadas à mão. O resto são mapas de estado por instância de tarefa
-- (status, concluídas, histórico, NUP, ordem, subtarefas, vínculo com meios).
-- ag_spots são as "Demandas do dia".
insert into public.agenda_data (key, value, updated_at) values
  ('ag_base',      '{"MT":[],"MO":[]}', now()),
  ('ag_user',      '[]',                now()),
  ('ag_spots',     '[]',                now()),
  ('ag_status',    '{}',                now()),
  ('ag_done',      '{}',                now()),
  ('ag_hist',      '{}',                now()),
  ('ag_nup',       '{}',                now()),
  ('ag_order',     '{}',                now()),
  ('ag_edits',     '{}',                now()),
  ('ag_subtasks',  '{}',                now()),
  ('ag_ships',     '{}',                now()),
  ('ag_tships',    '{}',                now()),
  ('ag_subsids',   '{}',                now()),
  ('ag_instedit',  '{}',                now())
on conflict (key) do update
   set value = excluded.value, updated_at = now();


-- ── PESSOAL ────────────────────────────────────────────────────────────────
-- ATENÇÃO: estas chaves NÃO existem hoje no banco do navio — a migração as
-- excluiu de propósito. Os militares do CHN-4 que aparecem na aba vêm do
-- cache do NAVEGADOR, não daqui: os dois apps moram no mesmo domínio
-- (langelim16.github.io) e por isso compartilham o localStorage.
--
-- Gravar array vazio aqui resolve de forma permanente: o app só consulta o
-- cache local quando o Supabase não tem a chave. Com a chave presente (mesmo
-- vazia), o cache do CHN-4 deixa de ser lido.
insert into public.agenda_data (key, value, updated_at) values
  ('aa_pessoal_v1',              '[]', now()),
  ('aa_pessoal_cards_v1',        '[]', now()),
  ('aa_pessoal_ferias_v1',       '[]', now()),
  ('aa_pessoal_ferias_2025_v1',  '[]', now()),
  ('aa_pessoal_ferias_2026_v1',  '[]', now())
on conflict (key) do update
   set value = excluded.value, updated_at = now();


-- ── Avisa os dispositivos para ressincronizar ──────────────────────────────
insert into public.agenda_data (key, value, updated_at)
values ('_meta', (extract(epoch from now()) * 1000)::bigint::text, now())
on conflict (key) do update
   set value = excluded.value, updated_at = now();


-- ── DEPOIS: confirme que zerou ─────────────────────────────────────────────
select key, value
  from public.agenda_data
 where key in ('ag_base','ag_user','ag_spots','ag_status','aa_pessoal_v1')
 order by key;
-- Esperado: ag_base = {"MT":[],"MO":[]} e os demais [] ou {}.
