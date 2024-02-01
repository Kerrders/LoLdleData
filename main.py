import json
from parsers.champions import Champions
from parsers.lane import Lane
from parsers.region import Region
from parsers.releaseDate import ReleaseDate

champions = Champions("14.2.1").parse()
champions = ReleaseDate(champions).parse()
champions = Region(champions).parse()
champions = Lane(champions).parse()

output_file_path = "champions.json"
with open(output_file_path, "w") as json_file:
    json.dump(champions, json_file, sort_keys=False, indent=4)

print(f"Champion data has been saved to {output_file_path}")