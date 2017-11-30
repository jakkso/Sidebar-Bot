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
        'Redskins': 'WAS',
        'Arizona': 'ARI',
        'Atlanta': 'ATL',
        'Baltimore': 'BAL',
        'Buffalo': 'BUF',
        'Carolina': 'CAR',
        'Chicago': 'CHI',
        'Cincinnati': 'CIN',
        'Cleveland': 'CLE',
        'Dallas': 'DAL',
        'Denver': 'DEN',
        'Detroit': 'DET',
        'Green Bay': 'GB',
        'Houston': 'HOU',
        'Indianapolis': 'IND',
        'Jacksonville': 'JAX',
        'Kansas City': 'KC',
        'Miami': 'MIA',
        'Minnesota': 'MIN',
        'New England': 'NE',
        'New Orleans': 'NO',
        'N.Y. Giants': 'NYG',
        'N.Y. Jets': 'NYJ',
        'Oakland': 'OAK',
        'Philadelphia': 'PHI',
        'Pittsburgh': 'PIT',
        'L.A. Chargers': 'LAC',
        'Seattle': 'SEA',
        'San Francisco': 'SF',
        'L.A. Rams': 'LAR',
        'Tampa Bay': 'TB',
        'Tennessee': 'TEN',
        'Washington': 'WAS'}

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
    text = 'Time | Away | | @ | | Home \n :-: | :-: | :-: | :-: | :-: | :-: \n'
    t = soup.select('div.live-update')
    for i in t:
        status = i.select('div.game-status')[0].get_text().strip()
        a = i.select('a.team')
        score = i.select('td.total-score')
        if len(score) == 0:
            score = [0, 0]
            v = [a[0].get_text(), score[0]]
            h = [a[1].get_text(), score[1]]
            text += ' {} | {} | {} | @ | {} | {} \n'.format(status, NICKNAME_DICT[v[0]], v[1], h[1],
                                                            NICKNAME_DICT[h[0]])
        else:
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
