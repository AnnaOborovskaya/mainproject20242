Для создания таблиц в postgre:

CREATE TABLE users(
	id_user SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	avg_order_complete_time time without time zone,
	avg_day_orders INTEGER,	
	district text[],
	active_order jsonb DEFAULT '{}',
	avg_list_time text[],
    time_start INTEGER,
    time_end INTEGER,
	counter_ord INTEGER,
	time_start_work INTEGER
);

CREATE TABLE orders(
	id_order SERIAL PRIMARY KEY,
	name TEXT NOT NULL,
	district text,
	status INTEGER, 
	id_user INTEGER,
	FOREIGN KEY (id_user) REFERENCES users (id_user)
);
