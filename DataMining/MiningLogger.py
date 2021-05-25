from datetime import datetime
import logging
from logging import handlers

class LoggerObject:
    level_relations = {
        'debug'     : logging.DEBUG,
        'info'      : logging.INFO,
        'warning'   : logging.WARNING,
        'error'     : logging.ERROR,
        'crit'      : logging.CRITICAL
    }

class MiningLogger(LoggerObject):
    
    def __init__(self, filename, level='info', when='M', backCount=888, fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        
        th.setFormatter(format_str)
        self.logger.addHandler(sh)
        self.logger.addHandler(th)

class MiningSaver(LoggerObject):
    def __init__(self, filename, level='info', when='H', backCount=888888888, fmt='%(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        sh = logging.StreamHandler()
        sh.setFormatter(format_str)
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')
        th.setFormatter(format_str)
        #self.logger.addHandler(sh)
        self.logger.addHandler(th)

minerlog     = MiningLogger('log/mining.log',level='info', when='D')