"""
Base classes for extensible decorators
"""

import types
import functools
import logging


def inclass(meth):
    return '.' in str(meth)


class DecoratorBase(object):
    """A picklable decorator"""

    def __init__(self, func):
        self.func = func
        # Update this class to look like the wrapped function
        functools.update_wrapper(self, func)

    def __call__(self, *args, **kws):
        # Default null decorator
        return self.func(*args, **kws)


# class ArgDecor():
#     def __init__(self, *args, **kws):
#         """
#         Inherited classes can implement stuff here, for example what to do with the args and kws passed
#         to the constructor
#         """
#         logging.debug('__init__ %s: %s; %s', self, args, kws)
#
#     def __call__(self, *args, **kws):
#         logging.debug('calling with %s; %s', args, kws)
#
#         if self.wrapped is None:
#             # The wrapped function has not yet been created - arguments passed to decorator constructor
#             logging.debug('not wrapped yet. creating wrapper. args: %s; kws: %s' % (args, kws))
#             func = args[0]
#             return self.make_wrapper(func)  # return the wrapped function
#
#         # The wrapped function has already been created
#         logging.debug('calling wrapped %s %s %s' % (self, args, kws))
#         return self.wrapped(*args, **kws)  # call the wrapped function
#
#     def make_wrapper(self, func):
#         """Null wrapper. To be implemented by subclass"""
#         print('YO'*100)
#         logging.debug('wrapping %s', func)
#         # logging.debug(('!'*10)+str(getattr(func, '__self__', None)))
#
#         # for decorated methods: make wrapped function MethodType to avoid errors downstream
#         if inclass(func):
#             func = types.MethodType(func, self)
#
#         # update __call__ method to look like func
#         functools.update_wrapper(self, func)
#
#         return func


class OptionalArgumentsDecorator(object):
    """
    Decorator class with optional arguments. Can be pickle, unlike function based decorators / factory.

    There are two distinct use cases
    1) No explicit arguments provided to decorator.
    eg.:
    @decorator
    def foo():
       ...
    In this case the wrapper will be built upon construction in `__new__`

    2) Explicit arguments and/or keywords provided to decorator.
    eg.:
    @decorator('hello', foo='bar')
    def baz():
        ...
    In this case the wrapper will be built upon first call to function

    NOTE: cannot use this class like:
    @decorator(some_callable)

    """

    # FIXME: this class is an ANTI-PATTERN!!!!

    def __new__(cls, *args, **kws):
        logging.debug('__new__ %s: %s; %s' % (cls, args, kws))
        ins = object.__new__(cls)

        if len(args) == 1 and callable(args[0]):
            # No optional arguments provided to decorator.
            # eg. usage:
            # @decorator
            # def foo(): pass
            logging.debug('No explicit arguments provided to decorator')
            func = args[0]
            cls.__init__(ins)
            ins.wrapped = ins.make_wrapper(func)
        else:
            ins.wrapped = None
            # (optional) arguments provided to decorator.
            # eg. usage:
            # @decorator('hello world', bar=None)
            # def foo(): pass
            logging.debug('Arguments given: %s; %s' % (args, kws))
            # Don't know the function yet, so can't create the wrapper
            # will create wrapper upon __call__

        return ins

    def __init__(self, *args, **kws):
        """
        Inherited classes can implement stuff here, for example what to do with the args and kws passed
        to the constructor
        """
        logging.debug('__init__ %s: %s; %s' % (self, args, kws))
        # if self.wrapped is None:

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def __call__(self, *args, **kws):
        logging.debug('calling with %s; %s', args, kws)

        if self.wrapped is None:
            # The wrapped function has not yet been created - arguments passed to decorator constructor
            logging.debug(
                'not wrapped yet. creating wrapper. args: %s; kws: %s' % (
                args, kws))
            func = args[0]
            return self.make_wrapper(func)  # return the wrapped function

        # The wrapped function has already been created
        logging.debug('calling wrapped %s %s %s' % (self, args, kws))
        return self.wrapped(*args, **kws)  # call the wrapped function

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def make_wrapper(self, func):
        """Null wrapper. To be implemented by subclass"""
        logging.debug('wrapping %s', func)
        # logging.debug(('!'*10)+str(getattr(func, '__self__', None)))

        # for decorated methods: make wrapped function MethodType to avoid errors downstream
        if inclass(func):
            func = types.MethodType(func, self)

        # update __call__ method to look like func
        functools.update_wrapper(self, func)

        return func


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)

    class Foo():
        @OptionalArgumentsDecorator
        def method1(self):
            print('method1')

        @OptionalArgumentsDecorator()
        def method2(self):
            print('method2')

        @OptionalArgumentsDecorator(hello='world')
        def method3(self):
            print('method3')


    @OptionalArgumentsDecorator
    def foo1():
        print('foo1')


    @OptionalArgumentsDecorator()
    def foo2():
        print('foo2')


    # test
    foo = Foo()
    foo.method1()
    foo.method2()
    foo.method3()

    foo1()
    foo2()
