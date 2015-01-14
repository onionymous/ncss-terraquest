import re

try:
    import tree
except ImportError:
    from . import tree

# Tokeniser regex
splitter = re.compile(r'(\{\{.+?\}\})|(\{%.+?%\})', re.MULTILINE | re.DOTALL)

class Parser:
    # Class constructor to set cursor to start of token list
    def __init__(self):
        self.counter = 0

    # Checks if all the tokens have been parsed and returns True, False otherwise
    def end(self):
        return self.counter == len(self.tokens)

    # Increment the cursor position
    def next(self):
        if not self.end():
            self.counter += 1

    # Current cursor position
    def current(self):
        return None if self.end() else self.tokens[self.counter]

    # Parse a given token group
    def parse(self, tokens):
        self.tokens = tokens
        self.counter = 0
        return self.parse_group()

    # Methods for extracting current token for python tokens
    #

    def is_command(self):
        return re.search(r'{% *.+ *%}', self.current())

    def unpack_command(self):
        r = re.search(r'{% *(.+?)( .+)? *%}', self.current())
        keyword, arg = r.group(1).strip(), r.group(2)
        if arg:
            arg = arg.strip()
        return keyword, arg

    # Terminal tokens should terminate parsing the current group, i.e. end, elif or else blocks
    def is_terminal_token(self):
        if self.is_command():
            keyword, arg = self.unpack_command()
            if keyword in ["end", "elif", "else"]:
                return True
        return False

    def has_terminal(self, string):
        return self.is_terminal_token() and string in self.current()

    def has_command(self, string):
        return self.is_command() and self.unpack_command()[0] == string

    def is_expr(self):
        r = re.search(r'{{ *(.+) *}}', self.current())
        if r:
            return r.group(1)
        else:
            return None

    def parse_group(self):
        group = tree.GroupNode()
        while not self.end():
            if self.is_terminal_token(): # end, elif or else
                break
            elif self.is_expr():
                node = tree.PythonNode(self.current()[2:-2])
                self.next()
            elif self.is_command():
                keyword, arg = self.unpack_command()
                if keyword == 'for':
                    node = self.parse_for()
                elif keyword == 'if':
                    node = self.parse_if()
                elif keyword == 'include':
                    node = parse_file(arg)
                    self.next()
                elif keyword == 'comment':
                    self.parse_comment()
                    continue
                else:
                    raise SyntaxError("Invalid command: " + self.current())
            else:
                node = tree.TextNode(self.current())
                self.next()
            group.add_child(node)
        return group

    def parse_for(self):
        if not self.has_command('for'):
            raise SyntaxError("Expected block: for")
        arg, lst = self.unpack_command()[1].split(' in ')
        self.next()
        group = self.parse_group()
        if self.has_terminal('for'):
            self.next()
            for_node = tree.ForNode(arg, lst, group)
            return for_node
        else:
            raise SyntaxError("Expected end block: for")

    def parse_if(self):
        if not self.has_command('if'):
            raise SyntaxError("Expected block: if")
        args = [self.unpack_command()[1]]
        self.next()
        groups = [self.parse_group()]
        elsegroup = None
        while self.has_command('elif'):
            args.append(self.unpack_command()[1])
            self.next()
            groups.append(self.parse_group())
        if self.has_command('else'):
            self.next()
            elsegroup = self.parse_group()
        if self.has_terminal('if'):
            self.next()
            if_node = tree.IfNode(args, groups, elsegroup)
            return if_node
        else:
            raise SyntaxError("Expected end block: if")

    def parse_comment(self):
        while not self.end():
            if self.has_terminal('comment'):
                break
            self.next()
        if self.end():
            raise SyntaxError("Expected end block: comment")
        self.next()

def parse_file(filename):
    tokens = [i for i in splitter.split(open(filename).read()) if i != None and i != '']
    #print(tokens)
    p = Parser()
    return p.parse(tokens)

def render(filename, dictionary):
    root = parse_file(filename)
    return root.render(dictionary)



# TEST CODE, IGNORE IF IMPORT
if __name__ == '__main__':

    class MockFriend:
        def __init__(self, name, age, gender, eat):
            self.name = name
            self.age = age
            self.gender = gender
            self.eat = eat

    friends = [MockFriend('Frank' , 32, 'M', 'omni'),MockFriend('Brett', 46, 'M', 'vego'), MockFriend('Emily', 18, 'F', 'vegan')]
    
    root = parse_file('MockWebPage.html')
    print(root.render({"name": "potato", "friends": friends}))
    # foo = re.compile(r'(?P<expr>\{\{.+?\}\})|(?P<stmt>\{%.+?%\})', re.MULTILINE | re.DOTALL)
    # for m in foo.finditer(open('test.html').read()):
    #     print(m.groupdict())
    #     print(m.start(), m.end())
