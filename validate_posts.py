from post_utils import get_posts

usual_start = '''<html>
<head>
    <meta charset='UTF-8'>
</head>
<body>
'''

usual_end = '''
</body>
</html>
'''

allowed_tags = ['<br/>', '<pre>', '</pre>']

escapes = ['&lt;', '&gt;', '&amp;']

def bad_tag(i):
    return i[0] == '<' and i not in allowed_tags

def bad_escapes(i):
    return i[0] != '<' and (i.count('>') or i.count('<') or (
        i.count('&') > sum(i.count(j) for j in escapes)))

def validate_post(filename):
    with open(filename) as f:
        post = f.read()
    if not (post.startswith(usual_start) and post.endswith(usual_end)):
        print('Weird start or end to post ' + filename)
    body = [i.lstrip() for i in post[len(usual_start):-len(usual_end)].split('\n')]
    if any(i.rstrip() != i for i in body):
        print('Trailing whitespace in post ' + filename + ' (' + [i for i in body if i.rstrip() != i][0] + ')')
    if any(not i for i in body):
        print('Empty line in post ' + filename + ', not doing additional checks on this file')
        return
    if any(bad_tag(i) for i in body):
        print('Weird line or tag in post ' + filename + ':')
        for i in body:
            if bad_tag(i):
                print(i)
    if any(bad_escapes(i) for i in body):
        print('Not enough escapes in post ' + filename + ':')
        for i in body:
            if bad_escapes(i):
                print(i)

def main():
    posts = get_posts()
    for i in posts:
        validate_post(i)

if __name__ == '__main__':
    main()
