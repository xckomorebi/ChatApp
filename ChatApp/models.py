from ChatApp.utils import get_conn, get_timestamp


class User:

    def __init__(self, name, ip, port, status="yes"):
        self.name = name
        self.ip = ip
        self.port = port
        self.status = status

    def __eq__(self, another):
        if not isinstance(another, User):
            return False
        return self.__dict__ == another.__dict__

    @classmethod
    def from_dict(cls, dict_):
        return cls(**dict_)

    @classmethod
    def from_list(cls, list_):
        result = []
        if isinstance(list_, dict):
            list_ = [list_]
        for dict_ in list_:
            result.append(cls.from_dict(dict_))
        return result

    @property
    def addr(self):
        return (self.ip, self.port)

    def __repr__(self):
        return f"User({self.name}, {self.addr}, {self.status})"

    def exists(self):
        return self.get_by_name(self.name) is not None

    def save_or_update(self):
        if self.exists():
            self.update()
        else:
            self.save()

    def save(self):
        sql = "insert into user(name, ip, port, status) " \
              "values (?, ?, ?, ?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.name, self.ip, self.port, self.status))
        conn.commit()

    def update(self):
        sql = "update user set ip = ?, port = ?, status = ? " \
              "where name = ?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.ip, self.port, self.status, self.name))
        conn.commit()

    @classmethod
    def save_from_list(cls, users):
        users = cls.from_list(users)
        for user in users:
            user.save_or_update()

    @classmethod
    def get_all_active_users(cls):
        sql = "select * from user where status='yes'"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    @classmethod
    def get_all(cls):
        sql = "select * from user"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    @classmethod
    def get_by_name(cls, name):
        sql = "select * from user where name=?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))
        user = cursor.fetchone()
        return cls(**user) if user else None


class Message:

    def __init__(self,
                 content,
                 from_,
                 to,
                 type_,
                 status="yes",
                 timestamp=get_timestamp()):
        self.content = content
        self.from_ = from_
        self.to = to
        self.type_ = type_
        self.status = status
        self.timestamp = timestamp

    def save(self):
        sql = "insert into message(content, from_, `to`, type_, timestamp) " \
              "values(?, ?, ?, ?, ?)"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (self.content, self.from_,
                       self.to, self.type_, self.timestamp))
        conn.commit()

    @classmethod
    def get_by_name(cls, name):
        sql = "select * from message where status='yes' and `to`=?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))
        messages = cursor.fetchall()
        return messages
 
    @classmethod
    def clear_message_by_name(cls, name):
        sql = "update message set status='no' where `to`=?"
        conn = get_conn()
        cursor = conn.cursor()
        cursor.execute(sql, (name, ))
        conn.commit()

    @classmethod
    def retrieve_by_name(cls, name):
        messages = cls.get_by_name(name)
        cls.clear_message_by_name(name)
        return messages