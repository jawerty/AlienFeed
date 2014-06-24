#!/usr/bin/env python

from argparse import ArgumentParser, ArgumentTypeError
import math
import os
import random
from subprocess import call
import sys
from textwrap import TextWrapper
import webbrowser
import praw

# Praw (Reddit API Wrapper) initialization
USER_AGENT = ('AlienFeed v0.3.1 by u/jw989 seen on '
              'Github http://github.com/jawerty/AlienFeed')

r = praw.Reddit(user_agent=USER_AGENT)


# Terminal color object. Used for colorful output
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
        # it's nsfw
        types.append(color.FAIL + LinkType.NSFW + color.ENDC)

    return ' '.join(types)

class _parser(ArgumentParser):
    def error(self, message):
        sys.stderr.write(color.FAIL +
                        '\nAlienFeed error: %s\n' % (message + color.ENDC))
        self.print_help()
        sys.exit(2)


# Gets a List of submissions in a desired form
# the submission_list parameter is a list of submissions (returned by Praw) to be processed
# verbose indicates whether it will post details about the list of submissions or just return it
def submission_getter(submission_list, verbose = False):
    submissions = []
    scores = []
    subreddits = set()

    for x, submission in enumerate(submission_list):
        submissions.append(submission)
        if verbose:
            scores.append(submission.score)
            subreddits.add(str(submission.subreddit))

    if not verbose:
        return submissions

    count_width = int(math.log(len(submissions), 10)) + 1
    score_width = len(str(max(scores)))

    fmt = {'arrow': ' -> '}
    indent = ' ' * (count_width + len(fmt['arrow']) + score_width + 1)

    try:
        _, terminal_width = os.popen('stty size', 'r').read().split()
        terminal_width = int(terminal_width)
    except:
        terminal_width = 80

    wrapper = TextWrapper(subsequent_indent = indent, width = terminal_width)

    for i, submission in enumerate(submissions):
        fmt['count'] = color.OKGREEN + str(i + 1).rjust(count_width)
        fmt['score'] = color.WARNING + str(submission.score).rjust(score_width)
        fmt['title'] = color.OKBLUE + submission.title
        fmt['tags'] = get_link_types(submission)

        if len(subreddits) > 1:
            fmt['title'] += color.SUBTEXT + u' ({0})'.format(submission.subreddit)

        wrap = wrapper.wrap(
            u'{count}{arrow}{score} {title} {tags}'.format(**fmt))

        for line in wrap:
            print line

    return submissions


# View a subreddit (i.e. display the links from it)
def subreddit_viewer(submission_list):
    links = submission_getter(submission_list, verbose = True)

# Get a list of links for a subreddit
def get_submissions_from_subreddit(subreddit, limit):
    links = []

    try:
        submissions = ( r.get_subreddit(subreddit).get_hot(limit = limit) if subreddit != 'front' else r.get_front_page(limit = limit) )
        links = submission_getter(submissions)

    except praw.errors.InvalidSubreddit, e:
        print_warning("I'm sorry but the subreddit '{0}' does not exist; try again.".format(subreddit), "InvalidSubreddit:", e)

    return links


# Print-related
def print_colorized(text):
    print color.HEADER, text, color.ENDC

def print_warning(text, exc=None, exc_details=None):
    if exc and exc_details:
        print color.FAIL, exc, exc_details
    print color.WARNING, text , color.ENDC

# Parse an argument value in the form of a range, like 1..5
def parse_range(string):
    try:
        splitted = string.split('..');
        if (len(splitted) != 2):
            raise ArgumentTypeError("'" + string + "' is not a valid range. Expected forms like '1..5'")

        start = int(splitted[0])
        end = int(splitted[1])

        return splitted
    except ValueError:
        raise ArgumentTypeError("Range values are not valid integers. Expected forms like '1..5'")

