# AlienFeed
AlienFeed is a commandline application made for displaying
and interacting with Reddit submissions. You can return a list containing the top submissions in a subreddit, and even open the links up if you'd like. I do not have any affiliation with Reddit; I made this to be a fun utilization of the Reddit API.

## Install Instructions
To download and install AlienFeed all you need to do is get a copy of this distribution

### Install via PIP
`$ pip install alienfeed`

###Install via setup.py 
Download this zip or clone it to your local machine. Then run the following commands to install AlienFeed.
```
$ cd /path/to/alienfeed
$ python setup.py install
```

## Usage

There are several different functions that are built into AlienFeed.
See `$ alienfeed -h` for help


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


If you want to return a list of submissons longer than 10

```
$ alienfeed pics -l 20
```

![Alt text](/public/pic4.png)

If you want to open up a link, use the '-o or --open' arguments. 

```
$ alienfeed pics -o 3
```

***hint: If you want to open a link larger than ten, you must use the limit argument***

Below is the link that popped up when I ran the previous command.

![Alt text](/public/pic2.png)

If you want to open a link that is the 11th most popular.

```
$ alienfeed funny -o 11 -l 11
```

The random function opens up a random link from the requested subreddit. Use the optional argument '-r or --random'.

```
$ alienfeed wtf -r
```

## Contact
If you would like to contact me for further information on the project, see the info below.

Email: jawerty210@gmail.com
Github: jawerty
Twitter: @jawerty
Blog: <http://wrightdev.herokuapp.com>
