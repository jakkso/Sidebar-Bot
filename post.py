from os import path
from argparse import ArgumentParser
import praw
from standings import main as standings
from games import main as games
import twitter

nfl = 'nflkuwait'
test = 'robottestingzone'
dir_path = path.dirname(path.abspath('post.py'))


def main():
    """
    Determines where to post sidebar.
    """
    parser = ArgumentParser()
    parser.add_argument('-r', '--robotesting', help='Runs the bot on /r/robottestingzone', action='store_true')
    args = parser.parse_args()

    if args.robotesting:
        poster(test)

    else:
        poster(nfl)


def poster(subreddit):
    """
    Creates sidebar message and posts it to specified subreddit
    :param subreddit:  the subreddit where the sidebar will be updated.
    """
    r = connect('reddit')
    res = games()
    game_list, bye = res[0], res[1]
    standings_chart = standings()
    schedule = schedule_url()
    new_sidebar = 'Welcome to NFL KUWAIT! We are your source for NFL news, events and competitions \
            in the Middle East.\n\n'
    new_sidebar += '[Twitter](http://twitter.com/NFLKuwait) [Instagram](https://www.instagram.com/nflkuwait/?hl=en\
            ) [Facebook](https://www.facebook.com/NFLKuwait/) [Snapchat](https://www.snapchat.com/add/nflkuwait/)\n\n'
    new_sidebar += '*****\n\n'
    new_sidebar += 'Here\'s the week\'s [AFN game air schedule](' + schedule + ')\n\n'
    new_sidebar += '*****\n\n'
    new_sidebar += '## This week\'s games\n\n'
    new_sidebar += game_list
    new_sidebar += '\n\nBye teams: ' + bye + '\n\n'
    new_sidebar += '\n\n*****\n\n'
    new_sidebar += '## Current standings\n\n'
    new_sidebar += '\n\n'
    new_sidebar += standings_chart
    r.subreddit(subreddit).mod.update(description=new_sidebar)


def connect(site):
    """
    :param site: website to establish connection to, can be either reddit or twitter
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
    :return: A link to the AFN's NFL schedule for the week.  If not found, a link to the AFNtelevision twitter feed.
    """
    try:
        api = connect('twitter')
        posts = api.GetUserTimeline(31264880)
        urls = []
        for post in posts:
            if '#NFL' in post.text:
                ind = post.text.index('https://')
                urls.append(post.text[ind:])
        if len(urls) == 0:
            return 'https://twitter.com/AFNtelevision'
        else:
            return urls[0]
    except AttributeError:
        return 'https://twitter.com/AFNtelevision'


if __name__ == '__main__':
    main()
