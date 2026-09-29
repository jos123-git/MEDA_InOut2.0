--
-- PostgreSQL database dump
--

-- Dumped from database version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)
-- Dumped by pg_dump version 14.10 (Ubuntu 14.10-0ubuntu0.22.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: userrole; Type: TYPE; Schema: public; Owner: user
--

CREATE TYPE public.userrole AS ENUM (
    'ADMIN',
    'HR',
    'EMPLOYEE'
);


ALTER TYPE public.userrole OWNER TO "user";

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: activity_logs; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.activity_logs (
    id integer NOT NULL,
    user_id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    keyboard_count integer DEFAULT 0,
    mouse_count integer DEFAULT 0,
    idle_duration double precision DEFAULT 0.0,
    screenshot_path character varying(500),
    productivity_score double precision DEFAULT 0.0,
    is_suspicious boolean DEFAULT false,
    alert_message text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.activity_logs OWNER TO "user";

--
-- Name: activity_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.activity_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.activity_logs_id_seq OWNER TO "user";

--
-- Name: activity_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.activity_logs_id_seq OWNED BY public.activity_logs.id;


--
-- Name: attendance_logs; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.attendance_logs (
    id integer NOT NULL,
    user_id integer NOT NULL,
    time_in timestamp without time zone NOT NULL,
    time_out timestamp without time zone,
    duration_minutes integer,
    status character varying(50) DEFAULT 'present'::character varying,
    notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.attendance_logs OWNER TO "user";

--
-- Name: attendance_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.attendance_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.attendance_logs_id_seq OWNER TO "user";

--
-- Name: attendance_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.attendance_logs_id_seq OWNED BY public.attendance_logs.id;


--
-- Name: employees; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.employees (
    id character varying NOT NULL,
    name character varying,
    role character varying,
    status character varying,
    last_sync timestamp without time zone
);


ALTER TABLE public.employees OWNER TO postgres;

--
-- Name: leave_requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.leave_requests (
    id integer NOT NULL,
    employee_id character varying,
    leave_type character varying,
    status character varying,
    start_date timestamp without time zone,
    end_date timestamp without time zone
);


ALTER TABLE public.leave_requests OWNER TO postgres;

--
-- Name: leave_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.leave_requests_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.leave_requests_id_seq OWNER TO postgres;

--
-- Name: leave_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.leave_requests_id_seq OWNED BY public.leave_requests.id;


--
-- Name: logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.logs (
    id integer NOT NULL,
    employee_id character varying,
    action character varying,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.logs OWNER TO postgres;

--
-- Name: logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.logs_id_seq OWNER TO postgres;

--
-- Name: logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.logs_id_seq OWNED BY public.logs.id;


--
-- Name: productivity_metrics; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.productivity_metrics (
    id integer NOT NULL,
    user_id integer NOT NULL,
    date date NOT NULL,
    total_hours double precision,
    average_productivity double precision,
    suspicious_counts integer DEFAULT 0,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.productivity_metrics OWNER TO "user";

--
-- Name: productivity_metrics_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.productivity_metrics_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.productivity_metrics_id_seq OWNER TO "user";

--
-- Name: productivity_metrics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.productivity_metrics_id_seq OWNED BY public.productivity_metrics.id;


--
-- Name: session_data; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.session_data (
    id integer NOT NULL,
    user_id integer NOT NULL,
    session_data jsonb,
    synced boolean DEFAULT false,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    synced_at timestamp without time zone
);


ALTER TABLE public.session_data OWNER TO "user";

--
-- Name: session_data_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.session_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.session_data_id_seq OWNER TO "user";

--
-- Name: session_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.session_data_id_seq OWNED BY public.session_data.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: user
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    full_name character varying(255) NOT NULL,
    role character varying(50) DEFAULT 'employee'::character varying NOT NULL,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.users OWNER TO "user";

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: user
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO "user";

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: user
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: activity_logs id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.activity_logs ALTER COLUMN id SET DEFAULT nextval('public.activity_logs_id_seq'::regclass);


--
-- Name: attendance_logs id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.attendance_logs ALTER COLUMN id SET DEFAULT nextval('public.attendance_logs_id_seq'::regclass);


--
-- Name: leave_requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests ALTER COLUMN id SET DEFAULT nextval('public.leave_requests_id_seq'::regclass);


--
-- Name: logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs ALTER COLUMN id SET DEFAULT nextval('public.logs_id_seq'::regclass);


--
-- Name: productivity_metrics id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.productivity_metrics ALTER COLUMN id SET DEFAULT nextval('public.productivity_metrics_id_seq'::regclass);


--
-- Name: session_data id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.session_data ALTER COLUMN id SET DEFAULT nextval('public.session_data_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: activity_logs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.activity_logs (id, user_id, "timestamp", keyboard_count, mouse_count, idle_duration, screenshot_path, productivity_score, is_suspicious, alert_message, created_at) FROM stdin;
\.


--
-- Data for Name: attendance_logs; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.attendance_logs (id, user_id, time_in, time_out, duration_minutes, status, notes, created_at) FROM stdin;
\.


--
-- Data for Name: employees; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.employees (id, name, role, status, last_sync) FROM stdin;
EMP-001	Mark Espedido	Lead	Offline	2026-04-13 16:16:47.904324
EMP-002	John Martin Tiu	UI/UX	Offline	2026-04-13 16:16:47.904327
EMP-003	Jos Fernan Alpuerto	Backend	Offline	2026-04-13 16:16:47.904327
EMP-004	Ed Josh Isaac Sayson	QA	Offline	2026-04-13 16:16:47.904328
EMP-005	Paolo Romero	Documentation	Offline	2026-04-13 16:23:31.325808
\.


--
-- Data for Name: leave_requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.leave_requests (id, employee_id, leave_type, status, start_date, end_date) FROM stdin;
\.


--
-- Data for Name: logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.logs (id, employee_id, action, "timestamp") FROM stdin;
\.


--
-- Data for Name: productivity_metrics; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.productivity_metrics (id, user_id, date, total_hours, average_productivity, suspicious_counts, created_at) FROM stdin;
\.


--
-- Data for Name: session_data; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.session_data (id, user_id, session_data, synced, created_at, synced_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: user
--

COPY public.users (id, username, email, hashed_password, full_name, role, is_active, created_at, updated_at) FROM stdin;
1	hr	hr@company.com	$pbkdf2-sha256$29000$tjYmRCjlHANAaC3lvJfyng$eV3GEV3Te/VWYTYVm1LO0YpPrXN7fxYP7LHvbieHzcc	HR Manager	HR	t	2026-03-31 09:15:09.626679	2026-03-31 09:15:09.587252
2	emp1	emp1@company.com	$pbkdf2-sha256$29000$FeL8n1MqpfT.n/NeC0GI0Q$ynSUpIox3YbfQPAUShhwrzQZ.IjCUojq.iAU1VdbC.k	Employee One	EMPLOYEE	t	2026-03-31 09:15:09.626683	2026-03-31 09:15:09.587252
4	admin	demo@meda.test	$2b$12$tbWpr6C7l3lFSkt.RDX8KOeLjeVk8OxRyKnYQUGvZx5wlgeEajfbq	Mark Espedido	Admin	t	2026-04-11 09:16:21.779888	2026-04-11 09:16:21.779888
\.


--
-- Name: activity_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.activity_logs_id_seq', 1, false);


--
-- Name: attendance_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.attendance_logs_id_seq', 1, false);


--
-- Name: leave_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.leave_requests_id_seq', 1, false);


--
-- Name: logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.logs_id_seq', 1, false);


--
-- Name: productivity_metrics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.productivity_metrics_id_seq', 1, false);


--
-- Name: session_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.session_data_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: user
--

SELECT pg_catalog.setval('public.users_id_seq', 4, true);


--
-- Name: activity_logs activity_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_pkey PRIMARY KEY (id);


--
-- Name: attendance_logs attendance_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.attendance_logs
    ADD CONSTRAINT attendance_logs_pkey PRIMARY KEY (id);


--
-- Name: employees employees_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.employees
    ADD CONSTRAINT employees_pkey PRIMARY KEY (id);


--
-- Name: leave_requests leave_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests
    ADD CONSTRAINT leave_requests_pkey PRIMARY KEY (id);


--
-- Name: logs logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.logs
    ADD CONSTRAINT logs_pkey PRIMARY KEY (id);


--
-- Name: productivity_metrics productivity_metrics_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.productivity_metrics
    ADD CONSTRAINT productivity_metrics_pkey PRIMARY KEY (id);


--
-- Name: productivity_metrics productivity_metrics_user_id_date_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.productivity_metrics
    ADD CONSTRAINT productivity_metrics_user_id_date_key UNIQUE (user_id, date);


--
-- Name: session_data session_data_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.session_data
    ADD CONSTRAINT session_data_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: idx_activity_suspicious; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_activity_suspicious ON public.activity_logs USING btree (is_suspicious);


--
-- Name: idx_activity_timestamp; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_activity_timestamp ON public.activity_logs USING btree ("timestamp");


--
-- Name: idx_activity_user_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_activity_user_id ON public.activity_logs USING btree (user_id);


--
-- Name: idx_attendance_time_in; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_attendance_time_in ON public.attendance_logs USING btree (time_in);


--
-- Name: idx_attendance_user_id; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_attendance_user_id ON public.attendance_logs USING btree (user_id);


--
-- Name: idx_productivity_user_date; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_productivity_user_date ON public.productivity_metrics USING btree (user_id, date);


--
-- Name: idx_session_data_synced; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_session_data_synced ON public.session_data USING btree (synced);


--
-- Name: idx_users_email; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_users_email ON public.users USING btree (email);


--
-- Name: idx_users_username; Type: INDEX; Schema: public; Owner: user
--

CREATE INDEX idx_users_username ON public.users USING btree (username);


--
-- Name: ix_employees_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_employees_id ON public.employees USING btree (id);


--
-- Name: ix_logs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_logs_id ON public.logs USING btree (id);


--
-- Name: activity_logs activity_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.activity_logs
    ADD CONSTRAINT activity_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: attendance_logs attendance_logs_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.attendance_logs
    ADD CONSTRAINT attendance_logs_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: leave_requests leave_requests_employee_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.leave_requests
    ADD CONSTRAINT leave_requests_employee_id_fkey FOREIGN KEY (employee_id) REFERENCES public.employees(id);


--
-- Name: productivity_metrics productivity_metrics_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.productivity_metrics
    ADD CONSTRAINT productivity_metrics_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: session_data session_data_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: user
--

ALTER TABLE ONLY public.session_data
    ADD CONSTRAINT session_data_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

