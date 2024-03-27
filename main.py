import json
from parsers.champions import Champions
from parsers.lane import Lane
from parsers.region import Region
from parsers.releaseDate import ReleaseDate

def main():
    champions_version = "14.6.1"
    
    champions_data = Champions(champions_version).parse()
    champions_data = ReleaseDate(champions_data).parse()
    champions_data = Region(champions_data).parse()
    champions_data = Lane(champions_data).parse()

    output_file_path = "champions.json"
    save_data_to_json(output_file_path, champions_data)

    print(f"Champion data has been saved to {output_file_path}", flush=True)

def save_data_to_json(file_path, data):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, sort_keys=False, indent=4)

if __name__ == "__main__":
    main()
