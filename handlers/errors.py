from templating import *

class ErrorHandler:
    def write_error(request, status_code, reason = "", **kwargs):
        print("WRITING ERROR")
        context = {
            'user' : None,
            'title': 'Terra Quest',
            'reason': reason,
        }
        if status_code == 404:
            request.write(render('templates/404.html', context))
        else:
            request.write(render('templates/500.html', context))