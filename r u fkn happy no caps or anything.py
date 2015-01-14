from database_system import *
import shutil

#parse cooke?

print('USE CORRECT DATA TYPES OR PAY THE IRON PRICE')
print('type help for help')
print('')
x = input('do something > ')
while x:
    
    x = x.lower()

    
    if x == 'create user':
        print('')
        print('User parameters - username, password, fname, lname, email')
        var1 = input('username (string) > ')
        var2 = input('password (string)> ')
        var3 = input('fname (string) > ')
        var4 = input('lname (string) > ')
        var5 = input('email (string) > ')
        obj_user = User(var1,var2,var3,var4,var5)
        print(obj_user)
        User.save(obj_user)
        print('')
        x = input('do something > ')
    elif x == 'create quest':
        print('')
        print('Quest parameters - name, private, creator_ref, latitude, longitude, desc, time, status')
        var1 = input('name (string) > ')
        var2 = int(input('private (int) > '))
        var3 = int(input('creator_ref (int) > '))
        var4 = float(input('latitude (float) > '))
        var5 = float(input('longitude (float) > '))
        var6 = input('description (string) > ')
        var7 = input('time (string) > ')
        var8 = input('status (string) > ')
        obj_quest = Quest(var1,var2,var3,var4,var5,var6,var7,var8)
        print(obj_quest)
        Quest.save(obj_quest)
        print('')
        x = input('do something > ')
    elif x == 'create tool':
        print('')
        print('Tool parameters - name, quest_ref, quantity')
        var1 = input('name (string) > ')
        var2 = int(input('quest_ref (int) > '))
        var3 = int(input('quantity (int) > '))
        obj_tool = Tool(var1,var2,var3)
        print(obj_tool)
        Tool.save(obj_tool)
        print('')
        x = input('do something > ')
    elif x == 'create participant':
        print('')
        print('Participant parameters - user_ref, quest_ref, is_admin')
        var1 = int(input('user_ref (int) > '))
        var2 = int(input('quest_ref (int) > '))
        var3 = int(input('is_admin (int) > '))
        obj.participant = Participant(var1,var2,var3)
        print(obj_participant)
        Participant.save(obj.participant)
        print('')
        x = input('do something > ')
    elif x == 'create tool_log':
        print('')
        print('Tool_Log parameters - user_ref, tool_ref')
        var1 = int(input('user_ref (int) > '))
        var2 = int(input('tool_ref (int) > '))
        obj.toolog = Tool_Log(var1,var2)
        print(obj.toolog)
        Tool_Log.save(obj.toolog)
        print('')
        x = input('do something > ')
        

        
    elif x == 'find user':
        print('')
        print('searching by - username')
        objiet = input('user to search > ')
        x = User.find('username', objiet)
        print(x[0].username)
        print(x[0].password)
        print(x[0].fname)
        print(x[0].lname)
        print(x[0].email)
        print('')
        x = input('do something > ')
    elif x == 'find quest':
        print('')
        print('searching by - questname')
        objiet = input('quest to search > ')
        x = Quest.find('name', objiet)
        print(x[0].name)
        print(x[0].private)
        print(x[0].creator_ref)
        print(x[0].location)
        print(x[0].desc)
        print(x[0].time)
        print(x[0].status)
        print('')
        x = input('do something > ')
    elif x == 'find tool':
        print('')
        print('searching by - toolname')
        objiet = input('tool to search > ')
        x = Tool.find('name', objiet)
        print(x[0].name)
        print(x[0].quest_ref)
        print(x[0].quantity)
        print('')
        x = input('do something > ')
    elif x == 'find participant':
        print('')
        print('searching by - primary key (ref)')
        objiet = int(input('primary key to search (int) > '))
        x = Participant.find('ref',objiet)
        print('friendly reminder - ref, quest_ref, user_ref, is_admin')
        print(x[0].ref)
        print(x[0].quest_ref)
        print(x[0].user_ref)
        print(x[0].is_admin)
        print('')
        x = input('do something > ')
    elif x == 'find tool_log':
        print('')
        print('searching by - primary key (ref)')
        objiet = int(input('primary key to search (int) > '))
        x = Tool_Log.find('ref',objiet)
        print('friendly reminder - ref, user_ref, tool_ref')
        print(x[0].ref)
        print(x[0].user_ref)
        print(x[0].tool_ref)

        
    elif x == 'delete user':
        print('')
        objiet = input('enter username of user to delete > ')
        x = User.find('username', objiet)
        User.destroy(x[0])
        print('object destroyed')
        print('')
        x = input('do something > ')
    elif x == 'delete quest':
        print('')
        objiet = input('enter questname of quest to delete > ')
        x = Quest.find('name', objiet)
        Quest.destroy(x[0])
        print('object destroyed')
        print('')
        x = input('do something > ')
    elif x == 'delete tool':
        print('')
        objiet = input('enter toolname of tool to delete > ')
        x = Tool.find('name', objiet)
        Tool.destroy(x[0])
        print('object destroyed')
        print('')
        x = input('do something > ')
    elif x == 'delete participant':
        print('')
        objiet = int(input('enter ref of participant to delete (int) > '))
        x = Participant.find('ref', objiet)
        Participant.destroy(x[0])
        print('object destroyed')
        print('')
        x = input('do something > ')
    elif x == 'delete tool_log':
        print('')
        objiet = int(input('enter ref of tool_log to delete (int) > '))
        x = Tool_Log.find('ref',objiet)
        Tool_Log.destroy(x[0])
        print('object destroyed')
        print('')
        x = input('do something > ')


        
    elif x == 'findall user' or x == 'findall users':
        print('')
        for i in User.find():
            print(i.username)
        print('')
        x = input('do something > ')
    elif x == 'findall quest' or x == 'findall quests':
        print('')
        for i in Quest.find():
            print(i.name)
        print('')
        x = input('do something > ')
    elif x == 'findall tool' or x == 'findall tools':
        print('')
        for i in Tool.find():
            print(i.name)
        print('')
        x = input('do something > ')
    elif x == 'findall participant' or x == 'findall participants':
        print('')
        print('this would just give you a bunch of numbers')
        print('')
        x = input('do something > ')
    elif x == 'findall tool_log':
        print('')
        print('this would just give you a bunch of numbers')
        print('')
        x = input('do something > ')


        
    elif x == 'nuke':
        print('')
        print('nuking...')
        for q in Quest.find():
            Quest.destroy(q)
        for u in User.find():
            User.destroy(u)
        for t in Tool.find():
            Tool.destroy(t)
        for p in Participant.find():
            Participant.destroy(p)
        for tl in Tool_Log.find():
            Tool_Log.destroy(tl)
        print('cya scrub rekt')
        print('')
        x = input('do something > ')

    elif x == 'repopulate':
        print('')
        print('resetting to default database')
        print('')
        print('nuking ...')
        for q in Quest.find():
            Quest.destroy(q)
        for u in User.find():
            User.destroy(u)
        for t in Tool.find():
            Tool.destroy(t)
        for p in Participant.find():
            Participant.destroy(p)
        for tl in Tool_Log.find():
            Tool_Log.destroy(tl)
        print('populating ...')
        shutil.copyfile("database_system/terra_quest_bup.db","database_system/terra_quest.db")
        print('table reset!')
        print('')
        x = input('do something > ')
        
    elif x == 'exit':
        print('')
        print('(ಥ﹏ಥ)')
        print('')
        break
    
    elif x == 'help':
        print('')
        print('1commands: ')
        print('nuke/exit/help/repopulate')
        print('')
        print('2commands: ')
        print('create/find/findall/delete')
        print('')
        print('objects available: ')
        print('user, quest, tool, participant, tool_log')
        print('')
        print('syntax: ')
        print('<2command> <object>')
        print('')
        x = input('do something > ')
   
    else:
        print('')
        print('wat')
        print('')
        x = input('do something > ')

