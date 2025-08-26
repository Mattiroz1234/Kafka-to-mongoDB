import json

def get_interesting():
    with open("../data/interesting_category_dict.json", "r", encoding="utf-8")as f:
        newsgroups_interesting = json.load(f)
    return newsgroups_interesting

def get_not_interesting():
    with open("../data/not_interesting_category_dict.json", "r", encoding="utf-8")as f:
        newsgroups_not_interesting = json.load(f)
    return newsgroups_not_interesting

