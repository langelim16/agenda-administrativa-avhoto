-- ═══════════════════════════════════════════════════════════════════════════
-- Schema inicial do backend do AvHoFlu Rio Tocantins.
-- Rodar UMA VEZ num projeto Supabase novo e vazio:
--   Painel Supabase → SQL Editor → New query → colar tudo → Run.
--
-- Já nasce com a RLS fechada (só usuário logado lê e escreve). Por isso a
-- ordem importa: rode este script, crie sua conta em Authentication, marque-a
-- como admin (bloco 4 no fim), e só então carregue os dados e abra o app.
-- ═══════════════════════════════════════════════════════════════════════════


-- ── 1) agenda_data — o banco do app inteiro ────────────────────────────────
-- Modelo chave-valor: cada chave (ag_*, aa_*) é um documento independente, o
-- que evita que abas diferentes disputem a mesma linha.
--
-- ATENÇÃO: `updated_at` é gravado PELO APP, nunca por trigger. O app usa esse
-- campo como trava de concorrência (envia `updated_at=eq.<valor conhecido>` no
-- PATCH e desiste se outro dispositivo escreveu antes). Um trigger de
-- "atualizar updated_at automaticamente" QUEBRARIA essa proteção — não criar.
create table if not exists public.agenda_data (
  key        text primary key,
  value      text,
  updated_at timestamptz not null default now()
);

alter table public.agenda_data enable row level security;

-- Só logado lê e escreve. Sem policy de DELETE: apagar linha é só pelo SQL
-- Editor, de propósito — o app nunca remove um documento inteiro.
drop policy if exists "auth_select" on public.agenda_data;
drop policy if exists "auth_insert" on public.agenda_data;
drop policy if exists "auth_update" on public.agenda_data;

create policy "auth_select" on public.agenda_data
  for select to authenticated using (true);
create policy "auth_insert" on public.agenda_data
  for insert to authenticated with check (true);
create policy "auth_update" on public.agenda_data
  for update to authenticated using (true) with check (true);


-- ── 2) app_roles — quem é admin ────────────────────────────────────────────
-- O papel é SEMPRE atribuído explicitamente aqui. Nunca sai de user_metadata:
-- de lá o próprio usuário conseguiria se autopromover a admin.
create table if not exists public.app_roles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  role    text not null default 'operador' check (role in ('admin','operador'))
);

alter table public.app_roles enable row level security;

-- Todo logado LÊ os papéis (o app usa para mostrar/esconder a aba CONFIG USERS).
-- Nenhuma policy de escrita: mudar papel só por SQL ou pela Edge Function admin.
drop policy if exists "auth_read_roles" on public.app_roles;
create policy "auth_read_roles" on public.app_roles
  for select to authenticated using (true);


-- ── 3) audit_log — trilha de auditoria com autor ───────────────────────────
create table if not exists public.audit_log (
  id         bigint generated always as identity primary key,
  author     uuid references auth.users(id),
  action     text not null,
  target     text,
  detail     text,
  created_at timestamptz not null default now()
);

create index if not exists audit_log_created_idx on public.audit_log (created_at desc);

alter table public.audit_log enable row level security;

drop policy if exists "auth_read_audit" on public.audit_log;
drop policy if exists "auth_insert_own_audit" on public.audit_log;

create policy "auth_read_audit" on public.audit_log
  for select to authenticated using (true);

-- Só dá para inserir linha com o próprio autor — não se forja autoria.
create policy "auth_insert_own_audit" on public.audit_log
  for insert to authenticated with check (author = auth.uid());

-- Sem UPDATE/DELETE pelo client: a auditoria é imutável pela aplicação.


-- ── 4) TE MARCAR COMO ADMIN ────────────────────────────────────────────────
-- Rodar DEPOIS de criar sua conta em Authentication → Users → Add user.
-- Descomente e troque o e-mail:
--
-- insert into public.app_roles (user_id, role)
-- select id, 'admin' from auth.users where email = 'SEU-EMAIL@AQUI'
-- on conflict (user_id) do update set role = 'admin';


-- ── Conferência ────────────────────────────────────────────────────────────
-- Sem login, a leitura tem que vir vazia ou 401. Se vier dado, a RLS não pegou:
--   curl -sS "https://SEU-PROJETO.supabase.co/rest/v1/agenda_data?select=key&limit=1" \
--     -H "apikey: SUA_CHAVE_PUBLISHABLE"
