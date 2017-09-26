import sys

template = '''<html>
<head>
    <meta charset='UTF-8'>
</head>
<body>
    English: [English]
    <br/>
    Yesean: [Yesean]
    <br/>
    Literal English meaning: [Literal English meaning]
    <br/>
    Author: [Author]
    <br/>
    [content as needed]
    <br/>
    Tags: [tags as needed, including @post]
</body>
</html>
'''

with open(sys.argv[1], 'w') as f:
    f.write(template)