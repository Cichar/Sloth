# -*- coding:utf-8 -*-

from Sloth.Utils.router import _PathMatch
import urllib.parse


if __name__ == '__main__':
    url = '/hello/(\d+)'
    match = _PathMatch(url)
    print(match.regex)
    print(match.regex.groupindex)
    print()

    text = '/hello/123'
    print(match.regex.match(text))
    print(match.regex.match(text).groups())
    print(match.match(text))
    print()

    url = '/hello/<name>'
    match = _PathMatch(url)
    print(match.regex)
    print(match.regex.groupindex)
    print()

    text = '/hello/123'
    print(match.regex.match(text))
    print(match.regex.match(text).groupdict())
    print(match.match(text))
    print()

    url = '/hello/<name>/(\d+)'
    match = _PathMatch(url)
    print(match.regex)
    print(match.regex.groupindex)
    print()

    text = '/hello/sloth/123'
    print(match.regex.match(text))
    print(match.regex.match(text).groups())
    print(match.match(text))
    print()
