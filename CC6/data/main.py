import json_factory

if __name__ == "__main__":
    factory = json_factory.JsonFactory("data.json")

    print("--- Weapons ---")
    for weapon in factory.get_all_weapons():
        print(weapon)

    print("\n--- Armors ---")
    for armor in factory.get_all_armors():
        print(armor)
