CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;

create table if not exists public.crawl (
	id uuid default uuid_generate_v4 (),
	url text,
	title text,
	lang char(2),
	html_content text,
	last_crawled text,
	last_updated text,
	primary key(id),
	unique(url, last_updated)
);

create table if not exists public.link (
	source_crawl_id uuid references public.crawl(id),
	destination_crawl_id uuid references public.crawl(id)
	primary key(source_crawl_id, destination_crawl_id),
);

create table if not exists public.chunk (
	id uuid default uuid_generate_v4 (),
	crawl_id uuid references public.crawl(id),
	title text,
	text_content text,
	primary key(id),
	unique(text_content)
);

create table if not exists public.token (
	id uuid default uuid_generate_v4 (),
	chunk_id uuid references public.chunk(id),
	tokens INTEGER[],
	encoding text default 'cl100k_base',
	primary key(id),
	unique(tokens)
);

create table if not exists public."text-embedding-ada-002" (
	id uuid default uuid_generate_v4 (),
	token_id uuid references public.token(id),
	embedding vector(1536),
	primary key(id),
	unique(embedding)
);

drop view documents;

create view documents as(
	select
		crawl.id as id,
		crawl.url as url,
		crawl.html_content as html_content,
		crawl.title as title,
		chunk.title as subtitle,
		chunk.text_content as content,
		embedding.embedding as embedding
	from crawl, chunk, token, "text-embedding-ada-002" as embedding
	where crawl.id = chunk.crawl_id
	and chunk.id = token.chunk_id
	and token.id = embedding.token_id
);

create or replace function match_documents (
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  content text,
  similarity float
)
language sql stable
as $$
  select
    documents.id,
    documents.content,
    1 - (documents.embedding <=> query_embedding) as similarity
  from documents
  where 1 - (documents.embedding <=> query_embedding) > match_threshold
  order by similarity desc
  limit match_count;
$$;