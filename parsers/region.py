from bs4 import BeautifulSoup
import requests

class Region:
    champions = []
    regions = [
        "bandle-city", "bilgewater", "demacia", "ionia", "ixtal", "noxus",
        "piltover", "shadow-isles", "shurima", "mount-targon", "freljord", "void", "zaun"
    ]

    def __init__(self, champions):
        self.champions = champions

    def parse(self):
        for faction in self.regions:
            try:
                data = requests.get(f"https://universe-meeps.leagueoflegends.com/v1/en_us/factions/{faction}/index.json")
                data = data.json()
            except:
                print(f"Can't load data for faction {faction}")
                continue

            region_champions = []
            for x in data.get("associated-champions"):
                region_champions.append(x.get("name"))

            for champ in region_champions:
                champ = str(champ).replace("’", "'")
                self.setRegion(champ, faction)

        for champion in self.champions:
            if not champion.get("region"):
             champion["region"] = "runeterra"
    
        return self.champions
    
    def setRegion(self, championName, faction):
        for champion in self.champions:
            if championName == champion.get("name"):
                if champion.get("region"):
                    champion["region"] += "," + faction
                else:
                    champion["region"] = faction
