# Function pcre_detidy to convert xmode regex string to non-xmode.
# Rev: 20160225_1800
import re


def detidy_cb(m):
    if m.group(2):
        return m.group(2)
    if m.group(3):
        return m.group(3)
    return ""


def terse(retext):
    """
    Go from verbose format multiline regex to single line terse representation

    """
    # https://stackoverflow.com/a/35641837/1098683
    decomment = re.compile(
        r"""(?#!py/mx decomment Rev:20160225_1800)
        # Discard whitespace, comments and the escapes of escaped spaces and hashes.
          ( (?: \s+                  # Either g1of3 $1: Stuff to discard (3 types). Either ws,
            | \#.*                   # or comments,
            | \\(?=[\r\n]|$)         # or lone escape at EOL/EOS.
            )+                       # End one or more from 3 discardables.
          )                          # End $1: Stuff to discard.
        | ( [^\[(\s#\\]+             # Or g2of3 $2: Stuff to keep. Either non-[(\s# \\.
          | \\[^# Q\r\n]             # Or escaped-anything-but: hash, space, Q or EOL.
          | \(                       # Or an open parentheses, optionally
            (?:\?\#[^)]*(?:\)|$))?   # starting a (?# Comment group).
          | \[\^?\]? [^\[\]\\]*      # Or Character class. Allow unescaped ] if first char.
            (?:\\[^Q][^\[\]\\]*)*    # {normal*} Zero or more non-[], non-escaped-Q.
            (?:                      # Begin unrolling loop {((special1|2) normal*)*}.
              (?: \[(?::\^?\w+:\])?  # Either special1: "[", optional [:POSIX:] char class.
              | \\Q       [^\\]*     # Or special2: \Q..\E literal text. Begin with \Q.
                (?:\\(?!E)[^\\]*)*   # \Q..\E contents - everything up to \E.
                (?:\\E|$)            # \Q..\E literal text ends with \E or EOL.
              )        [^\[\]\\]*    # End special: One of 2 alternatives {(special1|2)}.
              (?:\\[^Q][^\[\]\\]*)*  # More {normal*} Zero or more non-[], non-escaped-Q.
            )* (?:\]|\\?$)           # End character class with ']' or EOL (or \\EOL).
          | \\Q       [^\\]*         # Or \Q..\E literal text start delimiter.
            (?:\\(?!E)[^\\]*)*       # \Q..\E contents - everything up to \E.
            (?:\\E|$)                # \Q..\E literal text ends with \E or EOL.
          )                          # End $2: Stuff to keep.
        | \\([# ])                   # Or g3of3 $6: Escaped-[hash|space], discard the escape.
        """, re.VERBOSE | re.MULTILINE)
    return re.sub(decomment, detidy_cb, retext)


if __name__ == '__main__':
    test_text = r"""
            [0-9]            # 1 Number
            [A-Z]            # 1 Uppercase Letter
            [a-y]            # 1 lowercase, but not z
            z                # gotta have z...
            """
    print(terse(test_text))
