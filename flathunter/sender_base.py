import logging


class SenderBase:
    __log__ = logging.getLogger()

    def __init__(self):
        self.__log__.debug('init')
        pass

    def send_msg(self, msg):
        self.__log__.debug('Base class called o.O send msg: %s' % msg)
        pass

