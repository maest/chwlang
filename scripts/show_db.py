from reader.models import Article, Category

def run():
    print('**Articles:')
    for a in Article.objects.all():
        print(a)
    print()
    print('**Categories:')
    for c in Category.objects.all():
        print(c)
