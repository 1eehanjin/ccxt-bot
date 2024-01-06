import json
import pprint

def convert_addresses_to_json_array():
    json_array = []
    while True:
        address = input("(type 'q' to quit): ")
        if address.lower() == 'q':
            break
        json_array.append(address)

    #result = json.dumps(json_array, ensure_ascii=False)
    print("Result after converting entered addresses to a JSON array:")
    pprint.pprint(json_array)

if __name__ == "__main__":
    convert_addresses_to_json_array()

