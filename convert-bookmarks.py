#!/usr/bin/env python
#
# Convert browser bookmark export (NETSCAPE-Bookmark-file-1 format) to BM_TXT
#
from argparse import ArgumentParser
from bs4 import BeautifulSoup

parser = ArgumentParser(description="Convert Netscape bookmarks to JSON")
parser.add_argument(dest="filenames", metavar="filename", nargs="+")
parser.add_argument(
    "-t",
    "--tag",
    metavar="tag",
    dest="tags",
    action="append",
    help="add tag to bookmarks, repeat \
                for multiple tags",
)
args = parser.parse_args()

for filename in args.filenames:
    with open(filename, encoding="utf8") as file:
        soup = BeautifulSoup(file, "html5lib")

        for mydt in soup.find_all("dt"):
            try:
                for link in mydt.dl.find_all("a"):
                    category = list()
                    for header in link.parent.find_parents("dt"):
                        category.append(header.h3.string.strip())
                    bookmark = {}
                    category.reverse()
                    bookmark["dir"] = "/".join(category).replace(" ", "_")
                    # url and title
                    bookmark["url"] = link.get("href")
                    bookmark["title"] = link.string.strip() if link.string else ""
                    # tags
                    tags = list()
                    tags = link.get("tags").split(",") if tags else []
                    if args.tags:
                        tags += args.tags

                    bookmark["tags"] = " ".join(tags)
                    # comment
                    sibling = link.parent.next_sibling
                    bookmark["comment"] = (
                        sibling.string.strip()
                        if sibling and sibling.name == "dd"
                        else ""
                    )
                    print(
                        "{} {} {} {}".format(
                            bookmark["url"],
                            bookmark["title"],
                            bookmark["tags"],
                            bookmark["dir"],
                        )
                    )
            except AttributeError:
                pass
