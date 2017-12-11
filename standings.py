from requests import get
from bs4 import BeautifulSoup
from games import DICT as D


def main():
    """
    :return: Sidebar-formatted text
    """
    divisions = fetch()
    init = '{} | {} | {} | {} \n :-: | :-: | :-: | :-:\n'
    sidebar = ''
    for item in divisions:
        conf1, card1, div1, conf2, card2, div2 = item[0][0], item[0][1], item[0][2], item[1][0], item[1][1], item[1][2]
        header = init.format(conf1, card1, conf2, card2)
        for subitem in zip(div1, div2):
            header += '**{}** | {} | **{}** | {} \n'.format(subitem[0][0], subitem[0][1], subitem[1][0], subitem[1][1])
        sidebar += header + '\n'
    return sidebar


def fetch():
    """
    :return: Nested list of team standings, grouped by division
    """
    page = get('https://www.cbssports.com/nfl/standings')
    soup = BeautifulSoup(page.content, 'html.parser')
    section = soup.find_all('table', 'data stacked')
    league = []
    for item in section:
        for subitem in item:
            league.append(subitem)
    teams = team_separator(league)  # I did this to group by NSEW (Website formatting)
    return [[['AFC', 'North', [team for team in teams if D[team[0]] == 'AFC North']],
            ['AFC', 'South', [team for team in teams if D[team[0]] == 'AFC South']]],
            [['AFC', 'East', [team for team in teams if D[team[0]] == 'AFC East']],
            ['AFC', 'West', [team for team in teams if D[team[0]] == 'AFC West']]],
            [['NFC', 'North', [team for team in teams if D[team[0]] == 'NFC North']],
            ['NFC', 'South', [team for team in teams if D[team[0]] == 'NFC South']]],
            [['NFC', 'East', [team for team in teams if D[team[0]] == 'NFC East']],
            ['NFC', 'West', [team for team in teams if D[team[0]] == 'NFC West']]]]


def team_separator(html):
    """
    :param html: html soup object
    :return: nested list of team names & standings
    """
    remove = [35, 30, 25, 20, 15, 10, 5, 0]
    prefixes = ['x-', 'y-', 'z-', '*-']
    teams = []
    for table_row in html:
        stats = []
        for text in table_row:
            text = (text.get_text())
            if text[:2] in prefixes:
                text = text[2:]
            if text in D:  # This changes the city / team name into truncated city name
                text = D[text]
            stats.append(text)
        teams.append(stats)
    for num in remove:
        del teams[num]  # These are rows that are just column headers and aren't needed
    return [[i[0], str(i[1]) + '-' + str(i[2])] for i in teams]  # returns a list of just names & wins/losses
