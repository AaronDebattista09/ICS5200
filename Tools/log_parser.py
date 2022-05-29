import re


def parse_valid_file(valid_file):
    with open(valid_file, 'r', encoding='utf-8') as f:
        lines = list(map(lambda x: x.replace('\n',''), f.readlines()))

    filtered_lines = list(filter(lambda x: re.search(r'Up\. [0-9]+', x), lines))
    processed_lines = []

    for filtered_line in filtered_lines:
        split_log = filtered_line.split(':')
        split_log = split_log[2:]
        split_log[0] = split_log[0][15:]
        split_log[1] = split_log[1][5:]
        split_log = list(map(lambda x: x.strip(), split_log))
        split_log[0] = int(split_log[0])
        split_log[1] = int(split_log[1])
        split_log[3] = float(split_log[3])
        split_log[4] = 1 if 'new best' in split_log[4] else 0

        if split_log[4] == 0:
            split_log[5] = float(split_log[5][:-1])
        else:
            split_log.append(split_log[3])

        processed_lines.append(split_log)

    return processed_lines
