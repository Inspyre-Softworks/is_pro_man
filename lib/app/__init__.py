class ProjectMan:

    def start_logger(self):
        from ..common.logger import start

        name = self.__class__.__name__
        log = start(name=name, level='debug')
        return log


    def __init__(self):
        if __name__ == '__main__':
            print(self.__class__.__name__)
            self.App()


    class App:

        def __init__(self):
            self.my_name = self.__class__.__name__


        def name(self):
            return self.my_name


ProjectMan().App()
