from scraper.models import ArticleTest, CategoryTest
import json

def run():
    import pdb;pdb.set_trace()
    article = ArticleTest(headline = 'headline',
                      body = 'body')
    article.save()
    categories = [CategoryTest.objects.get_or_create(name = c)[0]
                  for c in ['name1', 'name2']]
    for c in categories:
        article.categories.add(c)
    article.save()
