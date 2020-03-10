
import settings
from termcolor import colored
from datetime import datetime

class Log :
    
    __instance = None
    __outstream = None

    @classmethod
    def getLogger(cls) :
        if cls.__instance is None :
            cls.__instance = cls()
        return cls.__instance

    @classmethod
    def begin(cls) :
        instance = cls.getLogger()
        return instance.__enter__()
    
    def __enter__(self) :
        if self.__outstream is None :
            self.__outstream = open(settings.LOGGER_RESULT_PATH, 'a')

        return self

    def __exit__(self, type, value, traceback) :
        self.__outstream.__exit__()
        self.__outstream = None

    def log(self, tag, msg, color='white') :
        output = colored("[{}] {}".format(tag, msg), color)
        print(output)
        self.__outstream.write(output + '\n')
        return self
    
    def attach_time(self) :
        self.log("@", datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'green')
        return self
