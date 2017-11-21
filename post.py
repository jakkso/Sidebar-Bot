from os import path
from argparse import ArgumentParser
import praw
import standings
import games
import twitter


afnTV = 31264880
nfl = 'nflkuwait'
test = 'robottestingzone'
dir_path = path.dirname(path.abspath('post.py'))


def main():
    """
    Connects to reddit, creates and then posts the sidebar message.
    """
    parser = ArgumentParser()
    parser.add_argument('-r', '--robotesting', help='Runs the bot on /r/robottestingzone', action='store_true')
    args = parser.parse_args()
    skld = schedule_url()

    if args.robotesting:
        poster(skld, test)

    else:
        poster(skld, nfl)


def poster(schedule, subreddit):
    """
    :param schedule: Link to AFN's twitter feed for that week's NFL air schedule
    :param subreddit:  either a testing subreddit or the nflkuwait subreddit
    """
    r = connect('reddit')
    results = games.main()
    stand = standings.main()
    upcoming = results[0]
    bye = results[1]
    if upcoming is not False:
        new_sidebar = 'Welcome to NFL KUWAIT! We are your source for NFL news, events and competitions \
                in the Middle East.\n\n'
        new_sidebar += '[Twitter](http://twitter.com/NFLKuwait) [Instagram](https://www.instagram.com/nflkuwait/?hl=en\
                ) [Facebook](https://www.facebook.com/NFLKuwait/) [Snapchat](https://www.snapchat.com/add/nflkuwait/)\n\n'
        new_sidebar += '*****\n\n'
        new_sidebar += 'Here\'s the week\'s [AFN game air schedule](' + schedule + ')\n\n'
        new_sidebar += '*****\n\n'
        new_sidebar += '## This week\'s games\n\n'
        new_sidebar += upcoming
        new_sidebar += '\n\nBye teams: ' + bye + '\n\n'
        new_sidebar += '\n\n*****\n\n'
        new_sidebar += '## Current standings\n\n'
        new_sidebar += '\n\n'
        new_sidebar += stand
        r.subreddit(subreddit).mod.update(description=new_sidebar)


def connect(site):
    """
    Depending on site param, it opens and reads from a text file and uses the credentials to establish
    a connection to the site via Oauth.
    :param site: website to establish connection to, can be either 'reddit' or 'twitter'
    :return: Connection to specified site
    """
    if site == 'reddit':
        try:
            credentials = []
            file_name = path.join(dir_path, 'reddit_credentials')
            file = open(file_name)
            for line in file:
                credentials.append(line[:-1])
            file.close()
            c_id = credentials[0]
            c_secret = credentials[1]
            r_id = credentials[2]
            r_pw = credentials[3]
            reddit = praw.Reddit(user_agent='NFL standings Bot (by /u/standingsBot)',
                                 client_id=c_id,
                                 client_secret=c_secret,
                                 username=r_id,
                                 password=r_pw)
            return reddit
        except FileNotFoundError:
            return 'Reddit credentials file not found!'

    elif site == 'twitter':
        try:
            credentials = []
            filename = path.join(dir_path, 'twitter_credentials')
            with open(filename) as file:
                for line in file:
                    credentials.append(line[:-1])
            con_key = credentials[0]
            con_sec = credentials[1]
            access_key = credentials[2]
            access_sec = credentials[3]
            auth = twitter.Api(consumer_key=con_key,
                               consumer_secret=con_sec,
                               access_token_key=access_key,
                               access_token_secret=access_sec)
            return auth
        except FileNotFoundError:
            return 'Twitter credentials file not found!'


def schedule_url():
    """
    Scrapes AFNTelevision twitter feed
    :return: A link to the AFN's NFL schedule for the week.  If not found, a link to the AFNtelevision twitter feed.
    """
    try:
        api = connect('twitter')
        stats = api.GetUserTimeline(afnTV)
        urls = []
        for s in stats:
            if 'NFL' and 'Week' in s.text:
                ind = s.text.index('https://')
                urls.append(s.text[ind:])
        if len(urls) == 0:
            return 'https://twitter.com/AFNtelevision'
        else:
            return urls[0]
    except AttributeError:
        return 'https://twitter.com/AFNtelevision'


if __name__ == '__main__':
    main()
