import auth_utils
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from templating import *
from database_system import *

chatList = set()

class MessageHandler(WebSocketHandler):
    def on_message(self, text):
        self.write_message("Msg: ")
        #questID = 0 # int(questID) 
        #m = Message(request.user.rowID, questID, text, "", "")
        #m.save()
        #request.redirect('/quest/%s' % (questID))
        for x in chatList:
            x.write_message(text)
          
    def open(self, huh):
        chatList.add(self)
        self.write_message("Hello friend!")
        print('websocket open')
        print(huh)

    def on_close(self):
        chatList.remove(self)
        print('websocket closed')

class MessageBoxHandler(RequestHandler):        
    @auth_utils.needs_login
    def get(request, questID):
        quest = Quest.get(questID)
        messages = Message.find('quest_ref', questID)
        for i in range(len(messages)):
            messages[i].username = User.get(messages[i].user_ref).username
        context = {'user': request.user, 'messages': messages, 'quest': quest}
        request.write(render('templates/chat_box.html', context))
 
    @auth_utils.needs_login
    def post(request, questID):
        text = request.get_body_argument("chatMsg")
        questID = int(questID)
        if text:
            print(request.user) 
            m = Message(request.user.rowID, questID, text, "", "")
            m.save()
            request.redirect('/quest/%s' % (questID))
        
        for x in chatList:
            x.write_message(text)
        
 