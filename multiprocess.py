from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager, BaseProxy

class Foo:
    def f(self):
        print('you call class Foo.f()')
    def g(self):
        print('you call class Foo.g()')
    def _h(self):
        print('you called class Foo._h()')



