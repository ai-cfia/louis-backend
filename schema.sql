CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

create table if not exists public.crawl (
	id uuid default uuid_generate_v4 (),
	url text,
	title text,
	lang char(2),
	html_content text,
	last_crawled text,
	last_updated text,
	primary key(id),
	unique(url)
);

create table if not exists public.chunk (
	id uuid default uuid_generate_v4 (),
	crawl_uuid uuid references public.crawl(id),
	title text,
	text_content text,
	text_content_hash text,
	primary key(id),
	unique(text_content_hash)
);
