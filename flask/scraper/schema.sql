drop table if exists products;
create table products (
    id integer primary key autoincrement,
    category_id integer not null,
    name text not null,
    code varchar(255)
);

drop table if exists categories;
create table categories (
    id integer primary key autoincrement,
    parent integer,
    name varchar(255)
);
