create database mobkoi;

\c mobkoi;
create table if not exists public.exchange_rates (
    base_code varchar(16) not null,
    target_code varchar(16) not null,
    rate float not null,
    unix_update integer not null,
    utc_update varchar(128) not null
);

create table if not exists public.binance_tickers (
    symbol varchar(16) not null,
    price float not null,
    created_at timestamp default now()
);
