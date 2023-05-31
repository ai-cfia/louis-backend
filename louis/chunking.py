

from bs4 import BeautifulSoup
import re

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

all_tags = []
def compute_tokens(tag):
    text_content = re.sub(r'\s+', ' ', tag.get_text()).strip()
    tokens = enc.encode(text_content)
    if 'tokens' in tag.attrs:
        raise ValueError(f"tag already has tokens: {tag}")
    tag.attrs['tokens'] = f"{tokens}"
    tag.attrs['token_count'] = f"{len(tokens)}"
    all_tags.append((tag, len(tokens)))

def chunk(html_content):
    """Chunk an HTML document into a list of chunks.
    
     chunks are made up of a title, and a body (which is a list of subheadings and paragraphs)
    
    each chunk should have between 256 and 512 tokens (ada tokens) 
    or less if the entire document is less than 256 tokens
    """
    # chunks are organized by headings in a graph
    # we organize leaf nodes contents into chunks 

    soup = BeautifulSoup(html_content, "lxml")

    current_level = 0
    parent_div = None
    for t in soup.find_all():
        # is this an header?
        if re.match('h[0-9]', t.name):
            # level is the heading level
            new_level = int(t.name[1])

            # we started seeing headers so we initialize a top-level h0-block
            if parent_div is None:
                parent_div = t.wrap(soup.new_tag("div", **{"class": f"h0-block"}))
                parent_div.insert(0, "\n")
                parent_div.append("\n")

            # sibling: we close the previous tag and create a new one
            if new_level == current_level:
                # we need to close the previous div
                compute_tokens(parent_div)
                # we fetch the parent div
                parent_div = parent_div.parent
                parent_div.append(t)
            # child: we push the tag to the block
            elif new_level > current_level:
                # inner tag we append to current parent
                parent_div.append(t)
            # higher-level heading: we close the current div and find the higher-level div
            elif new_level < current_level:
                while True:
                    parent_div = parent_div.parent
                    previous_parent_div_level = int(parent_div.attrs['class'][0][1])
                    if previous_parent_div_level >= new_level:
                        compute_tokens(parent_div)
                        # forget about this one and move to the next
                        continue
                    else:
                        break
                assert parent_div is not None, 'this should never happen because of the h0-block'           
                # we found the higher-level parent_div
                parent_div.append(t)


            # we nest the current tag into a div representing the heading
            parent_div = t.wrap(soup.new_tag(
                "div", **{"class": f"{t.name}-block"}))
            parent_div.insert(0, "\n")
            parent_div.append("\n")        
            current_level = new_level

            # compute tokens for the heading
            compute_tokens(t)
        else:
            # this is content so we push it to the current heading div
            if parent_div is not None:
                compute_tokens(t)
                parent_div.append(t)
                parent_div.append("\n")

    # we finished so we compute the last parent_div
    compute_tokens(parent_div)
    while True:
        parent_div = parent_div.parent
        compute_tokens(parent_div)
        if parent_div['class'] == ['h0-block']:
            break

    return soup

def split(soup):
    # depth-first search to collect all the leaf nodes
    level = 0
    for t in soup.find_all():
        if 'class' in t.attrs and t.attrs['class'] == [f"h{level}-block"]:
            tokens = int(t.attrs['token_count'])
            if tokens > 512:
                # we need to split this div into smaller chunks
                # we need to find the first div that has less than 512 tokens
                # and split it there
                # BFS and then DFS
                pass
            else:
                extract = t.extract()
                for t in extract.select('.h0-block'):
                    print(t)
                    t.replaceWithChildren()
                return extract