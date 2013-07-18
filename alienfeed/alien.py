#!/usr/bin/env python

import sys
import random
import argparse
import praw
import webbrowser
 
r = praw.Reddit(user_agent='AlienFeed v0.2.7 by u/jw989 seen on Github http://github.com/jawerty/AlienFeed')
 
class terminal_colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    
color = terminal_colors()
 
class _parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(color.FAIL + '\nAlienFeed error: %s\n\n' % message + color.ENDC)
        self.print_help()
        sys.exit(2)
 
def subreddit_viewer(generator):
    try:
        links = submission_getter(generator, verbose=True)
    except ValueError:
        print color.FAIL, "I'm sorry but the subreddit '",args.subreddit,"' does not exist; try again.", color.ENDC
 
def submission_getter(generator, memo=[], verbose=False):
    for x, link in enumerate(generator):
        memo.append(link.url)
        if verbose:
            print '\n', color.OKGREEN, x+1, '->', color.OKBLUE, link, color.ENDC
    return memo
 
def print_colorized(text):
    print color.HEADER, text, color.ENDC
    
def print_warning(text, exc=None, exc_details=None):    
    if exc and exc_details:
        print color.FAIL, exc, exc_details
    print color.WARNING, text , color.ENDC

def main():
    parser = _parser(description='''AlienFeed, by Jared Wright, is a commandline application made for displaying and interacting with recent Reddit links. I DO NOT HAVE ANY AFILIATION WITH REDDIT, I AM JUST A HACKER''')    
    parser.add_argument("-l", "--limit", type=int, default=10,          help='Limits output (default output is 10 links)')
    parser.add_argument("subreddit",               default='front',     help='Returns top links from subreddit \'front\' returns the front page')
    parser.add_argument("-o", "--open",  type=int,                      help='Opens one link that matches the number inputted. Chosen by number')
    parser.add_argument("-r", "--random",          action='store_true', help='Opens a random link (must be the only optional argument)')
    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args=parser.parse_args()        
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
	            print_colorized("\n\nviewing a random submission\n\n")
	        except KeyError, e:
	            print_warning("There was an error with your input. Hint: Perhaps the subreddit you chose was too small to run through the program", '\n\nKeyError: ',e)    
	    
	    else:
	        print_warning("You cannot use [-l LIMIT] with [-r RANDOM] (unless the limit is 10)")
        	sys.exit(1)

    elif args.open:
        try:
           subr = r.get_subreddit(args.subreddit).get_hot(limit=args.limit)
           links = submission_getter(subr)
           webbrowser.open( links[args.open - 1] )
           print '\n\nviewing submission\n\n'
        except KeyError, e:
           print_warning("The number you typed in was out of the feed's range (try to pick a number between 1-10 or add '--limit {0}".format(e)  ,'\n\nKeyError: ',e)
    
    else:
        if args.subreddit == 'front':
            subm_gen = r.get_front_page(limit=args.limit)
            print_colorized('\nTop {0} front page links:'.format(args.limit))
        else:
            subm_gen = r.get_subreddit(args.subreddit).get_hot(limit=args.limit)
            print_colorized('\nTop {0} r/{1} links:'.format(args.limit, args.subreddit) )
            
        subreddit_viewer(subm_gen)    

if __name__ == '__main__':
	main()
