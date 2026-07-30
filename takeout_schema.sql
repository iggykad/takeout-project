--
-- PostgreSQL database dump
--

\restrict f1MJAM8sYNorVL2V9SW6dVAvuy0tGgLzbeqDchdz98ggGvdCZ8Fkl3KLIHfFkBX

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

-- Started on 2026-07-30 12:07:45

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
-- TOC entry 219 (class 1259 OID 16593)
-- Name: customers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customers (
    customer_id bigint,
    customer_name character varying,
    tel_no character varying,
    address character varying
);


ALTER TABLE public.customers OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16596)
-- Name: menu_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.menu_items (
    item_id bigint,
    item_name character varying,
    price numeric,
    item_category text
);


ALTER TABLE public.menu_items OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16599)
-- Name: order_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.order_items (
    order_id bigint,
    item_id bigint,
    quantity integer
);


ALTER TABLE public.order_items OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16602)
-- Name: orders; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orders (
    order_id bigint,
    customer_id bigint,
    order_date date,
    is_delivery boolean
);


ALTER TABLE public.orders OWNER TO postgres;

--
-- TOC entry 4913 (class 0 OID 16593)
-- Dependencies: 219
-- Data for Name: customers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.customers (customer_id, customer_name, tel_no, address) FROM stdin;
1	Jon Dover	777-3909	47 Elmhead Ave.
2	Terry Klat	555-0284	101 Main St.
3	Garry Batch	555-0393	7 Frieda Rd
\.


--
-- TOC entry 4914 (class 0 OID 16596)
-- Dependencies: 220
-- Data for Name: menu_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.menu_items (item_id, item_name, price, item_category) FROM stdin;
1	Fried Rice	3.00	Rice
2	Fried Noodles	4.50	Noodles
5	Pho	7.00	Main
6	Udon Noodles	6.00	Main
7	Ramen Noodles	6.00	Main
8	Futo Maki x6	5.00	Main
9	Yangzhou Fried Rice	7.50	Rice
10	King Prawn Fried Rice	8.50	Rice
11	Chicken Chow Mein	8.50	Noodles
12	Chow Mein	7.50	Noodles
13	Chicken Lo Mein	8.50	Noodles
14	Lo Mein	6.50	Noodles
17	Chicken Fried Rice	9.50	Main
18	Pepsi Original 330ml	2.20	Drinks
19	Pepsi Max 330ml	2.20	Drinks
20	Monster Original 500ml	3.50	Drinks
21	Evian Still 500ml	2.50	Drinks
22	Tango Orange 330ml	2.30	Drinks
23	Tango Apple 330ml	2.30	Drinks
15	General Tso Chicken	10.00	Main
3	Summer Rolls	4.00	Starters
4	Spring Rolls	4.50	Starters
16	Egg Roll x4	2.50	Starters
24	Edamame	2.00	Starters
25	Vegetable Dumplings	2.80	Starters
26	Miso Soup	2.50	Starters
27	Hot+Sour Soup	3.80	Starters
28	Wonton	2.50	Starters
29	Tofu Ramen	3.80	Main
30	Vegetable Soup	5.50	Main
31	Mushroom Soup	5.20	Main
32	Beef Stew	8.50	Main
33	Pork Stew	7.80	Main
34	Beef Fried Rice	6.50	Rice
35	Chicken Fried Rice	6.80	Rice
36	Tofu Fried Rice	6.70	Rice
37	Brown Rice	2.40	Rice
38	Combination Fried Rice	11.00	Rice
39	Pork Fried Rice	3.80	Starters
40	Chinese Sticky Rice	9.90	Main
41	Chop Suey Noodles	6.50	Noodles
42	Wonton Noodle Soup	12.50	Main
43	Dan Dan Noodles	11.00	Noodles
44	Cold Sesame Noodles	7.90	Noodles
45	Shanghai Fried Noodles + Pork	9.50	Noodles
46	Shanghai Fried Noodles no Pork	9.00	Noodles
47	Shanghai Fried Noodles + Tofu	9.30	Noodles
\.


--
-- TOC entry 4915 (class 0 OID 16599)
-- Dependencies: 221
-- Data for Name: order_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.order_items (order_id, item_id, quantity) FROM stdin;
1	9	2
2	6	1
3	24	3
4	3	6
5	5	2
6	5	2
7	9	3
\.


--
-- TOC entry 4916 (class 0 OID 16602)
-- Dependencies: 222
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orders (order_id, customer_id, order_date, is_delivery) FROM stdin;
1	1	2026-07-22	t
2	2	2026-07-25	f
3	1	2026-07-27	t
4	2	2026-07-29	t
5	2	2026-07-29	f
6	1	2026-07-29	t
7	3	2026-07-29	t
\.


-- Completed on 2026-07-30 12:07:45

--
-- PostgreSQL database dump complete
--

\unrestrict f1MJAM8sYNorVL2V9SW6dVAvuy0tGgLzbeqDchdz98ggGvdCZ8Fkl3KLIHfFkBX

