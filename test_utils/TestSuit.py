from sys import stderr
import traceback


class TestSuit:
    def __call__(self, classtype=None):
        self.accused_exceptions = []
        functions = [(name, func)
                     for name, func in self.__class__.__dict__.items()
                     if 'test' in name]
        print(f'{self.__class__.__name__} suit case:')
        for test_name, func in functions:
            print('\t', end='')
            try:
                self.set_test_name(test_name)
                func(self)
                print(f'{test_name} is \033[42mpassed\033[0m')  # ]]
            except Exception:
                print(f'{test_name} is \033[41mnot passed\033[0m')  # ]]
                self.accused_exceptions.append(f'{traceback.format_exc()}')
        if self.accused_exceptions:
            for e in self.accused_exceptions:
                print(e, file=stderr)

    def get_test_name(self):
        return self.current_func_name

    def set_test_name(self, test_name):
        self.current_func_name = test_name

    def get_test_suit_name(self):
        return self.__class__.__name__

    def assert_true(self, pred, message=None):
        if pred:
            self.raise_exception('Assert true exception')

    def assert_eq(self, x, y, message=None):
        if x != y:
            self.raise_exception(f'Assert equals exception: {x} != {y}')

    def assert_raises(self, func, message=None):
        exception = None
        try:
            func()
        except Exception as e:
            exception = e

        if exception is None:
            self.raise_exception(
                    'Assert raises exception: no exception was raised')

    def raise_exception(self, message):
        test_suit_name = self.get_test_suit_name()
        test_name = self.get_test_name()
        exception_message = f'In {test_suit_name} at {test_name}:\n{message}'
        raise Exception(exception_message)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
