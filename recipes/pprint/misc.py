"""
Miscellaneous functions for pretty printing
"""

# std libs
import os
import functools

# relative libs
from ..introspection import get_class_that_defined_method


def seq_repr_trunc(seq, max_items=10, edge_items=1, sep=','):
    """

    Parameters
    ----------
    seq
    max_items
    edge_items
    sep

    Returns
    -------

    """

    # if len(seq) <= max_items:
    #     return repr(seq)

    brackets = {set: '{}',
                list: '[]',
                tuple: '()'}.get(type(seq), '[]')
    if len(seq) <= max_items:
        return sep.join(map(repr, seq)).join(brackets)

    return ', ... '.join((sep.join(map(repr, seq[:edge_items])),
                          sep.join(map(repr, seq[-edge_items:]))
                          )).join(brackets)


def method(func, show_class=True, submodule_depth=1):
    """
    Get a nice string representing the function.

    Parameters
    ----------
    func: Callable
        The callable to represent
    show_class: bool
        whether to show the class name eg: 'MyClass.method'
    submodule_depth: int
        number of sub-module levels to show.
        eg: 'foo.sub.MyClass.method'  for depth of 2

    Returns
    -------
    str

    """

    if show_class:
        cls = get_class_that_defined_method(func)
    else:
        cls = None
        submodule_depth = 0

    if cls is None:
        # handle partial
        if isinstance(func, functools.partial):
            func = func.func
            # represent missing arguments with unicode centre dot
            cdot = '·'  # u'\u00B7'
            argstr = str(func.args).strip(')') + ', %s)' % cdot
            return 'partial(%s%s)' % (method(func.func), argstr)
        # just a plain function # FIXME: module???
        return func.__name__
    else:
        # a class method
        # FIXME: this gives the wrong module.submodule structure if
        #  show_class=True
        parents = cls.__module__.split('.')
        prefixes = parents[:-submodule_depth - 1:-1]
        parts = prefixes + [cls.__name__, func.__name__]
        return '.'.join(parts)


def banner(text, swoosh='=', width=80, title=None, align='^'):
    """

    Parameters
    ----------
    text
    swoosh
    width
    title
    align

    Returns
    -------

    """

    swoosh = swoosh * width
    if title is None:
        pre = swoosh
    else:
        pre = overlay(' ', swoosh, align)

    banner = os.linesep.join((pre, text, swoosh, ''))
    return banner


def overlay(text, background='', alignment='^', width=None):
    """overlay text on background using given alignment."""

    # TODO: verbose alignment name conversions. see motley.table.get_alignment

    if not (background or width):  # nothing to align on
        return text

    if not background:
        background = ' ' * width  # align on clear background
    elif not width:
        width = len(background)

    if len(background) < len(text):  # pointless alignment
        return text

    # do alignment
    if alignment == '<':  # left aligned
        overlaid = text + background[len(text):]
    elif alignment == '>':  # right aligned
        overlaid = background[:-len(text)] + text
    elif alignment == '^':  # center aligned
        div, mod = divmod(len(text), 2)
        pl, ph = div, div + mod
        # start and end indeces of the text in the center of the background
        idx = width // 2 - pl, width // 2 + ph
        # center text on background
        overlaid = background[:idx[0]] + text + background[idx[1]:]
    else:
        raise ValueError('Alignment character %r not understood' % alignment)
    return overlaid
