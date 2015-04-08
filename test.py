from topvizproject import Keyword, Project

kw = Keyword(group='group213', date='12.11.10', position='pos12')
#print(kw)
kw.add_date('12.11.09','-')
#print(kw)

pr = Project(tv_url='url', keywords_count='13', title='тестовый титул')
#print (pr)
pr.add_keyword('херь', kw)
#print ('Первый прогон %s' % pr)
kw = Keyword(group='group213', date='13.', position='---')
pr.add_keyword('херь', kw)
print ('Второй прогон %s' % pr)
