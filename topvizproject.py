__author__ = 'vs'

class Keyword():
    def __init__(self, kw = None, group = None, relpage = None, date = None, position = None):
        self.group =group
        self.relpage = relpage
        self.stat = dict()
        self.add_date(date,position)

    def __repr__(self):
        return "%s:%s даты: %s" % (self.group, self.relpage, self.stat)

    def add_date(self, date, position):
        self.stat[date] = position


class Project():
    def __init__(self, tv_url=None, keywords_count=None, title=None):
        self.tv_url = tv_url
        self.keywords_count = keywords_count
        self.title = title
        self.keywords = {}
# keywords: {group, relpage, (date : position)}

    def add_keyword(self, element, kw_value):
        if element in self.keywords:
            self.keywords[element].stat.update(kw_value.stat)
        else:
            self.keywords[element] = kw_value

    def __repr__(self):
        return "%s:%s:%s:%s" % (self.title, self.keywords_count, self.tv_url, self.keywords)
