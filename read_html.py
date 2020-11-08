import argparse
import concurrent.futures
import html.parser
import logging
from collections import Counter
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig()
LOG = logging.getLogger(__name__)

DEFAULT_MAX_DEPTH = 4
DEFAULT_NUM_ENTRIES = 10


def is_external_link(link, current_netloc):
    """Check if link belongs to original server"""

    return urlparse(link).netloc != current_netloc


def get_links(anchor_tags, current_netloc):
    """Given list of anchors find all links that belong to original server"""

    links = set()
    for anchor in anchor_tags:
        anchor_link = anchor.attrs.get("href")
        if not is_external_link(anchor_link, current_netloc):
            links.add(anchor_link)
    return links


def generate_ngrams(word_list, n):
    """Given list of word list, find n-grams from the words"""

    ngram_list = []

    for x in range(0, len(word_list) - n + 1):
        ngram = " ".join(word_list[x : x + n])
        ngram_list.append(ngram)

    return ngram_list


def get_unigrams_bigrams(text_sections):
    """Given text sections on a page return list on unigrams and bigrams on that page"""

    uni_grams, bi_grams = Counter(), Counter()
    ignore_tags = ["script", "noscript", "css", "style"]
    for section in text_sections:
        if section.parent.name not in ignore_tags:
            uni_grams.update(generate_ngrams(section.strip().split(), 1))
            bi_grams.update(generate_ngrams(section.strip().split(), 2))
    return uni_grams, bi_grams


def parse_page_data(page_data, current_netloc):
    """Given page data return unigrams, bigrams and valid url links found on that page"""

    soup = BeautifulSoup(page_data, "html.parser")
    anchors = soup.find_all("a")
    text_sections = soup.find_all(text=True)
    links = get_links(anchors, current_netloc)
    uni_grams, bi_grams = get_unigrams_bigrams(text_sections)
    return uni_grams, bi_grams, links


def traverse(url):
    """Given url link, find all the relevent data on that page"""

    LOG.debug(f"Traversing link {url} ...")
    current_netloc = urlparse(url).netloc
    page = requests.get(url)
    return parse_page_data(page.content, current_netloc)


def show_results(unigrams, bigrams, num_entries):
    """Display the top num_entries unigrams, birgams"""

    print("List Unigrams:")
    for unigram, count in unigrams.most_common(num_entries):
        print(unigram, count)

    print()

    print("List Bigrams:")
    for bigram, count in bigrams.most_common(num_entries):
        print(bigram, count)


def depth_traversal_with_concurrency(url, max_depth, num_workers):
    """Traverse the given url upto max_depth using num_workers concurrently"""

    LOG.info(f"Exploring {url} till depth of {max_depth} links with {num_workers} workers...")
    master_uni, master_bi, found_links = traverse(url)
    depth = 1

    traversed_links = set()
    traversed_links.add(url)

    new_links = found_links

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor_pool:

        while depth < max_depth:
            links_to_visit = new_links
            new_links = set()

            future_traverse = {
                executor_pool.submit(traverse, link): link for link in links_to_visit
            }
            for future in concurrent.futures.as_completed(future_traverse):
                link = future_traverse[future]
                try:
                    uni, bi, found_links = future.result()
                except Exception as exc:
                    LOG.error(f"Error while traversing {link}")
                else:
                    master_uni.update(uni)
                    master_bi.update(bi)
                    new_links.update(found_links - (links_to_visit.union(traversed_links)))

                traversed_links.add(link)

            depth += 1
            LOG.info(f"Found {len(new_links)} links at depth {depth}")

    return master_uni, master_bi


def depth_traversal(url, max_depth):
    """Traverse the given url upto max_depth using a single thread"""

    LOG.info(f"Exploring {url} till depth of {max_depth} links ...")
    master_uni, master_bi, found_links = traverse(url)
    depth = 1

    traversed_links = set()
    traversed_links.add(url)

    new_links = found_links
    while depth < max_depth:
        links_to_visit = new_links
        new_links = set()

        for link in links_to_visit:
            uni, bi, found_links = traverse(link)
            master_uni.update(uni)
            master_bi.update(bi)
            new_links.update(found_links - (links_to_visit.union(traversed_links)))
            traversed_links.add(link)

        depth += 1
        LOG.info(f"Found {len(new_links)} links at depth {depth}")

    return master_uni, master_bi


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        required=True,
        help="Base url to start looking for unigrams and bigrams",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=DEFAULT_MAX_DEPTH,
        help="Maximum depth to search for urls",
    )
    parser.add_argument(
        "-n",
        "--num-top-entries",
        type=int,
        default=DEFAULT_NUM_ENTRIES,
        help="Total number of unigrams and bigrams to show",
    )
    parser.add_argument(
        "-w",
        "--num-workers",
        type=int,
        default=0,
        help="Total number of workers to use while using concurrency",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        default=0,
        action="count",
        help="Set logging level, -l for info, -ll for debug",
    )
    args = parser.parse_args()

    LOG.setLevel(logging.INFO)
    if args.log_level > 1:
        LOG.setLevel(logging.DEBUG)

    if args.num_workers:
        unigrams, bigrams = depth_traversal_with_concurrency(args.url, args.depth, args.num_workers)
    else:
        unigrams, bigrams = depth_traversal(args.url, args.depth)

    show_results(unigrams, bigrams, args.num_top_entries)
