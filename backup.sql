--
-- PostgreSQL database dump
--

\restrict jARDkBeVuZYPP28PopCcTlJLER65YsUCQdX3brkee7IxnfvmnKHQlabHBdVCAQT

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.1 (Ubuntu 18.1-1.pgdg24.04+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: items; Type: TABLE; Schema: public; Owner: khadija
--

CREATE TABLE public.items (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.items OWNER TO khadija;

--
-- Name: items_id_seq; Type: SEQUENCE; Schema: public; Owner: khadija
--

CREATE SEQUENCE public.items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.items_id_seq OWNER TO khadija;

--
-- Name: items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: khadija
--

ALTER SEQUENCE public.items_id_seq OWNED BY public.items.id;


--
-- Name: user_items; Type: TABLE; Schema: public; Owner: khadija
--

CREATE TABLE public.user_items (
    id integer NOT NULL,
    user_id integer,
    item_id integer
);


ALTER TABLE public.user_items OWNER TO khadija;

--
-- Name: user_items_id_seq; Type: SEQUENCE; Schema: public; Owner: khadija
--

CREATE SEQUENCE public.user_items_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_items_id_seq OWNER TO khadija;

--
-- Name: user_items_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: khadija
--

ALTER SEQUENCE public.user_items_id_seq OWNED BY public.user_items.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: khadija
--

CREATE TABLE public.users (
    id integer NOT NULL,
    name character varying,
    email character varying,
    password character varying
);


ALTER TABLE public.users OWNER TO khadija;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: khadija
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO khadija;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: khadija
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: items id; Type: DEFAULT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.items ALTER COLUMN id SET DEFAULT nextval('public.items_id_seq'::regclass);


--
-- Name: user_items id; Type: DEFAULT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.user_items ALTER COLUMN id SET DEFAULT nextval('public.user_items_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: items; Type: TABLE DATA; Schema: public; Owner: khadija
--

COPY public.items (id, name) FROM stdin;
1	pen
\.


--
-- Data for Name: user_items; Type: TABLE DATA; Schema: public; Owner: khadija
--

COPY public.user_items (id, user_id, item_id) FROM stdin;
1	\N	1
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: khadija
--

COPY public.users (id, name, email, password) FROM stdin;
7	kh	k@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$mnOfY.xHtGGXejoQgpahde$2UyLwLeyRqeQEWp4lb1PIQm5M0PzRuy
8	k	h@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$7v4jkx7A5QqcZQZuG6MVNe$9u80QnwLbsjPwAAise3.3.GRclaEAg2
9	kk	d@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$aVL7PZlXL8058GUvVCP3ou$6iMioqM7pqB2I3G8H9yrvmLJJk0hMgW
10	khaa	a@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$PIaSGkRFYJb7DTxsOtUGC.$vOZfm8/XZ/hxnVwaboQjKIr9ZtjjTP.
11	a	ali@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$NSgpgBRM7MM19QpGjr5jNe$vls.kZJK/O1qAn1.wqmTFy7/qGJVsWm
12	te	t@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$VLrkdectit/ecYIA8npgwe$v1HalrwpXSWopGt5dssIgXLEIHske1y
13	s	s@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$Ok6P4tIFzqm6EyprODgT8.$5PPdVy9YEc6cang.X64gJudpkU4wEwa
14	ss	ss@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$Pi2.XCpiVG4bujQ/QdP0..$f017Nup0LAQjzp5aKVNyvoLo1q2rvWG
15	str	str@gmail.com	$bcrypt-sha256$v=2,t=2b,r=12$87FqlEWDKDE5qvExw6EpJO$z1roHdKEc25QzT.O1aoRKlVmKUXVEje
\.


--
-- Name: items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khadija
--

SELECT pg_catalog.setval('public.items_id_seq', 1, true);


--
-- Name: user_items_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khadija
--

SELECT pg_catalog.setval('public.user_items_id_seq', 1, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: khadija
--

SELECT pg_catalog.setval('public.users_id_seq', 15, true);


--
-- Name: items items_pkey; Type: CONSTRAINT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.items
    ADD CONSTRAINT items_pkey PRIMARY KEY (id);


--
-- Name: user_items user_items_pkey; Type: CONSTRAINT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.user_items
    ADD CONSTRAINT user_items_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_items_id; Type: INDEX; Schema: public; Owner: khadija
--

CREATE INDEX ix_items_id ON public.items USING btree (id);


--
-- Name: ix_user_items_id; Type: INDEX; Schema: public; Owner: khadija
--

CREATE INDEX ix_user_items_id ON public.user_items USING btree (id);


--
-- Name: ix_users_email; Type: INDEX; Schema: public; Owner: khadija
--

CREATE UNIQUE INDEX ix_users_email ON public.users USING btree (email);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: khadija
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: ix_users_name; Type: INDEX; Schema: public; Owner: khadija
--

CREATE INDEX ix_users_name ON public.users USING btree (name);


--
-- Name: user_items user_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.user_items
    ADD CONSTRAINT user_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.items(id);


--
-- Name: user_items user_items_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: khadija
--

ALTER TABLE ONLY public.user_items
    ADD CONSTRAINT user_items_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict jARDkBeVuZYPP28PopCcTlJLER65YsUCQdX3brkee7IxnfvmnKHQlabHBdVCAQT

