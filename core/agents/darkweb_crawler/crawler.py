from adapters.darkweb_adapter.tor_client import TorClient

class DarkWebCrawler:
    def __init__(self):
        self.tor_client = TorClient()

    def crawl(self, url):
        return self.tor_client.session.get(url).text
