
import crawler, merger, remover
import settings
import time

directive_crawler = crawler.create_crawler(settings.CRAWLER_ROOT_DIRECTORY, settings.CRAWLER_NAME, settings.CRAWLER_QUERY)
directive_merger = merger.create_merger(settings.CRAWLER_RESULT_PATH, settings.MERGER_RESULT_PATH)
directive_remover = remover.create_remover(settings.CRAWLER_RESULT_PATH)

def task() :
        directive_remover()
        directive_crawler()
        directive_merger()

def task_looper(task, millis) :

    def looping_task(*args, **kwargs):
        while True :
            task(*args, **kwargs)
            time.sleep(millis)

    return looping_task

if __name__ == '__main__' :
    do = task_looper(task, settings.CRAWLER_TASK_INTERVAL)
    do()
