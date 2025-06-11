import json

input_file = 'input/hong_kong_place_ids_and_urls_progress2.jsonl'
output_file = 'input/hong_kong_place_ids_and_urls_progress2_en.jsonl'

def process_urls():
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                if 'Maps_url' in data and data['Maps_url']:
                    # Ensure the URL doesn't already have &hl=en
                    if '&hl=en' not in data['Maps_url']:
                        data['Maps_url'] += '&hl=en'
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                print(f"Skipping malformed JSON line: {line.strip()}")

if __name__ == '__main__':
    process_urls() 