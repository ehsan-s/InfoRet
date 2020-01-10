from bs4 import BeautifulSoup
import requests
import json
import pickle, os
from _md5 import md5
import time


class Cache:
    def __init__(self, cache_dir='cache/'):
        self.cache_dir = cache_dir

    def is_cached(self, url):
        cache_path = os.path.join(self.cache_dir, md5(url.encode()).hexdigest())
        if not os.path.exists(cache_path):
            return None

        return pickle.load(open(cache_path, mode='rb'))

    def cache(self, url, response):
        cache_path = os.path.join(self.cache_dir, md5(url.encode()).hexdigest())
        pickle.dump(response, open(cache_path, mode='wb'))


class Crawler:
    def __init__(self, json_file='crawl/papers.json', start_file='crawl/start.txt'):
        self.cache = Cache()
        self.crawl_url_queues = []
        with open(start_file, 'r') as file:
            urls = file.readlines()
            for url in urls:
                if 'https' in url:
                    self.crawl_url_queues.append(url)
        self.json_file = json_file
        with open(self.json_file, mode='w', encoding='utf-8') as file:
            json.dump([], file)

    def get_html(self, url):
        response = self.cache.is_cached(url)
        if response is not None:
            return response.content
        response = requests.get(url)
        time.sleep(0.1)
        if not response.ok:
            raise Exception('Error in reading html')
        self.cache.cache(url, response)
        return response.content

    def __crawl(self, url):
        content = self.get_html(url)
        soup = BeautifulSoup(content, 'html.parser')
        title = soup.find(name='meta', attrs={'name': 'citation_title'})['content']
        abstract = soup.find(name='meta', attrs={'name': 'description'})['content']
        date = soup.find(name='meta', attrs={'name': 'citation_publication_date'})['content']
        authors = soup.find_all(name='meta', attrs={'name': 'citation_author'})
        authors = [author['content'] for author in authors]
        references = soup.select(
            '#references > div.card-content > div > div.citation-list__citations div.citation__body > h2 > a')
        references = ['https://www.semanticscholar.org' + reference['href'] for reference in references]
        references = references[0:min(len(references), 10)]
        id = soup.find('link')['href'].split('/')[-1]

        return {'title': title, 'abstract': abstract, 'references': references, 'id': id, 'date': date,
                'authors': authors}

    def crawl(self, limit=5000):
        cntr = 0
        results = []
        while len(self.crawl_url_queues) > 0 and cntr < limit:
            url = self.crawl_url_queues.pop(0)
            print(url)
            result = self.__crawl(url)
            if cntr % 10 is 0:
                print(cntr)
            references = result.get('references')
            self.crawl_url_queues.extend(references[0:min(5, len(references))])
            results.append(result)
            cntr += 1

        return results


if __name__ == '__main__':
    if not os.path.exists('articles.json'):
        crawler = Crawler()
        results = crawler.crawl()
        json.dump(results, open('articles.json', 'w'))
