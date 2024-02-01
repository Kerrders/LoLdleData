from bs4 import BeautifulSoup
import requests

class Lane:
    champions = []
    columnLaneMap = {
        1: 'top',
        2: 'jungle',
        3: 'mid',
        4: 'bottom',
        5: 'support'
    }

    def __init__(self, champions):
        self.champions = champions

    def parse(self):
        data = requests.get("https://leagueoflegends.fandom.com/wiki/List_of_champions_by_draft_position")
        soup = BeautifulSoup(data.content, 'html.parser')
        table = soup.findAll("tbody")[1]
        for row in table.findAll("tr"):
            columns = row.findAll("td")
            if not columns:
                continue
            for index, column in enumerate(columns, start=1):
                img_tag = column.find('img', alt='Yes')
                if not img_tag:
                    continue
                lane = self.columnLaneMap.get(index - 1, 'unknown')
                if lane == 'unknown':
                    continue
                champion_name = columns[0].find("a")["title"].replace("/LoL", "")
                self.setLane(champion_name, lane)
        return self.champions
    
    def setLane(self, championName, lane):
        for champion in self.champions:
            if championName == champion.get("name"):
                if champion.get("lane"):
                    champion["lane"] += "," + lane
                else:
                    champion["lane"] = lane
