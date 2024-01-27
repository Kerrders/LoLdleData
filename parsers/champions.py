import requests

class Champions:
    version = ""

    def __init__(self, version):
        self.version = version

    def parse(self):
        data = requests.get(f"https://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/championFull.json")
        return self.mapData(data.json()["data"])
        
    def mapData(self, champions):
        mappedData = []
        for champ in champions:
            mappedData.append({
                "id": champions[champ].get("id"),
                "name": champions[champ].get("name"),
                "title": champions[champ].get("title"),
                "resource": champions[champ].get("partype"),
                "genre": ",".join(champions[champ].get("tags")),
                "skinCount": len(champions[champ].get("skins")),
                "image": champions[champ].get("image"),
                "gender": self.getGender(champions[champ].get("id")),
            })
            print('Data fetched for ' + champ)

        return mappedData

    def getGender(self, championId):
        if championId == "Renata":
            championId = "renataglasc"
        try:
            lore = requests.get(f"https://universe-meeps.leagueoflegends.com/v1/en_us/champions/{championId.lower()}/index.json").json()
            bio = lore.get("champion", {}).get("biography", {}).get("full", "").lower().split(" ")

            male_keywords = {"he", "him", "his"}
            female_keywords = {"she", "her", "hers"}

            male_count = sum(chunk in male_keywords for chunk in bio)
            female_count = sum(chunk in female_keywords for chunk in bio)

            if male_count > female_count:
                return "male"
            elif female_count > male_count:
                return "female"
            else:
                return "divers"
        except:
            return "divers"
    