from requests import get
from bs4 import BeautifulSoup

afc = 'AFC'
nfc = 'NFC'
e = 'East'
w = 'West'
n = 'North'
s = 'South'


def main():
    """Flattens a nested list of teams into a single string of text ready to be posted on a reddit sidebar.
    Instead of simplifying the function, I left the option open to be able to easily extend the function to compare
    different conferences / divisions, instead of the league as a whole."""
    league = fetch()
    afc_east = chart(afc, division_separator(league[1:5]), e)
    afc_north = chart(afc, division_separator(league[6:10]), n)
    afc_south = chart(afc, division_separator(league[11:15]), s)
    afc_west = chart(afc, division_separator(league[16:20]), w)
    nfc_east = chart(nfc, division_separator(league[21:25]), e)
    nfc_north = chart(nfc, division_separator(league[26:30]), n)
    nfc_south = chart(nfc, division_separator(league[31:35]), s)
    nfc_west = chart(nfc, division_separator(league[36:40]), w)
    afc_n_s = double_chart(afc_north, afc_south)
    afc_e_w = double_chart(afc_east, afc_west)
    nfc_n_s = double_chart(nfc_north, nfc_south)
    nfc_e_w = double_chart(nfc_east, nfc_west)
    american = [afc_n_s, afc_e_w]
    national = [nfc_n_s, nfc_e_w]
    total = [american, national]
    c = ''
    for i in total:
        b = ''
        for j in i:
            a = ''
            for k in j:
                a += k
                a += '\n'
            b += a
            b += '\n'
        c += b
    return c


def fetch():
    """Scrapes a web-page for current NFL standings, returns a parsed list"""
    page = get('https://www.cbssports.com/nfl/standings')
    soup = BeautifulSoup(page.content, 'html.parser')
    section = soup.find_all('table', 'data stacked')
    league = []
    for i in section:
        for j in i:
            league.append(j)
    return league


def division_separator(teams):
    """Processes, organizes the raw HTML text, returns clean, organized text.  Called once for each division"""
    division = []
    d = {
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
    for i in teams:
        t = []
        for j in i:
            j = (j.get_text())
            if j in d:
                j = d[j]
            t.append(j)
        division.append(t)
    return division


def chart(conference, division1, name1):
    """Further organizes the text into columns separated by characters that initialize reddit's table formatting"""
    template = []
    template.append(conference + ' | ' + str(name1))
    template.append(':-: | :-:')
    for i in division1:
        template.append('*' + str(i[0]) + '* | ' + str(i[1]) + '-' + str(i[2]))
    return template


def double_chart(div1, div2):
    """Combines two charts into a single chart, in order to better use the sidebar landscape."""
    conf = zip(div1, div2)
    d = []
    for i in conf:
        a = i[0]
        b = ' | ' + i[1]
        c = a + b
        d.append(c)
    return d





