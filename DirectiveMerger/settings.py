from datetime import datetime, timedelta

#DATE
TODAY = datetime.today()

YESTERDAY = TODAY - timedelta(days=1)

SINCE = YESTERDAY

#CRAWLER
CRAWLER_ROOT_DIRECTORY = './TweetScraper/'

CRAWLER_NAME = 'TweetScraper'

CRAWLER_RESULT_PATH =  './TweetScraper/Data/tweet' # directory

CRAWLER_FILTERS = " " + " ".join([ 
    "filter:links", 
    "since:"+ SINCE.strftime("%Y-%m-%d")
    ]
)

CRAWLER_QUERY = 'query="역따 OR 선플' + CRAWLER_FILTERS

CRAWLER_TASK_INTERVAL = 3*60 # min * sec

#MERGER
MERGER_RESULT_PATH = './TweetScraper/Merge/directives.json' # json format output file

#LOGGER
LOGGER_RESULT_PATH = './TweetScraper/Merge/log.txt' 