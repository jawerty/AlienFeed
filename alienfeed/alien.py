#!/usr/bin/env python

import argparse
import math
import os
import random
from subprocess import call
import sys
from textwrap import TextWrapper
import webbrowser

import praw


USER_AGENT = ('AlienFeed v0.3.1 by u/jw989 seen on '
              'Github http://github.com/jawerty/AlienFeed')

r = praw.Reddit(user_agent=USER_AGENT)


class TerminalColor(object):
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    SUBTEXT = '\033[90m'
    INFO = '\033[96m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

color = TerminalColor()


class LinkType(object):
    NSFW = '[NSFW]'
    POST = '[POST]'
    PIC = '[PIC]'
    ALBUM = '[ALBUM]'
    VIDEO = '[VIDEO]'


def get_link_types(link):
    types = []
    image_types = ('jpg', 'jpeg', 'gif', 'png')
    image_hosts = ('imgur', 'imageshack', 'photobucket', 'beeimg')

    if link.url == link.permalink:
        # link is a post
        types.append(color.INFO + LinkType.POST + color.ENDC)
    elif link.url.split('.')[-1].lower() in image_types:
        # is it an image?
        types.append(color.OKGREEN + LinkType.PIC + color.ENDC)
    elif link.domain.split('.')[-2].lower() in image_hosts:
        # supposedly for an album, can also be a single image
        types.append(color.OKGREEN + LinkType.ALBUM + color.ENDC)
    elif link.media:
        # it's a video
        types.append(color.OKGREEN + LinkType.VIDEO + color.ENDC)

    if link.over_18:
        types.append(color.FAIL + LinkType.NSFW + color.ENDC)

    return ' '.join(types)

class _parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(color.FAIL +
                        '\nAlienFeed error: %s\n' % (message + color.ENDC))
        self.print_help()
        sys.exit(2)

def subreddit_viewer(generator):
    links = submission_getter(generator, verbose=True)

def submission_getter(generator, memo=[], verbose=False):
    links = []
    scores = []
    subreddits = set()

    for x, link in enumerate(generator):
        memo.append(link.url)
        if verbose:
            links.append(link)
            scores.append(link.score)
            subreddits.add(str(link.subreddit))

    if not verbose:
        return memo

    count_width = int(math.log(len(links), 10)) + 1
    score_width = len(str(max(scores)))
    fmt = {'arrow': ' -> '}

    indent = ' ' * (count_width + len(fmt['arrow']) + score_width + 1)
    try:
        _, terminal_width = os.popen('stty size', 'r').read().split()
        terminal_width = int(terminal_width)
    except:
        terminal_width = 80
    wrapper = TextWrapper(subsequent_indent=indent, width=terminal_width)

    for i, link in enumerate(links):
        fmt['count'] = color.OKGREEN + str(i + 1).rjust(count_width)
        fmt['score'] = color.WARNING + str(link.score).rjust(score_width)
        fmt['title'] = color.OKBLUE + link.title
        fmt['tags'] = get_link_types(link)

        if len(subreddits) > 1:
            fmt['title'] += color.SUBTEXT + u' ({0})'.format(link.subreddit)

        wrap = wrapper.wrap(
            u'{count}{arrow}{score} {title} {tags}'.format(**fmt))

        for line in wrap:
            print line

    return memo

def print_colorized(text):
    print color.HEADER, text, color.ENDC
    
def print_warning(text, exc=None, exc_details=None):    
    if exc and exc_details:
        print color.FAIL, exc, exc_details
    print color.WARNING, text , color.ENDC

def main():
    parser = _parser(description='''AlienFeed, by Jared Wright, is a
                     commandline application made for displaying and
                     interacting with recent Reddit links. I DO NOT HAVE
                     ANY AFILIATION WITH REDDIT, I AM JUST A HACKER''')
    
    parser.add_argument("-l", "--limit", type=int, default=10,
                        help='Limits output (default output is 10 links)')
    parser.add_argument("subreddit", default='front',
                        help="Returns top links from subreddit 'front' "
                             "returns the front page")
    parser.add_argument("-o", "--open", type=int,
                        help='Opens one link that matches the number '
                             'inputted. Chosen by number')
    parser.add_argument("-r", "--random", action='store_true',
                        help='Opens a random link (must be the only '
                             'optional argument)')
    parser.add_argument("-U", "--update", action='store_true',
                        help='Automatically updates AlienFeed via pip')


    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args=parser.parse_args()    

    subm_gen = None

    if args.open and args.random:
        print_warning("You cannot use [-o OPEN] with [-r RANDOM]")
        sys.exit(1)  

    if args.random:
        if args.limit == 10:
            if args.subreddit == 'front':
                front = r.get_front_page(limit=200)
                links = submission_getter(front)
            else:
                top = r.get_subreddit(args.subreddit).get_top(limit=200)
                new = r.get_subreddit(args.subreddit).get_new(limit=200)
                hot = r.get_subreddit(args.subreddit).get_hot(limit=200)
                links = submission_getter(top)
                links = submission_getter(new, links)
                links = submission_getter(hot, links)
                
            try:
                webbrowser.open( random.choice(links) )
                print_colorized("\nviewing a random submission\n")
            except IndexError, e:
                print_warning("There was an error with your input. "
                              "Hint: Perhaps the subreddit you chose was "
                              "too small to run through the program",
                              "IndexError:", e)
        else:
            print_warning("You cannot use [-l LIMIT] with [-r RANDOM] "
                          "(unless the limit is 10)")
            sys.exit(1)

    elif args.open:
        try:
            subr = (r.get_subreddit(args.subreddit).get_hot(limit=args.limit)
                    if args.subreddit != 'front' else
                    r.get_front_page(limit=args.limit))
            links = submission_getter(subr)
            webbrowser.open( links[args.open - 1] )
            print '\nviewing submission\n'
        except IndexError, e:
            print_warning("The number you typed in was out of the feed's range"
                          " (try to pick a number between 1-10 or add"
                          " --limit {0}".format(e), "IndexError:", e)
        except praw.errors.InvalidSubreddit, e:
            print_warning("I'm sorry but the subreddit '{0}' does not exist; "
                          "try again.".format(args.subreddit),
                          "InvalidSubreddit:", e)
    
    else:
        if args.subreddit == 'front':
            subm_gen = r.get_front_page(limit=args.limit)
            print_colorized('Top {0} front page links:'.format(args.limit))
        else:
            subm_gen = r.get_subreddit(args.subreddit).get_hot(limit=args.limit)
            print_colorized('Top {0} /r/{1} links:'.format(
                args.limit, args.subreddit))

    try:
        if subm_gen:
            subreddit_viewer(subm_gen)
    except praw.errors.InvalidSubreddit, e:
        print_warning("I'm sorry but the subreddit '{0}' does not exist; "
                      "try again.".format(args.subreddit),
                      "InvalidSubreddit:", e)

    if args.update == True:
        try:
            print "Upgrading AlienFeed..."
            call(['pip', 'install', 'alienfeed', '--upgrade', '--quiet'])
        except OSError, e:
            print_warning("You cannot use -U without having pip installed.")

if __name__ == '__main__':
    main()