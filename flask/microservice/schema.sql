create table if not exists products (
    id integer primary key autoincrement,
    category_id integer not null,
    name text not null,
    code varchar(255)
);

create table if not exists  categories (
    id integer primary key autoincrement,
    parent integer,
    name varchar(255)
);
