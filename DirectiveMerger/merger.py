
import os
import re
import json
import settings
from logger import Log

def create_merger(target_directory, output_file_path) :
    
    def merger() :
        contents = get_contents_of(target_directory)
        directives = DirectiveParser.parse_raws(contents)

        with open(output_file_path, 'w') as f :
            json.dump(directives, f, ensure_ascii=False) #이 옵션은 한글을 바로 식별할 수 있게 해준다
        
        with Log.begin() as logger:
            logger.log("머져", "{}개 지령이 취합되었습니다".format(len(contents)), color='red')
        
    return merger

def get_contents_of(target_path) :
    contents = []
    for filename in os.listdir(target_path) :
        path = os.path.join(target_path, filename)
        with open(path) as f :
            contents.append(json.load(f))
    return contents


class Directive :

    def __init__(self) :
        self.jsonformat = None
        self.director = None
        self.datetime = None
        self.text = None
        self.targets = None

    def json(self) :
        if self.jsonformat is not None :
            return self.jsonformat
        else :
            raise Exception('is not jsonated')

    def jsonate(self) :
        self.jsonformat = {
            'director' : self.director,
            'datetime' : self.datetime,
            'text' : self.text,
            'targets' : self.targets,
        }

class DirectiveParser :

    target_pattern = re.compile(r"([a-zA-Z0-9가-힣]*)(https?://[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=,]*)")
    articleurl_pattern = re.compile(r"https?://.*naver.*oid=([0-9]+).*aid=([0-9]+).*")

    @classmethod
    def parse_raw(cls, raw_directive) :
        directive = Directive()
        cls.__parse(directive, raw_directive)
        return directive.json()
    
    @classmethod
    def parse_raws(cls, raw_directives) :
        directives = list()
        for raw_directive in raw_directives :
            directives.append(cls.parse_raw(raw_directive))
        return directives

    @classmethod
    def __parse(cls, directive, raw_directive) :
        directive.director = raw_directive['usernameTweet']
        directive.datetime = raw_directive['datetime']
        directive.text = cls.__trimmer(raw_directive['text'])
        directive.targets = cls.__extract_targets(directive.text)
        
        directive.jsonate()

    @classmethod
    def __trimmer(cls, text) :
        trim = text.replace(" ", "").replace("\n", "")
        return trim

    @classmethod
    def __extract_targets(cls, text) :
        targets = list()
        matched_target = re.findall(cls.target_pattern, text)
        for helpkey, url in matched_target :
            articleurl = cls.__extract_article_url(url)
            targets.append({
                'helpkey' : helpkey,
                'url' : url,
                'articleurl' : articleurl,
            })
        return targets

    @classmethod
    def __extract_article_url(cls, comment_url) :
        articleurl = ""
        if "naver" in comment_url :
            matched_article_id = re.findall(cls.articleurl_pattern, comment_url)
            for oid, aid in matched_article_id : 
                articleurl = cls.__url_string("https://m.news.naver.com/read.nhn", oid=oid, aid=aid)
        return articleurl

    @classmethod
    def __url_string(cls, domain, **kwargs) :
        querystring = "?"
        for key, val in kwargs.items() :
            querystring += "{}={}&".format(key, val)
        return domain + querystring