# Main method
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
    parser.add_argument("-or", "--openrange", type=parse_range,
                        help="Opens a range of links of the form 'x..y', "
                             "where 'x' and 'y' are chosen numbers")
    parser.add_argument("-s", "--self", action="store_true",
                        help="Displays the self text of a post")
    parser.add_argument("-r", "--random", action='store_true',
                        help='Opens a random link (must be the only '
                             'optional argument)')
    parser.add_argument("-U", "--update", action='store_true',
                        help='Automatically updates AlienFeed via pip')


    # if only 1 argument, print the help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    # else, get the arguments
    args = parser.parse_args()

    subm_gen = None

    # This holds the opened submissions, to further do operations on them (e.g. --self)
    chosen_submissions = []

    # Do acion depending on the passed arguments
    # Open range of submissions case
    if args.openrange:
        if args.open or args.random:
            print_warning("You cannot use [-or OPENRANGE] with [-o OPEN] or with [-r RANDOM]")
            sys.exit(1)
        else:
            start = int(args.openrange[0])
            end = int(args.openrange[1])

            # ensure end is not above the limit
            if end > args.limit:
                print_warning("The upper range limit you typed was out of the feed's range"
                              " (try to pick a number between 1 and 10 or add --limit {0})")
                sys.exit(1)
            else:
                end += 1        # add 1 to include upper end of range

            # Get the submissions for the subreddit
            submissions = get_submissions_from_subreddit(args.subreddit, args.limit)

            print_colorized("Viewing a range of submissions\n")

            for x in range(start, end):
                # Chosen submission
                chosen = submissions[x - 1]

                # Save the chosen submission
                chosen_submissions.append(chosen)

                # Open the link
                webbrowser.open(chosen.url)

    # Invalid case
    elif args.open and args.random:
        print_warning("You cannot use [-o OPEN] with [-r RANDOM]")
        sys.exit(1)

    # Open a certain submisison case
    elif args.open:
        try:
            # Get the submissions for the subreddit
            submissions = get_submissions_from_subreddit(args.subreddit, args.limit)

            print_colorized("Viewing a submission\n")

            # Save chosen submission
            chosen_submissions.append(submissions[args.open - 1]);

            # Open desired link
            webbrowser.open(submissions[args.open - 1].url)
        except IndexError, e:
            print_warning("The number you typed in was out of the feed's range"
                          " (try to pick a number between 1 and 10 or add"
                          " --limit {0})".format(e), "IndexError:", e)

    # Random submission case
    elif args.random:
        if args.limit == 10:
            if args.subreddit == 'front':
                front = r.get_front_page(limit = 200)
                submissions = submission_getter(front)
            else:
                top = r.get_subreddit(args.subreddit).get_top(limit = 200)
                new = r.get_subreddit(args.subreddit).get_new(limit = 200)
                hot = r.get_subreddit(args.subreddit).get_hot(limit = 200)
                submissions = submission_getter(top)
                submissions.extend(submission_getter(new))
                submissions.extend(submission_getter(hot))

            try:
                # Get a random submission
                chosen = random.choice(submissions)

                # Save the chosen submission
                chosen_submissions.append(chosen)

                # Open the link
                webbrowser.open( chosen.url )
                print_colorized("Viewing a random submission\n")

            except IndexError, e:
                print_warning("There was an error with your input. "
                              "Hint: Perhaps the subreddit you chose was "
                              "too small to run through the program",
                              "IndexError:", e)
        else:
            print_warning("You cannot use [-l LIMIT] with [-r RANDOM] "
                          "(unless the limit is 10)")
            sys.exit(1)

    # Default case is listing Top 'limit' elements
    else:
        if args.subreddit == 'front':
            submission_list = list(r.get_front_page(limit=args.limit))
            print_colorized('Top {0} front page links:'.format(args.limit))
        else:
            submission_list = list(r.get_subreddit(args.subreddit).get_hot(limit=args.limit))
            print_colorized('Top {0} /r/{1} links:'.format(args.limit, args.subreddit))

        try:
            # Save them to the chosen submissions
            chosen_submissions.extend(submission_list)

            # Display the Submissions
            subreddit_viewer(submission_list)
        except praw.errors.InvalidSubreddit, e:
            print_warning("I'm sorry but the subreddit '{0}' does not exist; "
                          "try again.".format(args.subreddit), "InvalidSubreddit:", e)

    # Self post case
    if args.self:
        print_colorized("Selft text of submission(s):")
        for i, submission in enumerate(chosen_submissions):
            print color.OKGREEN, "[" + str(i) + "] -> ", color.OKBLUE, submission.selftext, color.ENDC

    # Update AlienFeed case
    if args.update == True:
        try:
            print "Upgrading AlienFeed..."
            call(['pip', 'install', 'alienfeed', '--upgrade', '--quiet'])
        except OSError, e:
            print_warning("You cannot use -U without having pip installed.")

if __name__ == '__main__':
    main()
