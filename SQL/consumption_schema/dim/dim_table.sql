-- region dimension
use schema consumption;
create or replace sequence region_dim_seq start = 1 increment = 1;
create or replace transient table region_dim(
    region_id_pk number primary key,
    Country text, 
    Region text,
    isActive text(1)
);

-- product dimension
use schema consumption;
create or replace sequence product_dim_seq start = 1 increment = 1;
create or replace transient table product_dim(
    product_id_pk number primary key,
    Mobile_key text,
    Brand text, 
    Model text,
    Color text,
    Memory text,
    isActive text(1)
);

-- promo_code dimension
use schema consumption;
create or replace sequence promo_code_dim_seq start = 1 increment = 1;
create or replace transient table promo_code_dim(
    promo_code_id_pk number primary key,
    promo_code text,
    isActive text(1)
);

-- customer dimension
use schema consumption;
create or replace sequence customer_dim_seq start = 1 increment = 1;
create or replace transient table customer_dim(
    customer_id_pk number primary key,
    customer_name text,
    CONCTACT_NO text,
    SHIPPING_ADDRESS text,
    country text,
    region text,
    isActive text(1)
);

-- payment dimension
use schema consumption;
create or replace sequence payment_dim_seq start = 1 increment = 1;
create or replace transient table payment_dim(
    payment_id_pk number primary key,
    PAYMENT_METHOD text,
    PAYMENT_PROVIDER text,
    country text,
    region text,
    isActive text(1)
);

-- date dimension
use schema consumption;
create or replace sequence date_dim_seq start = 1 increment = 1;
create or replace transient table date_dim(
    date_id_pk int primary key,
    order_dt date,
    order_year int,
    oder_month int,
    order_quater int,
    order_day int,
    order_dayofweek int,
    order_dayname text,
    order_dayofmonth int,
    order_weekday text
);