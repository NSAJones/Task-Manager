import sqlite3 as sql
import uuid,sys

class Database:
    def __init__(self) -> None:
        self.db = sql.connect("db/data.db", check_same_thread=False)
        self.cursor = self.db.cursor()
        self.create_db()

    def create_db(self):
        query = """
        CREATE TABLE IF NOT EXISTS Login(
        username VARCHAR(15) PRIMARY KEY,
        password VARCHAR(15) NOT NULL,
        sessionID VARCHAR(15)
        );

        CREATE TABLE IF NOT EXISTS ToDoList(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(25) NOT NULL,
        creator VARCHAR(15) NOT NULL,
        FOREIGN KEY (creator) REFERENCES Login(username)
        );

        CREATE TABLE IF NOT EXISTS Task (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        ToDoListID INTEGER,
        name VARCHAR(25) NOT NULL,
        description TEXT(50),
        FOREIGN KEY (ToDoListID) REFERENCES ToDoList(ID)
        );
        """

        self.cursor.executescript(query)
        self.db.commit()
    
    def validate_user(self,username:str,password:str) -> str:
        """Checks user is valid and then generates a session ID if
        they are. Returns generated session ID."""

        # Check user exists
        self.cursor.execute(
            "SELECT * FROM Login WHERE username=? AND password=?",
            (username,password))
        response = self.cursor.fetchall()

        

        # If User exists generate sessionID and update user in table
        if response != []:
            sessionID = str(uuid.uuid4())
            self.cursor.execute(
                "UPDATE Login SET sessionID=? WHERE username=? AND password=?",
                (sessionID,username,password)
                )
            self.db.commit()
            return sessionID
        return None
    
    def sessionID(self,id:str) -> str:
        """Check session ID is valid, returns username."""

        # Check session ID is valid
        self.cursor.execute(
            "SELECT username FROM Login WHERE sessionID=?",
            (id,)
        )
        response = self.cursor.fetchall()

        if response != []:
            return response[0][0]
        return None

    def get_todolists(self,username:str):
        self.cursor.execute(
            "SELECT * FROM ToDoList WHERE creator=?",
            (username,)
        )
        return self.cursor.fetchall()

    def get_tasks(self,id:int):
        self.cursor.execute(
            "SELECT * FROM Task WHERE ToDoListID=?",
            (id,)
        )
        return self.cursor.fetchall()

    def create_todolist(self,username:str,name:str):
        self.cursor.execute(
            "INSERT INTO ToDoList (name,creator) VALUES (?,?)",
            (id,name,username)
        )

        self.db.commit()

    def update_task(self,taskID):
        pass
    
    def create_user(self,username:str,password:str):
        """Creates a new user."""

        # Check user exists
        self.cursor.execute(
            "SELECT * FROM Login WHERE username=? AND password=?",
            (username,password))
        response = self.cursor.fetchall()

        # If user doesn't exist create user
        if response == []:
            self.cursor.execute(
                "INSERT INTO Login (username,password) VALUES (?,?)",
                (username,password)
            )
            self.db.commit()

            return True
        return False

    def get_user(self,sessionID:str) -> str:
        self.cursor.execute("SELECT username FROM Login WHERE sessionID=?",
                        (sessionID,))
        response = self.cursor.fetchall()

        print(response,sessionID, file=sys.stdout)

        if response:
            return response[0][0]
        return None


    def create_todolist(self,sessionID:str):
        """Create empty todolist, return id of newly created list"""

        username = self.get_user(sessionID)
        self.cursor.execute(
            "INSERT INTO ToDoList (creator,name) VALUES (?,?)",
            (username,"untitled"))
        
        # Return new entry id
        return self.cursor.lastrowid

database = Database()
    
if __name__ =='__main__':
    db = Database()
    db.create_user("foo","bar")
    id = db.validate_user("foo","bar")
    user = db.sessionID(id)
    print(f"id= {id} user= {user}")

