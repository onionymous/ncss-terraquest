import html
from sys import stderr

class Node:
    def render(context):
        raise NotImplementedError("heh")

class GroupNode(Node):
    def __init__(self):
        self.children = []
        
    def add_child(self, child):
        self.children.append(child)

    def render(self, context):
        return ''.join(i.render(context) for i in self.children)
        
class TextNode(Node):
    def __init__(self, content):
        self.content = content

    def render(self, context):
        return self.content

class PythonNode(Node):
    def __init__(self, code):
        self.code = code

    def render(self, context):
        try:
            return html.escape(str(eval(self.code, {}, context)))
        except Exception as e:
            stderr.write("Templating error: " + str(e) + "\n")
            return 'VARIABLE_NOT_FOUND'

class ForNode(Node):
    def __init__(self, arg, lst, group):
        self.arg = arg
        self.lst = lst
        self.group = group

    def render(self, context):
        arr = []
        for i in eval(self.lst, {}, context):
            newcontext = {}
            newcontext.update(context)
            newcontext[self.arg] = i
            arr.append(self.group.render(newcontext))
        return ''.join(arr)

class IfNode(Node):
    def __init__(self, args, groups, elsegroup=None):
        self.args = args
        self.groups = groups
        self.elsegroup = elsegroup

    def render(self, context):
        for arg, group in zip(self.args, self.groups):
            if eval(arg, {}, context):
                return group.render(context)
        if self.elsegroup != None:
            return self.elsegroup.render(context)
        else:
            return ""

# This testing code is not run when the file is imported
if __name__ == '__main__':
    root = GroupNode()
    root.add_child(TextNode("<p>"))
    root.add_child(PythonNode("x * y"))
    root.add_child(TextNode("<p>"))

    forgroup = GroupNode()
    forgroup.add_child(PythonNode('i*i'))
    root.add_child(ForNode('i', 'mylist', forgroup))
    root.add_child(TextNode('\n'))

    ifgroup1 = GroupNode()
    ifgroup1.add_child(TextNode("ifblock"))
    ifgroup2 = GroupNode()
    ifgroup2.add_child(TextNode("elifblock"))
    ifgroup2_1 = GroupNode()
    ifgroup2_1.add_child(TextNode("elifblock2"))
    ifgroup3 = GroupNode()
    ifgroup3.add_child(TextNode("elseblock"))
    root.add_child(IfNode(["1==1", "2*2==4", "'56' in 'abcd5'"], [ifgroup1, ifgroup2, ifgroup2_1], ifgroup3))


    print(root.render({'x': 3, 'y': 4, 'mylist': [1, 2, 3, 4, 100]}))

