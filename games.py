from bs4 import BeautifulSoup
from requests import get
from datetime import datetime
from pytz import timezone


NICKNAME_DICT = {
        'Cardinals': 'ARI',
        'Falcons': 'ATL',
        'Ravens': 'BAL',
        'Bills': 'BUF',
        'Panthers': 'CAR',
        'Bears': 'CHI',
        'Bengals': 'CIN',
        'Browns': 'CLE',
        'Cowboys': 'DAL',
        'Broncos': 'DEN',
        'Lions': 'DET',
        'Packers': 'GB',
        'Texans': 'HOU',
        'Colts': 'IND',
        'Jaguars': 'JAX',
        'Chiefs': 'KC',
        'Dolphins': 'MIA',
        'Vikings': 'MIN',
        'Patriots': 'NE',
        'Saints': 'NO',
        'Giants': 'NYG',
        'Jets': 'NYJ',
        'Raiders': 'OAK',
        'Eagles': 'PHI',
        'Steelers': 'PIT',
        'Chargers': 'LAC',
        'Seahawks': 'SEA',
        '49ers': 'SF',
        'Rams': 'LAR',
        'Buccaneers': 'TB',
        'Titans': 'TEN',
        'Redskins': 'WAS'}


def main():
    """
    Fetches NFL.com's schedule page, calls various scraping functions based upon whether a game is upcoming or already
    played.
    :return: a tuple of a string formatted for Reddit's sidebar and the teams on bye week
    """
    text = 'Time | Away | | @ | | Home \n'
    text += ':-: | :-: | :-: | :-: | :-: | :-: \n'
    soup = fetch_webpage()
    pre_game = pregame(soup)
    post_game = postgame(soup)
    bye = bye_teams(soup)
    if pre_game is False and post_game is False and bye is False:
        return False
    elif pre_game is not False and post_game is False:
        text += pre_game
        return text, bye
    elif pre_game is False and post_game is not False:
        text += post_game
        return text, bye
    elif pre_game is not False and post_game is not False:
        text += post_game
        text += pre_game
        return text, bye


def fetch_webpage():
    """To minimize contact with NFL.com, this fetches the website once and the other functions use its return"""
    url = get('http://www.nfl.com/schedules')
    soup = BeautifulSoup(url.content, 'html.parser')
    return soup


def pregame(soup):
    """Scrapes upcoming games.  The first result in the list is removed because the NFL schedule webpage shows it twice,
    both as the next upcoming game and in a list of the upcoming games."""
    s = soup.select('li.schedules-list-matchup.pre.expandable.type-reg.pro-legacy.no-weather')
    if len(s) == 0:
        return False
    else:
        text = ''
        del s[0]
        for i in s:
            t = i.select('span.time')
            suff = i.select('span.suff')
            clock = ''
            am_or_pm = ''
            for j in t:
                clock += j.get_text()
            hour = int(clock[:clock.index(':')])
            minute = int(clock[clock.index(':') + 1:])
            for j in suff:
                am_or_pm += j.get_text()
            if (am_or_pm[1:3]) == 'PM':
                hour += 12
            if hour == 24:
                hour = 0
            d = i.select('div.schedules-list-content.pre.expandable.type-reg')
            d = str(d[0])
            point = d.index('data-gameid=')
            s = d[point + 13:point + 21]
            date = datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]), hour=hour, minute=minute, second=00)
            tz = timezone('US/Eastern')
            utc = timezone('UTC')
            d_tz = tz.normalize(tz.localize(date))
            d_utc = d_tz.astimezone(utc)
            kuwait = d_utc.astimezone(timezone('Asia/Kuwait'))
            f = kuwait.strftime("%m/%d %H:%M AST")
            a = NICKNAME_DICT[i.select('span.team-name.away')[0].get_text()]
            h = NICKNAME_DICT[i.select('span.team-name.home')[0].get_text()]
            text += (f + '  | ' + a + ' | 0 | @ | 0 | ' + h + '\n')
        return text


def postgame(soup):
    """
    :param soup: a soup object of the NFL's schedule page.
    :return: string formatted for Reddit's sidebar
    """
    s = soup.select('div.schedules-list-hd.post')
    if len(s) == 0:
        return False
    else:
        text = ''
        for i in s:
            away = i.select('span.team-name.away')[0].get_text()
            if away in NICKNAME_DICT:
                away = NICKNAME_DICT[away]
            away_score = i.select('span.team-score.away')[0].get_text()
            home = i.select('span.team-name.home')[0].get_text()
            if home in NICKNAME_DICT:
                home = NICKNAME_DICT[home]
            home_score = i.select('span.team-score.home')[0].get_text()
            text += ' Final | ' + away + ' | ' + away_score + ' | @ | ' + home_score + ' | ' + home + '\n'
        return text


def bye_teams(soup):
    """
    :param soup: a soup object of the NFL's schedule page.
    :return: string of the bye-week teams
    """
    s = soup.select('span.bye-team')
    if len(s) == 0:
        return 'None'
    for i in s:
        text = (i.get_text(strip=True))
        return text
