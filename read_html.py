import html.parser
from urllib.parse import urlparse
from collections import Counter

import requests
from bs4 import BeautifulSoup

def is_external_link(link, current_netloc):
    return urlparse(link).netloc != current_netloc

def get_links(anchor_tags, current_netloc):
    links = set()
    for anchor in anchor_tags:
        anchor_link = anchor.attrs.get("href")
        if not is_external_link(anchor_link, current_netloc):
            links.add(anchor_link)
    return links

def generate_ngrams(word_list, n):
    ngram_list = []

    for x in range(0, len(word_list)-n+1):
        ngram = " ".join(word_list[x:x+n])
        ngram_list.append(ngram)

    return ngram_list

def get_unigrams_bigrams(text_sections):
    uni_grams, bi_grams = Counter(), Counter()
    ignore_tags = ['script', 'noscript', 'css', 'style']
    for section in text_sections:
        if section.parent.name not in ignore_tags:
            uni_grams.update(generate_ngrams(section.strip().split(), 1))
            bi_grams.update(generate_ngrams(section.strip().split(), 2))
    return uni_grams, bi_grams

def parse_page_data(page_data, current_netloc):
    soup = BeautifulSoup(page_data, 'html.parser')
    anchors = soup.find_all("a")
    text_sections = soup.find_all(text=True)
    links = get_links(anchors, current_netloc)
    uni_grams, bi_grams = get_unigrams_bigrams(text_sections)
    return uni_grams, bi_grams, links

def traverse(url):
    current_netloc = urlparse(url).netloc
    page=requests.get(url)
    return parse_page_data(page.content, current_netloc)


MAX_DEPTH = 4


def depth_traversal(url):
    u, b, found_links = traverse(url)

    traversed_links = set()
    traversed_links.add(url)

    new_links = found_links
    depth = 1
    print(depth, len(new_links))
    while depth <= MAX_DEPTH:
        links_to_visit = new_links
        new_links = set()
        for link in links_to_visit:
            u, b, found_links = traverse(link)
            new_links.update(found_links - (links_to_visit.union(traversed_links)))
            traversed_links.add(link)
        depth += 1
        print(depth, len(new_links))


if __name__ == "__main__":
    url = "http://www.314e.com/"
    # print(traverse(url))
    print(depth_traversal(url))
