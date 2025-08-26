import json

def get_interesting():
    with open("newsgroups_interesting.json", "r", encoding="utf-8")as f:
        newsgroups_interesting = json.load(f)
    return newsgroups_interesting

def get_not_interesting():
    with open("newsgroups_not_interesting.json", "r", encoding="utf-8")as f:
        newsgroups_not_interesting = json.load(f)
    return newsgroups_not_interesting

print(get_interesting()[0])