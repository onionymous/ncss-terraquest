from tornado.ncss import Server
import templating

class MockFriend:
    def __init__(self, name, age, gender, eat):
        self.name = name
        self.age = age
        self.gender = gender
        self.eat = eat


def index_handler(request):
    friends = [MockFriend('Frank', 32, 'M', 'omni'),
               MockFriend('Brett', 46, 'M', 'vego'),
               MockFriend('Emily', 18, 'F', 'vegan')]
    data = {"name": "potato", "friends": friends}

    try:
        response = templating.render('templates/index.html', data)
        request.write(response)
    except SyntaxError:
        request.write("Template syntax error")


server = Server()
server.register(r'/', index_handler)
server.run()
