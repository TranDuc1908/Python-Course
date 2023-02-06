class Core(object):
    def __init__(self):
        pass
    def unicodeTrans(self, string):
        return u''.join(string).encode('utf-8').strip()