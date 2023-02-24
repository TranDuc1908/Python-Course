class CoreHelper():
    def unicodeTrans(self, string):
        return u''.join(string).encode('utf-8').strip()