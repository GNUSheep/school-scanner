import mysql.connector


class Connection:
    def __init__(self):
        self.con = mysql.connector.connect(
            host="",
            user="",
            password="",
            database="",
        )
        if self.con:
            print("Connection established")
        else:
            print("ERROR: CANNOT CONNECT TO DATABASE")


def isUser(string):
    for c in string:
        if c.isalpha():
            return True
    return False


class Request:
    def __init__(self, user_input):
        self.user_input = user_input
        self.usr = self.User(user_input)
        self.tl = self.Tool(user_input)

    class User:
        def __init__(self, user_input):
            self.id = user_input

        def isExist(self, con):
            cur = con.cursor()

            cur.execute("SELECT ID FROM users")
            output = cur.fetchall()

            for usr in output:
                if self.id == usr[0]:
                    return True

            return False

        def get_name(self, con):
            cur = con.cursor()

            cur.execute("SELECT Name FROM users WHERE ID='" + self.id + "'")
            output = cur.fetchall()

            for out in output:
                return out[0]

        def get_borrowed_tools(self, name, con):
            cur = con.cursor()

            cur.execute("SELECT * FROM tools WHERE who_borrowed='" + name + "' AND is_borrowed='1'")
            output = cur.fetchall()

            tools = []

            for out in output:
                tools.append([out[0], out[1]])

            return tools

        def create(self, name, con):
            cur = con.cursor()

            cur.execute(
                "Insert into users (ID, Name) Values ('"
                + self.id
                + "', '"
                + name
                + "')"
            )

    class Tool:
        def __init__(self, user_input):
            self.id = user_input

        def isExist(self, con):
            cur = con.cursor()

            cur.execute("SELECT ID FROM tools")
            output = cur.fetchall()

            for tool in output:
                if int(self.id) == tool[0]:
                    return True
            return False

        def add(self, name, con):
            cur = con.cursor()

            cur.execute(
                "Insert into tools (Name, is_borrowed) Values ('" + name + "', '0')"
            )

        def isBorrowed(self, con):
            cur = con.cursor()

            cur.execute("SELECT ID FROM tools")
            output = cur.fetchall()

            for tool in output:
                if int(self.id) == tool[0]:
                    cur.execute("SELECT is_borrowed FROM tools WHERE ID=" + self.id)
                    out = cur.fetchall()[0]
                    if 1 == int(out[0]):
                        return True
                    return False

        def borrow(self, user, con):
            cur = con.cursor()

            cur.execute("UPDATE tools SET is_borrowed=1, who_borrowed='"+ user + "', when_borrowed=NULL WHERE ID=" + self.id)

            con.commit()

        def unborrow(self, con):
            cur = con.cursor()

            cur.execute("UPDATE tools SET is_borrowed=0, who_borrowed=NULL, when_borrowed=NULL WHERE ID=" + self.id)

            con.commit()
