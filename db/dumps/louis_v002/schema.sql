--
-- PostgreSQL database dump
--

-- Dumped from database version 15.3
-- Dumped by pg_dump version 15.3

SELECT pg_catalog.set_config('search_path', '', false);

--
-- Name: louis_v002; Type: SCHEMA; Schema: -; Owner: -
--


CREATE SCHEMA louis_v002;

SET search_path to louis_v002, public;

create type score_type as enum('recency', 'traffic');
create type encoding as enum('cl100k_base');



--
-- Name: ada_002; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE ada_002 (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    token_id uuid,
    embedding vector(1536)
);


--
-- Name: chunk; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE chunk (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    crawl_id uuid,
    title text,
    text_content text
);


--
-- Name: crawl; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE crawl (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    url text,
    title text,
    lang character(2),
    html_content text,
    last_crawled text,
    last_updated text,
    last_updated_date date
);


--
-- Name: score; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE score (
    entity_id uuid,
    score double precision,
    score_type score_type
);


--
-- Name: scoring; Type: VIEW; Schema: louis_v002; Owner: -
--

CREATE VIEW scoring AS
 SELECT score.entity_id,
    avg(score.score) AS score
   FROM score
  GROUP BY score.entity_id;


--
-- Name: token; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE token (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    chunk_id uuid,
    tokens integer[],
    encoding encoding
);


--
-- Name: documents; Type: VIEW; Schema: louis_v002; Owner: -
--

CREATE VIEW documents AS
 SELECT crawl.id,
    crawl.url,
    crawl.html_content,
    crawl.title,
    chunk.title AS subtitle,
    chunk.text_content AS content,
    embedding.embedding,
    cardinality(token.tokens) AS tokens_count,
    crawl.last_updated,
    scoring.score
   FROM crawl,
    chunk,
    token,
    ada_002 embedding,
    scoring
  WHERE ((crawl.id = chunk.crawl_id) AND (chunk.id = token.chunk_id) AND (token.id = embedding.token_id) AND (crawl.id = scoring.entity_id));


--
-- Name: link; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE link (
    source_crawl_id uuid NOT NULL,
    destination_crawl_id uuid NOT NULL
);


--
-- Name: query; Type: TABLE; Schema: louis_v002; Owner: -
--

CREATE TABLE query (
    id uuid DEFAULT uuid_generate_v4() NOT NULL,
    query text,
    tokens integer[],
    embedding vector(1536),
    encoding text DEFAULT 'cl100k_base'::text,
    model text DEFAULT 'ada_002'::text
);

--
-- Name: match_documents(vector, double precision, integer); Type: FUNCTION; Schema: louis_v002; Owner: -
--

CREATE FUNCTION match_documents(query_embedding vector, match_threshold double precision, match_count integer) RETURNS TABLE(id uuid, url text, title text, subtitle text, content text, similarity double precision, tokens_count integer, last_updated text, score double precision)
    LANGUAGE sql
    AS $$
		SET ivfflat.probes = 8;
		with documents as (
			select documents.*, 1 - (documents.embedding operator(<=>) query_embedding) as similarity
			from documents
		)
		select
		    documents.id,
		    documents.url,
		    documents.title,
		    documents.subtitle,
		    documents.content,
		    similarity,
		    documents.tokens_count as tokens_count,
		    documents.last_updated as last_updated,
		    documents.score as score
	  	from documents
	  	where similarity > match_threshold
	  	order by (score + similarity) / 2 desc
	  	limit match_count;
	$$;
--
-- Name: ada_002 ada_002_pkey; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY ada_002
    ADD CONSTRAINT ada_002_pkey PRIMARY KEY (id);


--
-- Name: chunk chunk_pkey; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY chunk
    ADD CONSTRAINT chunk_pkey PRIMARY KEY (id);


--
-- Name: chunk chunk_text_content_key; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY chunk
    ADD CONSTRAINT chunk_text_content_key UNIQUE (text_content);


--
-- Name: crawl crawl_pkey; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY crawl
    ADD CONSTRAINT crawl_pkey PRIMARY KEY (id);


--
-- Name: crawl crawl_url_last_updated_key; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY crawl
    ADD CONSTRAINT crawl_url_last_updated_key UNIQUE (url, last_updated);


--
-- Name: link link_pkey; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_pkey PRIMARY KEY (source_crawl_id, destination_crawl_id);


--
-- Name: query query_pkey; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY query
    ADD CONSTRAINT query_pkey PRIMARY KEY (id);


--
-- Name: query query_tokens_key; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY query
    ADD CONSTRAINT query_tokens_key UNIQUE (tokens);


--
-- Name: token token_pkey; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_pkey PRIMARY KEY (id);


--
-- Name: token token_tokens_key; Type: CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_tokens_key UNIQUE (tokens);


--
-- Name: ada_002_embedding_idx; Type: INDEX; Schema: louis_v002; Owner: -
--

CREATE INDEX ada_002_embedding_idx ON ada_002 USING ivfflat (embedding vector_cosine_ops) WITH (lists='83');


--
-- Name: ada_002 ada_002_token_uuid_fkey; Type: FK CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY ada_002
    ADD CONSTRAINT ada_002_token_uuid_fkey FOREIGN KEY (token_id) REFERENCES token(id) ON DELETE CASCADE;


--
-- Name: chunk chunk_crawl_uuid_fkey; Type: FK CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY chunk
    ADD CONSTRAINT chunk_crawl_uuid_fkey FOREIGN KEY (crawl_id) REFERENCES crawl(id) ON DELETE CASCADE;


--
-- Name: link link_destination_crawl_id_fkey; Type: FK CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_destination_crawl_id_fkey FOREIGN KEY (destination_crawl_id) REFERENCES crawl(id) ON DELETE CASCADE;


--
-- Name: link link_source_crawl_id_fkey; Type: FK CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_source_crawl_id_fkey FOREIGN KEY (source_crawl_id) REFERENCES crawl(id) ON DELETE CASCADE;


--
-- Name: token token_chunk_uuid_fkey; Type: FK CONSTRAINT; Schema: louis_v002; Owner: -
--

ALTER TABLE ONLY token
    ADD CONSTRAINT token_chunk_uuid_fkey FOREIGN KEY (chunk_id) REFERENCES chunk(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

