
import os
from logger import Log

def create_remover(target_directory) :

    def remover() :
        for filename in os.listdir(target_directory) :
            path = os.path.join(target_directory, filename)
            os.remove(path)

        with Log.begin() as logger:
            logger.log("리무버", "개별 지령이 제거되었습니다")

    return remover
