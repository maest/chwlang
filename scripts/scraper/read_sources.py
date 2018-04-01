from scripts.scraper.read_sources_lib import build_xinhuanet_articles, build_163_articles, download_and_parse_articles
import logging
logging.basicConfig(level=logging.INFO)

def run():
    articles = build_xinhuanet_articles()
    #articles = build_163_articles()
    #articles = articles.iloc[:40]
    full_articles = download_and_parse_articles(articles)
    #save_full_articles_to_db(full_articles)
