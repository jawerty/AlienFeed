#!/usr/bin/env python

import sys
import random
import argparse
import praw
import webbrowser

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

r = praw.Reddit(user_agent='AlienFeed v0.1.0 by u/jw989 as seen on Github http://github.com/jawerty/AlienFeed')
parser = _parser(description='''AlienFeed, by Jared Wright, is a commandline application made for displaying and interacting with recent Reddit links. I DO NOT HAVE ANY AFILIATION WITH REDDIT, I AM JUST A HACKER''')
parser.add_argument("-l", "--limit", type=int, help='Limits output (default output is 10 links)')
parser.add_argument("subreddit", help='Returns top links from subreddit \'front\' returns the front page')
parser.add_argument("-o", "--open", type=int, help='Opens one link that matches the number inputted. Chosen by number')
parser.add_argument("-r", "--random", action='store_true', help='Opens a random link (must be the only optional argument)')

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args=parser.parse_args()

def main():
	temp = {}
	x = 1

	if args.subreddit:
		if args.random and not args.limit:
			links = {}
			random_int = random.randint(0,300)
			x = 1
			top = r.get_subreddit(args.subreddit).get_top(limit=200)
			new = r.get_subreddit(args.subreddit).get_new(limit=200)
			hot = r.get_subreddit(args.subreddit).get_hot(limit=200)

			for link in top:
				links[x] = link
				x += 1
			for link in new:
				links[x] = link
				x += 1
			for link in hot:
				links[x] = link
				x += 1
			try:
				webbrowser.open(links[random_int].url)
				print color.HEADER, "\n\nviewing a random submission\n\n", color.ENDC
			except KeyError, e:
				print color.FAIL, '\n\nKeyError: ', e
				print color.WARNING,"There was an error with your input. Hint: Perhaps the subreddit you chose was too small to run through the program", color.ENDC
		elif args.random and args.limit:
			print color.WARNING, "You cannot use [-l LIMIT] with [-r RANDOM]", color.ENDC	
		else:			
			if args.subreddit == 'front':
				if args.limit:
					links = r.get_front_page(limit=args.limit)

					print color.HEADER, '\nTop', args.limit, 'front page links:', color.ENDC
						
					for link in links:
						temp[x] = link.url
						print '\n', color.OKGREEN, x,'->', color.OKBLUE, link, color.ENDC
						x += 1
						
				else:
					links = r.get_front_page()

					print color.HEADER, '\nTop 25 front page links:', color.ENDC

					for link in links:
						temp[x] = link.url
						print '\n', color.OKGREEN, x,'->', color.OKBLUE, link, color.ENDC
						x += 1
			else:	
				if args.limit:
					links = r.get_subreddit(args.subreddit).get_hot(limit=args.limit)

					print color.HEADER, '\nTop', args.limit, 'r/' + args.subreddit + ' links:', color.ENDC
						
					try:
						for link in links:
							temp[x] = link.url
							print '\n', color.OKGREEN, x,'->', color.OKBLUE, link, color.ENDC
							x += 1
					except ValueError:
						print color.FAIL, "I'm sorry but the subreddit '",args.subreddit,"' does not exist; try again.", color.ENDC
				else:
					links = r.get_subreddit(args.subreddit).get_hot(limit=10)

					print color.HEADER, '\nTop 10 r/' + args.subreddit + ' links:', color.ENDC
						
					try:
						for link in links:
							temp[x] = link.url
							print '\n', color.OKGREEN, x,'->', color.OKBLUE, link, color.ENDC
							x += 1
					except ValueError:
						print color.FAIL, "I'm sorry but the subreddit '",args.subreddit,"' does not exist; try again.", color.ENDC
	elif args.open:
		try:
			if args.random:
		   		print color.WARNING, "You cannot use [-o OPEN] with [-r RANDOM]", color.ENDC
			else:
				webbrowser.open(temp[args.open])
				print '\n\nviewing submission\n\n'
		except KeyError, e:
			print color.FAIL, '\n\nKeyError: ', e
			print color.WARNING,"The number you typed in was out of the feed's range (try to pick a number between 1-10 or add '--limit", e, "')\n", color.ENDC
	else:
		print "No arguments made"

if __name__ == '__main__':
	main()