import csv


def write_to_csv(json_data, output_path):
    keys = json_data[0].keys()
    with open(output_path, 'w', newline='', encoding='utf-8-sig') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(json_data)
