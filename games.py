from bs4 import BeautifulSoup
from requests import get


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
CBS = 'https://www.cbssports.com/nfl/scoreboard/'
NFL = 'http://www.nfl.com/schedules'


def main():
    """
    Fetches CBS sport & NFL schedule page, parses that info
    :return: a tuple of a string formatted for Reddit's sidebar and the teams on bye week
    """
    text = game_scores(fetch_webpage(CBS))
    bye = bye_teams(fetch_webpage(NFL))
    return text, bye


def fetch_webpage(site):
    """
    :param site: website to be parsed
    :return: soup object of site param
    """
    url = get(site)
    soup = BeautifulSoup(url.content, 'html.parser')
    return soup


def game_scores(soup):
    """
    :param soup: A soup object of the CBS sports NFL page
    :return: parsed text formatted for reddit's table markdown.
    """
    t = soup.select('div.live-update')
    text = 'Time | Away | | @ | | Home \n :-: | :-: | :-: | :-: | :-: | :-: \n'
    for i in t:
        status = i.select('div.game-status')[0].get_text().strip()
        a = i.select('a.team')
        score = i.select('td.total-score')
        v = [a[0].get_text(), score[0].get_text()]
        h = [a[1].get_text(), score[1].get_text()]
        text += ' {} | {} | {} | @ | {} | {} \n'.format(status, NICKNAME_DICT[v[0]], v[1], h[1], NICKNAME_DICT[h[0]])
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
