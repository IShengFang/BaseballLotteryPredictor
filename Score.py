import requests
from bs4 import BeautifulSoup
def FindScore(game):
    scores = []
    url = 'http://www.baseball-reference.com/boxes/{}/{}.shtml'.format(game[0:3],game)
    tag = ".score"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "lxml")
    for score in soup.select('{}'.format(tag)):
        scores.append(int(score.get_text()))
    return scores
def WinOrLoss(scores):
    if scores[0] > scores[1]:
        return 0
    else:
        return 1