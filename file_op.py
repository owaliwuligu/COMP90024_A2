import json


def get_children(s, v):
    children1 = []
    for key1, value1 in v.items():
        if value1 == 0:
            temp1 = {'name': key1, 'value': s[key1]['total']}
        else:
            temp1 = {'name': key1, 'value': get_value(s, value1), 'children': get_children(s, value1)}
        children1.append(temp1)
    return children1


def get_value(s, v):
    score1 = 0
    for key1, value1 in v.items():
        if value1 == 0:
            score1 += s[key1]['total']
        else:
            score1 += get_value(s, value1)
    return score1


category_file = open("food_category.json", mode='r')
category = json.loads(category_file.read())
score_file = open("food_category_score.json", mode='r')
score = json.loads(score_file.read())
res = {'name': 'Food'}
children = []
for key, value in category.items():
    temp = {'name': key, "value": get_value(score, value), 'children': get_children(score, value)}
    children.append(temp)
res['children'] = children
print(res)
