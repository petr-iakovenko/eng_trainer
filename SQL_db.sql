-- CREATE SCHEMA IF NOT exists english_words;
-- drop table if exists english_words.eng_to_rus_words;
-- drop table if exists english_words.rus_to_eng_words;

create table if not exists english_words.eng_to_rus_words (
	id SERIAL PRIMARY key ,
	word_en varchar unique,
	word_ru varchar,
	countet_try bigint default 0,
	counter_forgot bigint default 0,
	flag_forgot int 
	);

create table if not exists english_words.rus_to_eng_words (
	id SERIAL PRIMARY key ,
	word_ru varchar unique,
	word_en varchar,
	countet_try bigint default 0,
	counter_forgot bigint default 0,
	flag_forgot int 
	);