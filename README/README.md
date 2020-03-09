# Get Recommendation Abuser On Twitter!

## 목적

- 트위터에서 포털 사이트 뉴스 댓글의 추천 수 조작을 요청하는 최신 지령들을 크롤링하고, 하나의 JSON 파일로 취합하여 제공합니다. 추천 수 조작 행위를 모니터링하는 RESTful API 구현을 위한 기저 로직으로 이용할 목적입니다.
- 크롤링 툴은 [jonbakerfish/TweetScraper](https://github.com/jonbakerfish/TweetScraper) 를 이용합니다.
- 본 레포지토리는 크롤링 된 개별 결과물을 하나의 파일로 합치고 이 과정을 주기적으로 반복하는 로직을 덧붙인 것입니다.
- [jonbakerfish/TweetScraper](https://github.com/jonbakerfish/TweetScraper)는 잘 정의된 트위터 크롤링 툴로 생각됩니다. settings를 손보면 트위터에서 필요한 정보를 긁는 데 이용할 수 있습니다. 



## 실행 준비

레포지토리 루트 디렉토리에서 (jonbakerfinsh/TwetScraper 인용)

```bash
$ cd ./TweetScraper/
$ pip install -r requirements.txt  #add '--user' if you are not root
$ scrapy list
$ #If the output is 'TweetScraper', then you are ready to go.
```

## 실행

레포지토리의 루트 디렉토리에서

```bash
python ./DirectiveMerger/main.py
```

## 결과물

- `./TweetScraper/Data/tweet/` 에 개별적인 지령이 JSON 형태로 **임시 저장**됩니다. 병합 작업 후 전부 제거됩니다.

- `./TweetScraper/Merge/directives.log` 에는 크롤링 된 최신 지령들이 취합되어 JSON 형태로 저장됩니다.

  ![img0](/Users/mac/Documents/jjb/OneDrive/6.5학기/트위터/README/img0.png)

- `./TweetScraper/Merge/log.txt` 는 크롤러 동작을 간단히 로깅합니다.

## 종료

크롤러는 강제종료 하기 전까지 지정된 주기로 반복적인 크롤링을 합니다. `ctrl+c` 로 종료하십시오.



## 세팅

`./DirectiveMerger/settings.py`

```python

#CRAWLER
CRAWLER_ROOT_DIRECTORY = './TweetScraper/'

CRAWLER_NAME = 'TweetScraper'

CRAWLER_RESULT_PATH =  './TweetScraper/Data/tweet' # directory

CRAWLER_QUERY = 'query="역따 filter:links"'

CRAWLER_TASK_INTERVAL = 3*60*1000 # min * sec * millis

#MERGER
MERGER_RESULT_PATH = './TweetScraper/Merge/directives.json' # json format output file

#LOGGER
LOGGER_RESULT_PATH = './TweetScraper/Merge/log.txt' 
```

- `CRAWLER_QUERY` 를 변경하면 원하는 정보를 검색할 수 있습니다. 사용할 수 있는 쿼리는 [jonbakerfish/TweetScraper](https://github.com/jonbakerfish/TweetScraper) 를 참고합니다.
- `CRAWLER_TASK_INTERVAL` 는 크롤링 동작 주기를 의미합니다.
- `MERGER_RESULT_PATH` 는  취합된 트윗을 저장할 파일을 지정합니다.
- `LOGGER_RESULT_PATH` 는 로그를 저장할 파일을 지정합니다.
- 언급하지 않은 변수는 변경하지 않습니다.