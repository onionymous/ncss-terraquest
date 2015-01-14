from tornado.ncss import Server, ncssbook_log
from handlers import profiles, quests, message, errors
from templating import *
from tornado.options import options, define
import auth_utils
from database_system import *

# Port to be used by Tornado (credit: http://stackoverflow.com/a/25837878)
define("host", default="localhost", help="app host", type=str)
define("port", default=8888, help="app port", type=int)

@auth_utils.is_logged_in
def index_handler(request, logged_in):
    '''Handles the home page'''
    if logged_in: # Redirect to /home
        request.redirect('/home')
        
    else: # Show login page etc
        context = {
            'user' : None,
            'title': 'Terra Quest',
            'quests' : Quest.find()
        }
        request.write(render('templates/index_loggedout.html', context))

@auth_utils.needs_login
def home_handler(request):
    context = {
        'user' : request.user,
        'title': 'Terra Quest',
        'quests' : Quest.find(),
    }
    request.write(render('templates/index_loggedin.html', context))

def invalid_url_handler(request):
    request.send_error(status_code = 404)
            
def map_handler(request):
    request.write(render('templates/map.html', {}))
        

# /quest/create?qid=0
# if user owns quest, will open editor
# if invalid or has no rights, create new

server = Server(hostname=options.host, port=options.port)
server.register(r'/', index_handler)
server.register(r'/home', home_handler)
server.register(r'/login', profiles.ProfileHandler.login)
server.register(r'/logout', profiles.ProfileHandler.logout)
server.register(r'/user/new', profiles.ProfileHandler.new)
server.register(r'/user', profiles.ProfileHandler.submit_new)
server.register(r'/user/(\d+)/edit', profiles.ProfileHandler.profile_edit)
server.register(r'/user/(\d+)', profiles.ProfileHandler.profile, get = profiles.ProfileHandler.profile, patch = profiles.ProfileHandler.update, delete = profiles.ProfileHandler.delete)
server.register(r'/quest/(\d+)/messages', message.MessageHandler)
server.register(r'/quest/(\d+)/messagebox', message.MessageBoxHandler)
server.register(r'/quest/create', quests.QuestHandler.quest_editor, post = quests.QuestHandler.quest_create)
server.register(r'/quest/(\d+)', quests.QuestHandler.quest, write_error = errors.ErrorHandler.write_error)


server.register(r'/map', map_handler)
server.register(r'.+', invalid_url_handler, write_error = errors.ErrorHandler.write_error)
server.cookie_secret = 'bacon'  # allow cookies over server restarts
server.run()
