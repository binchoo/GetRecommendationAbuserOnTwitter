
import subprocess
from logger import Log

def create_crawler(crawler_root, crawler_name, query) :

    def crawler() :
        with Log.begin() as logger:
            logger.log("크롤러", "-------시작-------").attach_time()
            subprocess.call(['scrapy','crawl', crawler_name, '-a', query, '-a', 'top_tweet=True'], cwd=crawler_root)
            logger.log("크롤러", "완료").attach_time()

    return crawler