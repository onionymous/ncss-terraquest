#!/usr/bin/env python3
from database_system import *

user = User('sam', 'iamsupercool', 'Sam', 'Thorogood', 'butts@google.com')
user.save()

user2 = User('tim', 'password1', 'Tim', 'Dawborn', 'kilotim@google.com')
user2.save()

user3 = User('tdaw0001', 'qwerty', 'Tim', 'Dawborn', 'timD@google.com')
user3.save()

users = User.find()

print('Find all users in the database:')

for u in users:
    print('{} - {} {} - {} - {}'
          .format(u.rowID, u.fname, u.lname, u.username, u.email))

#-------------------

print("\nChange the username for user 2 to 'timmy':")

user2.username = 'timmy'
user2.save()

user = User.get(2)
print('Username is now: {}'.format(user.username))


print("\nFind all users with the firstname 'Tim':")
users = User.find('username','Tim')

for u in users:
    print('{} - {} {} - {} - {}'
          .format(u.rowID, u.fname, u.lname, u.username, u.email))

#-------------------

quest = Quest('Walk 1 Kilotim', 'false', user2.rowID,
              'Google Inc., Sydney', 'Walk', '1:00am', 'Ongoing')
quest.save()

quest2 = Quest('NCSS All-Nighter', 'false', user.rowID, 'USYD',
               'Code', '8:30pm', 'Ongoing')
quest2.save()

print("\nList all quests from the database:")
for quest_load in Quest.find():
    print('{} at {}'.format(quest_load.name, quest_load.location))

#-------------------

print("\nMake some users part of some quests...")
participant = Participant(2, 1, True)
participant.save()

participant = Participant(2, 2, False)
participant.save()

participant = Participant(1, 2, False)
participant.save()

print("\nPrint the participants table:")
for p in Participant.find():
    print("user_ref:{}, quest_ref:{}, is_admin:{}"
          .format(p.user_ref, p.quest_ref, p.is_admin))

print("\nFind all quests that user 1 is in:")
for p in Participant.find('user_ref', 1):
    quest = Quest.get(p.quest_ref)
    print("{}".format(quest.name))

#-------------------

print("\nDelete all the users, participants and quests...")

for q in Quest.find():
    Quest.destroy(q)

for u in User.find():
    User.destroy(u)

for p in Participant.find():
    Participant.destroy(p)
#-------------------

print("\nNow show all the users and quests in the database:")

users = User.find()
quests = Quest.find()
participants = Participant.find()

print(users, participants, quests)


# add exp
# add **kwargs
