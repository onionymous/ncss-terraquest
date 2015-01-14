import sqlite3, os
path = os.path.realpath(__file__)
path = os.path.dirname(path)
conn = sqlite3.connect(path+'/terra_quest.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def create_tables():
    with open(path +"/tablemaker.txt") as file:
         data = file.read()
         cur.executescript(data)
    conn.commit()

create_tables() #runs if tables dont already exist

class Table:
    def __init__(self):
        self.className = self.__class__.TABLE
        self.rowID = None

##    def get(value, group = None, order_by = None, where = None, having = None, limit = None, distinct = None):
##    {age:'>20', name:'john'}

    @classmethod
    def find(cls, key = -1, value = -1, orderBy=None):
        order = ""
        if orderBy is not None:
            if orderBy[0] == "+":
                order = "ORDER BY " + orderBy[1:]
            elif orderBy[0] == "-":

                order = "ORDER BY " + orderBy[1:] + "DESC"
            else:
                raise ValueError("Must include either a '+' or '-' as first character for 3rd parameter, orderBy")
        query = cur.execute('SELECT * FROM {} WHERE {} = ?'.format(cls.TABLE, key) + order, (value,))
        results = query.fetchall()
        objs = []
        
        for row in results:
            obj = cls.load(row)
            objs.append(obj)
            obj.rowID = row[0]
        return objs

    @classmethod
    def get(cls, id):
        query = cls.find("rowid",id)
        if len(query) == 0:
            return None
        return query[0]
        

    def save(self, value_dict, where = None):
        if self.rowID == None:
            cur.execute('INSERT INTO {} DEFAULT VALUES'.format(self.className))
            self.rowID = cur.lastrowid
        for key, value in value_dict.items():
            cur.execute('UPDATE {} SET {} = ? WHERE rowid = ?'.format(self.className, key), (value, self.rowID))

        conn.commit()
            
    @classmethod
    def destroy(cls, row):
        if row.rowID is not None:
            cur.execute("DELETE FROM {} WHERE rowid = ?".format(row.className),(row.rowID,))
            conn.commit()
        row.rowID = None
        
#class Tool_Log(Table):
#   def __init__(self, ref, user_id, quest_id, tool_id):
#        self.ref = ref
#        self.user_id = user_id
#        self.quest_id = quest_id
#        self.tool_id = tool_id

#-----------------------------------------------------------------------------------------------------------------------------------------

class User(Table):
    TABLE = 'User'
    def __init__(self, username, password, fname, lname, email):
        super().__init__()
        self.username = username
        self.password = password
        self.fname = fname
        self.lname = lname
        self.email = email
        self.exp = 0

    def save(self):
        self_dict = {'username':self.username, 'password':self.password, 'fname':self.fname, 'lname':self.lname, 'email':self.email}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['username'], data['password'], data['fname'], data['lname'], data['email'])
        return u

    @classmethod
    def check_password(cls, user, passw):
        founduser = cls.find("username",user)
        if len(founduser) != 0:
            if founduser[0].password == passw:
                return True
        return False

# u.participateIn(QuestId)

    def participateIn(self, QuestId, admin):
        p = Participant(self.rowID, QuestId, admin)
        p.save()
        
# x = a.findQuests(QuestId)
#aay lmao

    def findQuests(self, QuestId = None):
        userID = self.rowID
        QuestList = []
        query = Participant.find('user_ref',userID)            
        for obj in query:
            if QuestId is None:
                QuestList.append(Quest.get(obj.quest_ref))     
            else:
                if obj.quest_ref == QuestId:
                    return True
        if QuestId is None:
            return QuestList
        return False

  # def stopParticipatingIn(self, QuestId):
        

#-----------------------------------------------------------------------------------------------------------------------------------------

class Quest(Table):
    TABLE = "Quest"
    def __init__(self, name, private, creator_ref, lat, long, desc, time, status):#, exp_returned): #exp_returned TODO
        super().__init__()
        self.name = name
        self.status = status
        self.private = private
        self.creator_ref = creator_ref
        self.lat = lat
        self.long = long
        #tites fall down
        
        self.desc = desc
        self.time = time
        #self.exp_returned = exp_returned

    def save(self):
        self_dict = {'name':self.name, 'status':self.status, 'creator_ref':self.creator_ref, 'private':self.private, 'lat':self.lat, 'long':self.long, 'desc':self.desc, 'time':self.desc}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['name'], bool(data['private']), data['creator_ref'], data['lat'], data['long'], data['desc'], data['time'], data['status'])
        return u

    def addUser(self, UserId, admin):
        p = Participant(UserId, self.rowID, admin)
        p.save()

    def tools(self):
        return Tool.find('quest_ref', self.rowID)

    def admins(self):
        return [u for u in self.findUsers() if u.is_admin]
        
