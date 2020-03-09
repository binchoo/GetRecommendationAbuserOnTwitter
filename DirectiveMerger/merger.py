
import os
import json
from logger import Log

def create_merger(target_directory, output_file_path) :
    
    def merger() :
        contents = get_contents_of(target_directory)
        with open(output_file_path, 'w') as f :
            json.dump(contents, f, ensure_ascii=False) #이 옵션은 한글을 바로 식별할 수 있게 해준다
        with Log.begin() as logger:
            logger.log("머져", "{}개 지령이 취합되었습니다".format(len(contents)))
        
    return merger

def get_contents_of(target_path) :
    contents = []
    for filename in os.listdir(target_path) :
        path = os.path.join(target_path, filename)
        with open(path) as f :
            contents.append(json.load(f, encoding=''))
    return contents