# -*- coding:utf-8 -*-

from Sloth.Utils.router import _PathMatch


if __name__ == '__main__':
    url = '/hello/<name>'
    match = _PathMatch(url)
    print(match.regex)

    text = '/hello/123'
    print(match.regex.match(text))
    print(match.regex.match(text).groupdict())
