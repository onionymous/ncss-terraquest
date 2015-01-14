import auth_utils
from database_system import *
from templating import *


class ProfileHandler:
    def login(request):
        '''
        Checks username and password with "database" and redirects to
        home if true otherwise displays error message
        '''
        username = request.get_field("username", None)
        password = request.get_field("password", None)



            
        if User.check_password(username, password):
            request.set_secure_cookie("username", username)
            request.redirect(r'/home', True)
        else:
            print("Login Request was denied.")
            request.write({"status" : 'invalid_login'})


            
    def logout(request):
        '''
        Will handle the Logging out protocol
        '''
        if request.get_secure_cookie('username', None) is not None:
            request.clear_cookie('username')
            request.redirect(r'/', True)
        else:
            request.redirect(r'/', True)








    
    def new(request):
        '''Allows user to create or edit profile'''
        context = {
            'user' : None,
            'title' : "Edit Profile"
        }
        request.write(
            render("templates/create_profile.html", context))

            

    def submit_new(request):
        username = request.get_field("username", None)
        password_1 = request.get_field("password_1", None)
        password_2 = request.get_field("password_2", None)

        print(User.find("username", username))
        
        if len(User.find("username", username)) == 0:
            if password_1 == password_2: # check if boxes have values
                user = User(
                    request.get_field("username"),
                    request.get_field("password_1"),
                    request.get_field("f_name"),
                    request.get_field("l_name"),
                    request.get_field("email"))
                user.save()
                request.set_secure_cookie("username", request.get_field("username"))
                request.write({"status" : 'valid'})
            else:
                request.write({"status" : 'invalid_password'})
        else:
            request.write({"status" : 'invalid_username'})

    @auth_utils.needs_login
    def profile_edit(request, user_ID):
        context = {
            'user' : request.user,
            'title' : "Edit Profile"
        }
        request.write(
            render("templates/edit_profile.html", context))



            
    @auth_utils.needs_login
    def update(request, user_ID):
        if request.get_field("password_old") == request.user.password:
            if request.get_field("password_1") == request.get_field("password_2"): # check if boxes have values
                request.user.password = request.get_field("password_1")
                request.user.fname = request.get_field("f_name")
                request.user.lname = request.get_field("l_name")
                request.user.email = request.get_field("email")
                request.user.save()
                request.write({"status" : 'valid'})
            else:
                request.write({"status" : 'invalid_password'})
        else:
            request.write({"status" : 'invalid_password_old'})

            

    def delete(request):
        pass
        

    
    @auth_utils.needs_login
    def profile(request, user_ID):
        '''Shows user profile'''
        try:
            user_id = int(user_ID)
        except Exception:
            return None

        user = User.get(user_ID)
        if user is None:
            pass # throw 404
        else:
            adminList = list()
            for quest in user.findQuests():
               if quest.isAdmin(user.rowID):
                   adminList.append(quest)
            context = {
                'title' : 'View Quest',
                'user' : user,
                'created_quests' : adminList,
                'participating_quests' : user.findQuests()
            }
            request.write(render('templates/profile.html', context))
