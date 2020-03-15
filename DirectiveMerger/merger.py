
import os
import re
import json
import settings
import requests
from html.parser import HTMLParser
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
        self.origin = None
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
            'origin' : self.origin,
            'director' : self.director,
            'datetime' : self.datetime,
            'text' : self.text,
            'targets' : self.targets,
        }

class Target :

    def __init__(self) :
        self.jsonformat = None
        self.helpkey = None
        self.upvote = None
        self.url = None
        self.articleurl = None
        self.articletitle = None

    def json(self) :
        if self.jsonformat is not None :
            return self.jsonformat
        else :
            raise Exception('is not jsonated')

    def jsonate(self) :
        self.jsonformat = {
                'helpkey' : self.helpkey,
                'upvote' : self.upvote,
                'url' : self.url,
                'articleurl' : self.articleurl,
                'articletitle' : self.articletitle,
            }

class DirectiveParser :

    @classmethod
    def parse_raws(cls, raw_directives) :
        directives = list()
        for raw_directive in raw_directives :
            directive = cls.parse_raw(raw_directive)
            if len(directive['targets']) > 0 :
                directives.append(directive)
        return directives

    @classmethod
    def parse_raw(cls, raw_directive) :
        directive = Directive()
        cls.__parse(directive, raw_directive)
        return directive.json()

    @classmethod
    def __parse(cls, directive, raw_directive) :
        directive.origin = 'http://twitter.com' + raw_directive['url']
        directive.director = '@' + raw_directive['usernameTweet']
        directive.datetime = raw_directive['datetime']
        directive.text = cls.__trimmer(raw_directive['text'])
        directive.targets = TargetParser.parse(directive.text)
        
        directive.jsonate()

    @classmethod
    def __trimmer(cls, text) :
        trim = text.replace(" ", "").replace("\n", "")
        return trim

class TargetParser :

    target_pattern = re.compile(r"([a-zA-Z0-9ㄱ-ㅎ가-힣!\?\(\)]*)(https?://[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b[-a-zA-Z0-9()@:%_\+.~#?&//=,]*)")
    articleurl_pattern = re.compile(r"https?://.*naver.*oid=([0-9]+).*aid=([0-9]+).*")

    @classmethod
    def parse(cls, text) :
        return cls.__parse(text)

    @classmethod
    def __parse(cls, text) :
        targets = list()
        matched_target = re.findall(cls.target_pattern, text)
        upfirst = True
        for helpkey, url in matched_target :
            if cls.__check_url_validation(url) == True :
                target = Target()
                target.helpkey = helpkey
                target.url = url
                upfirst, target.upvote = cls.__extract_upvote(upfirst, helpkey)
                target.articleurl = cls.__extract_article_url(url)
                target.articletitle = cls.__extract_article_title(target.articleurl)

                target.jsonate()
                targets.append(target.json())
        return targets

    @classmethod
    def __extract_upvote(cls, upfirstmode, helpkey) :
        upfirst = upfirstmode
        if upfirst :
            if "역따" in helpkey or "신고" in helpkey or "👎" in helpkey:
                upfirst = False
                upvote = False
            else :
                upvote = True
        else :
            if "선플" in helpkey or "많이" in helpkey or "👍" in helpkey:
                upfirst = True
                upvote = True
            else :
                upvote = False
        return upfirst, upvote

    @classmethod
    def __check_url_validation(cls, url) :
        return ("naver" in url) or ("daum" in url)

    @classmethod
    def __extract_article_url(cls, comment_url) :
        articleurl = ""
        if "naver" in comment_url :
            matched_article_id = re.findall(cls.articleurl_pattern, comment_url)
            for oid, aid in matched_article_id : 
                articleurl = cls.__url_string("http://m.news.naver.com/read.nhn", oid=oid, aid=aid)
        return articleurl

    @classmethod
    def __extract_article_title(cls, article_url) :
        article_parser = TitleParser()
        try :
            article_html = requests.get(article_url).text
            article_parser.feed(article_html)
        except :
            return ''
        return article_parser.get_title()

    @classmethod
    def __url_string(cls, domain, **params) :
        querystring = "?"
        for key, val in params.items() :
            querystring += "{}={}&".format(key, val)
        return domain + querystring

class TitleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.match = False
        self.title = ''

    def handle_starttag(self, tag, attributes):
        self.match = True if tag == 'title' else False

    def handle_data(self, data):
        if self.match:
            self.title = data
            self.match = False

    def get_title(self) :
        return self.title