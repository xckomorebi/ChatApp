create table if not exists message
(
    id      integer     not null
        constraint message_pk
            primary key autoincrement,
    content text        not null,
    from_   varchar(50) not null,
    "to"    varchar(50) not null,
    type_   varchar(10) not null,
    timestamp varchar(30) not null,
    status  varchar(3) default 'yes' not null
);
