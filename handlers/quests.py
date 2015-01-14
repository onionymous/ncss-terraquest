import auth_utils
from tornado.options import options
from templating import *
from database_system import *

class QuestHandler:
    @auth_utils.needs_login
    def quest_editor(request):
        '''Allows user to create or edit quest'''
        context = {
            'user': request.user, 
            'title': 'Create Quest',
            'logged_in': True
        }
        request.write(render('templates/create_quest.html', context))

    @auth_utils.needs_login
    def quest_create(request):
        quest = Quest(
            request.get_field("quest_name"),
            False, # This only will become dynamic on private quest implementaiton
            request.user.rowID,
            request.get_field("location").split(" ")[0], # this isnt a good temp
            request.get_field("location").split(" ")[-1],
            request.get_field("description"),
            request.get_field("date_time"),
            "")
        quest.save()

        for name in request.get_arguments("items"):
            if name.strip() != "":
                tool = Tool(quest.rowID, name, 1)
                tool.save()
        
        quest.addUser(request.user.rowID, True)
        request.redirect(r'/quest/' + str(quest.rowID), True)
    
    @auth_utils.needs_login
    def quest(request, questID):
        '''Allows user to view or give ability to edit quest'''
        '''
        if questID != None:
            with open('static_wireframe/quest.html') as questPage:
                request.write(questPage.read())
            #NEEDS WORK. Needs to get data for individual quest
        #if isAdmin(questID):
            #Make editable link
        '''
        quest = Quest.get(questID)
        if quest is None:
            request.send_error(status_code = 404, reason = "Quest not found")
        else:
            messages = Message.find('quest_ref', questID)
            for i in range(len(messages)):
                messages[i].username = User.get(messages[i].user_ref).username
            questing = quest.findUsers(request.user.rowID)
            
            if request.request.method == 'POST':
                if not questing:
                    quest.addUser(request.user.rowID, False)
                request.redirect(request.request.path, True)
                return
                
            
            context = {
                'user': request.user,
                'title': 'View Quest', 
                'quest_id': questID,
                'quest': quest,
                'items': quest.tools(),
                'messages': messages,
                'logged_in': True,
                'questing': questing,
                'server_port': options.port,
                'server_host': options.host,
            }
            request.write(render('templates/quest.html', context))
        
