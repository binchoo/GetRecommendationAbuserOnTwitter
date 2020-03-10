
import subprocess
from logger import Log

def create_crawler(crawler_root, crawler_name, query) :

    def crawler() :
        with Log.begin() as logger:
            logger.log("크롤러", "-------시작-------", color='red').attach_time()
            subprocess.call(['scrapy','crawl', crawler_name, '-a', query], cwd=crawler_root)
            logger.log("크롤러", "완료", color='red').attach_time()

    return crawler