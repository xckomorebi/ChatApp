import sqlite3

if __name__ == "__main__":
    user_ddl = """
create table if not exists user 
(
    name   varchar(50) not null
        constraint user_pk
            primary key,
    ip     varchar(15) not null,
    port   integer     not null,
    status varchar(3) default 'yes' not null
);
    """

    user_index_ddl = """
create unique index if not exists user_name_uindex
on user (name);
"""

    conn = sqlite3.connect("resource/chatapp.db")
    cursor = conn.cursor()
    cursor.execute(user_ddl)
    cursor.execute(user_index_ddl)
    conn.commit()
