from scripts import MfoParser

parser = MfoParser.MfoParser(
        r'/path/to/source.txt',
        r'/path/to/mirrors.txt',
        r'/path/to/blocklist.txt'
    )
parser.execute()
