FILE_PATH = ''


def parse_events():
    xml_text = open(FILE_PATH).read()
    rows = xml_text.split('\n')
    events = []
    for row in rows:
        if row == '':
            continue
        vals = row.split(',')
        corner1 = (int(vals[0]), int(vals[1]))
        corner2 = (int(vals[2]), int(vals[3]))
        boxes.append((corner1, corner2))
    return boxes
