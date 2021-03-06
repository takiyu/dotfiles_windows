#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
try:
    # Python 3
    import urllib.parse as urllib_parse
    import urllib.request as urllib_request
    from html.parser import HTMLParser
except ImportError:
    # Python 2
    import urllib as urllib_parse
    import urllib2 as urllib_request
    from HTMLParser import HTMLParser

USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) ' + \
             'Gecko/20100101 Firefox/40.0'


class GtransParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.depth = 0
        self.results = []

    def handle_starttag(self, tag, attrs):
        if tag == "span":
            if self.depth > 0:
                self.depth += 1
            else:
                for attr in attrs:
                    if attr == ('id', 'result_box'):
                        self.depth = 1

    def handle_endtag(self, tag):
        if tag == "span":
            if self.depth > 0:
                self.depth -= 1

    def handle_data(self, data):
        if self.depth > 0:
            self.results.append(data)

    def get_result(self):
        return '\n'.join(self.results)


def gtrans_search(src_lang, tgt_lang, src_text):
    # Encode for URL
    src_text = urllib_parse.quote_plus(src_text)

    # Header and URL
    headers = {'User-Agent': USER_AGENT}
    url = 'https://translate.google.com/?ie=UTF-8&oe=UTF-8&sl=' + src_lang + \
          '&tl=' + tgt_lang + '&text=' + src_text

    # Access to translation website
    try:
        req = urllib_request.Request(url, data=None, headers=headers)
        response = urllib_request.urlopen(req)
        html = response.read()
    except Exception:
        return 'Error: Failed to access google translation website.'
    finally:
        try:
            response.close()
        except NameError:
            pass

    html = html.decode('utf-8')

    # Parse html
    parser = GtransParser()
    parser.feed(html)
    parser.close()

    return parser.get_result()


def fetch_args_vim():
    import vim
    src_lang = vim.eval('g:gtransweb_src_lang')
    tgt_lang = vim.eval('g:gtransweb_tgt_lang')
    src_text = vim.eval('s:src_text')
    return src_lang, tgt_lang, src_text


def return_result_vim(tgt_text):
    import vim
    tgt_text = tgt_text.replace("'", "''")
    vim.command("let s:tgt_text = '" + tgt_text + "'")


if __name__ == "__main__":
    # Argument
    parser = argparse.ArgumentParser(description='gtrans-web')
    parser.add_argument('--mode', choices=['vim', 'alone'], default='vim')
    parser.add_argument('--src_lang', type=str, default='auto',
                        help='Source language in `alone` mode')
    parser.add_argument('--tgt_lang', type=str, default='auto',
                        help='Target language in `alone` mode')
    parser.add_argument('--src_text', type=str, default='This is a pen.',
                        help='Srouce text in `alone` mode')
    args = parser.parse_args()

    # Text and language information
    if args.mode == 'vim':
        src_lang, tgt_lang, src_text = fetch_args_vim()
    else:
        src_lang, tgt_lang, src_text = \
            args.src_lang, args.tgt_lang, args.src_text

    # Access translate.google.com
    tgt_text = gtrans_search(src_lang, tgt_lang, src_text)

    # Result
    if args.mode == 'vim':
        return_result_vim(tgt_text)
    else:
        print(tgt_text)
