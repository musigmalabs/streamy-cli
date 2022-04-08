from termcolor import colored


def color(msg, color, attrs=[]):
    return colored(msg, color, attrs=attrs)


class TermPrinter:
    def __init__(self) -> None:
        pass

    @staticmethod
    def yellow(msg):
        print(color(msg, 'yellow'))
    
    @staticmethod
    def red(msg):
        print(color(msg, 'red'))
    
    @staticmethod
    def green(msg):
        print(color(msg, 'green'))
    
    @staticmethod
    def magenta(msg):
        print(color(msg, 'magenta'))
    
    @staticmethod
    def cyan(msg):
        print(color(msg, 'cyan'))