# x = a.findQuests(QuestId)
#aay lmao

    def findUsers(self, UserId = None):
        questID = self.rowID
        UserList = []
        query = Participant.find('quest_ref',questID)            
        for obj in query:
            if UserId is None:
                user = User.get(obj.user_ref)
                user.is_admin = obj.is_admin
                UserList.append(user)     
            else:
                if obj.user_ref == UserId:
                    return True
        if UserId is None:       
            return UserList
        return False

    def isAdmin(self, UserId):
        query = Participant.find('user_ref',UserId)
        if len(query) != 0 and query[0].is_admin:
            return True
        return False

#-----------------------------------------------------------------------------------------------------------------------------------------

class Message(Table):
    TABLE = "Message"
    def __init__(self, user_ref, quest_ref, text, time, category):
        super().__init__()
        self.user_ref = user_ref
        self.quest_ref = quest_ref
        self.text = text
        self.time = time
        self.category = category

    def save(self):
        self_dict = {'user_ref':self.user_ref, 'quest_ref':self.quest_ref, 'text':self.text, 'time':self.time, 'category':self.category}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['user_ref'], data['quest_ref'], data['text'], data['time'], data['category'])
        return u

#-----------------------------------------------------------------------------------------------------------------------------------------

class Invite(Table):
    TABLE = "Invite"
    def __init__(self, invitee_ref, inviter_ref, quest_ref, date):
        super().__init__()
        self.invitee_ref = invitee_ref
        self.inviter_ref = inviter_ref
        self.quest_ref = quest_ref
        self.date = date

    def save(self):
        self_dict = {'invitee_ref':self.invitee_ref, 'inviter_ref':self.inviter_ref, 'quest_ref':self.quest_ref, 'date':self.date}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['invitee_ref'], data['inviter_ref'], data['quest_ref'], data['date'])
        return u

#-----------------------------------------------------------------------------------------------------------------------------------------

class Tool(Table):
    TABLE = "Tool"
    def __init__(self, quest_ref, name, quantity):
        super().__init__()
        self.quest_ref = quest_ref
        self.name = name
        self.quantity = quantity

    def save(self):
        self_dict = {'quest_ref':self.quest_ref, 'name':self.name, 'quantity':self.quantity}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['quest_ref'], data['name'], data['quantity'])
        return u

    def assignToUser(self, UserId):
        t = Tool_Log(UserId, self.rowid)
        t.save()
  

#-----------------------------------------------------------------------------------------------------------------------------------------

class Participant(Table):
    TABLE = "Participant"
    def __init__(self, user_ref, quest_ref, is_admin):
        super().__init__()
        self.user_ref = user_ref
        self.quest_ref = quest_ref
        self.is_admin = is_admin

    def save(self):
        self_dict = {'user_ref':self.user_ref, 'quest_ref':self.quest_ref, 'is_admin':self.is_admin}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['user_ref'], data['quest_ref'], bool(data['is_admin']))
        return u

    

#-----------------------------------------------------------------------------------------------------------------------------------------
    

class Tool_Log(Table):
    TABLE = "Tool_Log"
    def __init__(self, user_ref, tool_ref):
        super().__init__()
        self.user_ref = user_ref
        self.tool_ref = tool_ref

    def save(self):
        self_dict = {'user_ref':self.user_ref, 'tool_ref':self.tool_ref}
        super().save(self_dict)

    @classmethod
    def load(cls, data):
        u = cls(data['user_ref'], data['tool_ref'])
        return u

#-----------------------------------------------------------------------------------------------------------------------------------------
#TESTING

if __name__ == "__main__":
    u = Quest("To Mordor",False,1,2345678987.2345,5162452346524.2345,"Take the ring to Mordor",15134562356256213,"Ongoing")
    u.save()
    p = Participant(1, u.rowID, False)
    p.save()
    user = User("asf", "he", "Be", "n", "a@g")
    user.save()
    user = User.get(1)
    for x in range(100):
        print(user.findQuests(x))
            

