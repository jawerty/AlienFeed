# AlienFeed
AlienFeed is a command line application made for displaying and interacting with Reddit submissions. The client can return a list containing the top submissions in a subreddit, and even open the links up if you'd like. I do not have any affiliation with Reddit; I made this to be a fun utilization of the Reddit API.

Current version: 0.3.2

### Contributors
* [jawerty](http://github.com/jawerty)
* [mreinhardt](http://github.com/mreinhardt)
* [thekarangoel](http://github.com/thekarangoel)

## Install Instructions
To download and install AlienFeed, all you need to do is get a copy of this distribution with setup.py or install via pypi

### Install via PIP

```
$ pip install alienfeed
```

###Install via setup.py 
Download this zip or clone it to your local machine. Then run the following commands to install AlienFeed.

```
$ cd /path/to/alienfeed
$ python setup.py install
```

## Usage

There are several different functions that are built into AlienFeed.
See `$ alienfeed -h` for help.

Here you can return a default list of the 10 top r/pics submissions.

```
$ alienfeed pics
```

The output should look similar to the picture below.

![Alt text](/public/pic1.png)

You can also limit the amount of submissions returned by using the '-l or --limit' arguments. If you want a feed that returns a longer list than 10, then you would use this argument. 

```
$ alienfeed pics -l 2
```

The output is below


![Alt text](/public/pic3.png)


If you want to return a list of submissons longer than 10, then you would run the command below.

```
$ alienfeed pics -l 20
```

![Alt text](/public/pic4.png)

If you want to open up a link, use the '-o or --open' arguments. An example is below.

```
$ alienfeed pics -o 3
```

***hint: If you want to open a link larger than ten, you must use the limit argument, which is -l and --limit***

Below is the link that popped up when I ran the previous command. (enjoy the cute dog)

![Alt text](/public/pic2.png)

If you want to open a link that is the 11th most popular. You would have to run the command below. Note that the command is comprised of two different optional arguments, one -o and one -l.

```
$ alienfeed funny -o 11 -l 11
```

The random function opens up a random link from the requested subreddit in a new browser tab (similar to the --open argument). Use the optional argument '-r or --random'. Example using the r/wtf subreddit.

```
$ alienfeed wtf -r
```

This command would of course open up the link in a new browser tab.

To upgrade alienfeed via pip, you would need to call this argument, '-U'
```
$alienfeed funny -U
```

## Contact
If you would like to contact me for further information on the project, see the info below.

Email: jawerty210@gmail.com

Github: jawerty

Twitter: @jawerty

Blog: <http://jawerty.github.io>
