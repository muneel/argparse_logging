from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO, ERROR, FileHandler, NullHandler
import traceback
import os
import argparse
import sys
'''
# type =  type to which the command-line argument should be converted
# help =  description of what the argument does.
# required = whether option is required
# nargs = for list of inputs
# default = value produced if the argument is absent from the command line.
# choices = list of the allowable values for the argument.
'''
# Argument Parser Funtion


def get_cli_args(args=None):
    parser = argparse.ArgumentParser(description='<Desicription of Script Here>')
    parser.add_argument('-s', '--server',
                        type=str,
                        help='server ip',
                        required='True')
    parser.add_argument('-p', '--port',
                        type=str,
                        help='port of the web server',
                        required=True,
                        nargs='+')
    parser.add_argument('-u', '--user',
                        type=str,
                        help='user name',
                        choices={'admin', 'user'},
                        default='root')
    # logging arguments
    parser.add_argument('-lv', '--loglevel',
                        type=str,
                        help='Log Level {INFO,DEBUG,ERROR} Default = INFO',
                        choices={'INFO', 'DEBUG', 'ERROR'},
                        default='INFO')
    parser.add_argument('-lt', '--logtype',
                        type=str,
                        help='Log to  {CONSOLE,FILE,BOTH,NONE} Default = CONSOLE',
                        choices={'CONSOLE', 'FILE', 'BOTH', 'NONE'},
                        default='CONSOLE')
    parser.add_argument('-lf', '--logfilename',
                        type=str,
                        help='Log filename Default = output.log',
                        default='output.log')
    results = parser.parse_args(args)
    results.port = results.port[0].split(",")
    return (results.server,
            results.port,
            results.user,
            results.loglevel,
            results.logtype,
            results.logfilename)
'''
# Logger
# logtype  : {'CONSOLE', 'FILE', 'BOTH', 'NONE'}
# level : {INFO, DEBUG, ERROR}
'''


class MLOGGER:

    @staticmethod
    def get_logger(name):
        if not name:
            raise ValueError('Name parameter can not be empty.')
        return MLOGGER(name)

    @staticmethod
    def __create_stream_handler(level):
        handler = StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(
            Formatter('%(asctime)s - %(levelname)s - %(instance_id)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
        return handler

    @staticmethod
    def __create_file_handler(level, filename):
        filename_path = str(os.path.dirname(os.path.realpath(__file__))) + '/' + str(filename)
        fileHandler = FileHandler(filename_path, mode='w')
        fileHandler.setLevel(level)
        fileHandler.setFormatter(
            Formatter('%(asctime)s - %(levelname)s - %(instance_id)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
        return fileHandler

    def __init__(self, name, level=INFO, logtype='CONSOLE', filename=None):
        # logtype  : {'CONSOLE', 'FILE', 'BOTH', 'NONE'}
        # level : {INFO, DEBUG, ERROR}
        self.user_variables = {}
        self.user_variables['instance_id'] = self.__class__.__name__
        self.logger = getLogger(name)
        self.logger.setLevel(level)
        if logtype == 'CONSOLE':
            self.logger.addHandler(MLOGGER.__create_stream_handler(level))
        elif logtype == 'FILE':
            if filename is not None:
                self.logger.addHandler(MLOGGER.__create_file_handler(level, filename))
            else:
                raise ValueError('filename cannot be empty')
                sys.exit()
        elif logtype == 'BOTH':
            self.logger.addHandler(MLOGGER.__create_stream_handler(level))
            if filename is not None:
                self.logger.addHandler(MLOGGER.__create_file_handler(level, filename))
            else:
                raise ValueError('filename cannot be empty')
                sys.exit()
        elif logtype == 'NONE':
            self.logger.addHandler(NullHandler())

    def __set_message(self, message):
        tb = traceback.extract_stack()
        return(tb[1][2] + ' - ' + message)

    def debug(self, message):
        self.logger.debug(self.__set_message(message), extra=self.user_variables)

    def info(self, message):
        self.logger.info(self.__set_message(message), extra=self.user_variables)

    def warn(self, message):
        self.logger.warn(self.__set_message(message), extra=self.user_variables)

    def error(self, message):
        self.logger.error(self.__set_message(message), extra=self.user_variables)


class tester(MLOGGER):

    def __init__(self, level='INFO', logtype='CONSOLE', filename='output.log'):
        MLOGGER.__init__(self, 'test', level=level, logtype=logtype, filename=filename)

    def testmethod(self):
        self.error('error test')
        self.debug('debug test')
        self.warn('warn test')
        self.info('info test')

if __name__ == '__main__':
    h, p, u, lv, lt, lf = get_cli_args(sys.argv[1:])
    print 'h =', h
    print 'p =', p
    print 'u =', u
    print 'lv=', lv
    print 'lt=', lt
    print 'lf=', lf
    t = tester(level=lv, logtype=lt, filename=lf)
    t.testmethod()
    logger = MLOGGER('Test', level=lv, logtype=lt, filename=lf)
    logger.debug('debug test')
    logger.info('info test')
    logger.warn('warn test')
    logger.error('error test')
