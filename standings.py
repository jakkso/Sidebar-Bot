from requests import get
from bs4 import BeautifulSoup
from games import NICKNAME_DICT as D


def main():
    div = fetch()
    init = '{} | {} | {} | {} \n :-: | :-: | :-: | :-:\n'
    sidebar = ''
    for item in div:
        conf1, card1, div1, conf2, card2, div2 = item[0][0], item[0][1], item[0][2], item[1][0], item[1][1], item[1][2]
        header = init.format(conf1, card1, conf2, card2)
        for subitem in zip(div1, div2):
            header += '{} | {} | {} | {} \n'.format(subitem[0][0], subitem[0][1], subitem[1][0], subitem[1][1])
        sidebar += header + '\n'
    return sidebar


def fetch():
    """Returns nested list of team divisions"""
    page = get('https://www.cbssports.com/nfl/standings')
    soup = BeautifulSoup(page.content, 'html.parser')
    section = soup.find_all('table', 'data stacked')
    league = []
    for i in section:
        for j in i:
            league.append(j)
    teams = team_separator(league)
    return [[['AFC', 'North', teams[4:8]], ['AFC', 'South', teams[8:12]]], [['AFC', 'East', teams[:4]],
            ['AFC', 'West', teams[12:16]]], [['NFC', 'North', teams[20:24]], ['NFC', 'South', teams[24:28]]],
            [['NFC', 'East', teams[16:20]], ['NFC', 'West', teams[28:]]]]


def team_separator(html):
    """Parses HTML into text, returns list of team standings"""
    remove = [35, 30, 25, 20, 15, 10, 5, 0]
    division = []
    for table_row in html:
        stats = []
        for text in table_row:
            text = (text.get_text())
            if text in D:  # This changes the city / team name into truncated city name
                print(text)
                text = D[text]
            stats.append(text)
        division.append(stats)
    for num in remove:
        del division[num]  # These are rows that are just column headers
    return [[i[0], str(i[1]) + '-' + str(i[2])] for i in division]  # returns a list of just wins/losses


if __name__ == '__main__':
    main()