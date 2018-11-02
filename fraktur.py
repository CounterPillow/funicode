#!/usr/bin/env python3
import argparse
import sys
from itertools import chain


def alpha_iter(start_c, end_c):
    return [chr(x) for x in range(ord(start_c), ord(end_c) + 1)]


def normal_fraktur_mapping():
    to_fraktur = {}
    for alpha, frak in zip(chain(alpha_iter('A', 'Z'), alpha_iter('a', 'z')),
                           alpha_iter('𝔄', '𝔷')):
        to_fraktur[alpha] = frak
    # Fixups because Unicode is awful
    for alpha, frak in [('C', 'ℭ'), ('H', '\u210c'), ('I', '\u2111'),
                        ('R', '\u211c'), ('Z', '\u2128')]:
        to_fraktur[alpha] = frak
    return to_fraktur


def bold_fraktur_mapping():
    to_fraktur_bold = {}
    for alpha, frak in zip(chain(alpha_iter('A', 'Z'), alpha_iter('a', 'z')),
                           alpha_iter('𝕬', '𝖟')):
        to_fraktur_bold[alpha] = frak
    return to_fraktur_bold


def main():
    to_fraktur = normal_fraktur_mapping()
    to_fraktur_bold = bold_fraktur_mapping()

    parser = argparse.ArgumentParser(description='Converts normal text to '
                                                 'Unicode fraktur')
    in_grp = parser.add_mutually_exclusive_group(required=True)
    in_grp.add_argument('text', nargs='?', metavar='TEXT', type=str)
    in_grp.add_argument('-i', '--stdin', action='store_true',
                        help='Read from standard input')
    parser.add_argument('-b', '--bold', default=False, action='store_true',
                        help='Output bold fraktur (default: %(default)s)')
    nl_grp = parser.add_mutually_exclusive_group()
    nl_grp.add_argument('--newline', dest='newline', action='store_true',
                        default=sys.stdout.isatty(),
                        help='Print newline at the end of output')
    nl_grp.add_argument('-n', '--no-newline', default=not sys.stdout.isatty(),
                        action='store_false', dest='newline',
                        help='Omit newline at the end of output (default: '
                             'newline added if on a tty, otherwise omitted)')
    args = parser.parse_args()

    mapping = to_fraktur_bold if args.bold else to_fraktur
    in_text = sys.stdin.read() if args.stdin else args.text
    for c in in_text:
        sys.stdout.write(mapping[c] if c in mapping else c)
    if args.newline:
        sys.stdout.write('\n')


if __name__ == '__main__':
    main()
