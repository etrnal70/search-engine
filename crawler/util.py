from urllib.parse import urlparse
import requests
class Util:
    def count_keyword_in_text(self, text, keyword):
        count_keyword = text.count(keyword)
        return count_keyword
    
    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.scheme in ['http', 'https'] and bool(parsed.netloc)
    
    def get_page(self, url):
        try:
            res = requests.get(url, verify=False, timeout=300)
            res.raise_for_status()
            return res
        except Exception as e:
            print(e)
            return
    
    def running_thread_count(self, futures):
        r = 0
        for future in futures:
            if future.running():
                r += 1
        print(f'{r} threads running')
        return r
