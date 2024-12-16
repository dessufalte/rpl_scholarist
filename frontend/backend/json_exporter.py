import json

def save_configuration(filtered_items, selected_format):
    config = {
        "bibliography": filtered_items,
        "format": selected_format
    }
    with open("bibliography_config.json", "w") as file:
        json.dump(config, file, indent=4)
    print("Konfigurasi berhasil disimpan.")
