import image_preprocess

pd = '../../../../Downloads/'

f = open(pd + 'sentences.txt','r').read().split('\n')

lines = []
for each_line in f:
    lines.append(each_line.split())

new_lines = []

for each_line in lines:
    if len(each_line) > 3:
        if each_line[2] == 'ok':
            new_lines.append((each_line[0],each_line[-1],len(each_line[-1].split('|'))))

predictions = []
actual = []

for i in range(300):
    s = new_lines[i][0].split('-')
    filename = pd + 'sentences/' + s[0] + '/' + "-".join(s[:2]) + '/' + new_lines[i][0] + '.png'
    x = len(image_preprocess.split_sentence(filename))
    predictions.append(x)
    actual.append(new_lines[i][-1])

error = 0
total = 0

count = 0
for x,y in zip(predictions,actual):
    error1 = x - y
    if error1 < 0 :
        error1 = -1 * error1
    error += error1
    total += y

print(1 - (error)/total)