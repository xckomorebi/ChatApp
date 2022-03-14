create table user
(
    name   varchar(50) not null
        constraint user_pk
            primary key,
    ip     varchar(15) not null,
    port   integer     not null,
    status varchar(3) default 'yes' not null
);

create unique index user_name_uindex
    on user (name);

