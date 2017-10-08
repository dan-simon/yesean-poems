from post_utils import get_posts

start = '''<html>
<head>
    <meta charset='UTF-8'>
</head>
<body>
    List of entries, together with their tags:
    <br/>
    '''

middle = '''
    <br/>
    List of tags, together with entries with that tag:
    <br/>
    '''

end = '''
</body>
</html>
'''

def join_br(l):
    return '\n    <br/>\n    '.join(l)

def valid_tag(tag):
    return tag[0] == '@' and tag[1:].isalpha() and tag[1:].islower()

def get_tags(x):
    tag_line_start = 'Tags:'
    with open(x) as f:
        tag_lines = [l for l in f.readlines() if l.strip().startswith(tag_line_start)]
    if len(tag_lines) != 1:
        raise ValueError('Too few or too many tag lines (' + str(len(tag_lines)) + ', not 1) on file ' + x)
    tags = [i.strip() for i in tag_lines[0].strip()[len(tag_line_start):].strip().split(',')]
    if any(not valid_tag(tag) for tag in tags):
        raise ValueError('Bad tags: ' + ', '.join(tag for tag in tags if not valid_tag(tag)))
    return tags

def link_file(f):
    return '<a href="' + f + '">' + f + '</a>'

def get_tag_dict(files, tags):
    d = {}
    for f, t in zip(files, tags):
        for tag in t:
            d.setdefault(tag, [])
            d[tag].append(f)
    return d

def main_and_tags():
    files = get_posts()
    tags = [list(sorted(get_tags(i))) for i in files]
    main_section = [link_file(f) + ', with tags ' + ', '.join(t) for f, t in zip(files, tags)]
    tag_dict = get_tag_dict(files, tags)
    tags_section = ['Tag ' + t + ': ' + ', '.join(link_file(i) for i in tag_dict[t])
    for t in sorted(tag_dict.keys())]
    return join_br(main_section), join_br(tags_section)

def main():
    main_section, tags_section = main_and_tags()
    text = start + main_section + middle + tags_section + end
    with open('contents.html', 'w') as f:
        f.write(text)

if __name__ == '__main__':
    main()
