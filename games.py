from bs4 import BeautifulSoup
from requests import get

DICT = {'Cardinals': 'ARI',
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
        'Washington': 'WAS',
        'NE': 'AFC East',
        'BUF': 'AFC East',
        'NYJ': 'AFC East',
        'MIA': 'AFC East',
        'KC': 'AFC West',
        'LAC': 'AFC West',
        'OAK': 'AFC West',
        'DEN': 'AFC West',
        'PIT': 'AFC North',
        'BAL': 'AFC North',
        'CIN': 'AFC North',
        'CLE': 'AFC North',
        'TEN': 'AFC South',
        'JAX': 'AFC South',
        'HOU': 'AFC South',
        'IND': 'AFC South',
        'MIN': 'NFC North',
        'DET': 'NFC North',
        'GB': 'NFC North',
        'CHI': 'NFC North',
        'NO': 'NFC South',
        'CAR': 'NFC South',
        'ATL': 'NFC South',
        'TB': 'NFC South',
        'PHI': 'NFC East',
        'DAL': 'NFC East',
        'WAS': 'NFC East',
        'NYG': 'NFC East',
        'LAR': 'NFC West',
        'SEA': 'NFC West',
        'ARI': 'NFC West',
        'SF': 'NFC West'}
CBS = 'https://www.cbssports.com/nfl/scoreboard/'
NFL = 'http://www.nfl.com/schedules'


def main():
    """
    Fetches CBS sport & NFL schedule page, parses that info
    :return: a tuple of a string formatted for Reddit's sidebar and the teams on bye
    """
    scores = game_scores(fetch_webpage(CBS))
    bye = bye_teams(fetch_webpage(NFL))
    return scores, bye


def fetch_webpage(site):
    """
    :param site: website to be parsed
    :return: soup object of site
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
    games = soup.select('div.live-update')
    for game in games:
        status = game.select('div.game-status')[0].get_text().strip()
        team = game.select('a.team')
        score = game.select('td.total-score')
        if len(score) == 0:
            score = [0, 0]
            v = [team[0].get_text(), score[0]]
            h = [team[1].get_text(), score[1]]
            text += ' {} | {} | {} | @ | {} | {} \n'.format(status, DICT[v[0]], v[1], h[1],
                                                            DICT[h[0]])
        else:
            v = [team[0].get_text(), score[0].get_text()]
            h = [team[1].get_text(), score[1].get_text()]
            text += ' {} | {} | {} | @ | {} | {} \n'.format(status, DICT[v[0]], v[1], h[1], DICT[h[0]])
    return text


def bye_teams(soup):
    """
    :param soup: a soup object of the NFL's schedule page.
    :return: string of the bye-week teams
    """
    bye = soup.select('span.bye-team')
    if len(bye) == 0:
        return 'None'
    for team in bye:
        text = (team.get_text(strip=True))
        return text
