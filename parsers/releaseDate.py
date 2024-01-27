from bs4 import BeautifulSoup
import requests

class ReleaseDate:
    champions = []

    def __init__(self, champions):
        self.champions = champions

    def parse(self):
        data = requests.get("https://leagueoflegends.fandom.com/wiki/List_of_champions")
        soup = BeautifulSoup(data.content, 'html.parser')
        table = soup.findAll("tbody")[0]
        for row in table.findAll("tr"):
            columns = row.findAll("td")
            if columns:
                champion = columns[0].find("a")["title"].replace("/LoL", "")
                year = columns[2].text.strip()[0:4]
                self.setReleaseDate(champion, year)
        return self.champions
    
    def setReleaseDate(self, championName, year):
        for champion in self.champions:
            if championName == champion.get("name"):
                champion["releaseDate"] = int(year)
