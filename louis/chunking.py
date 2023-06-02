# in each HTML document, find all the headings and split the document into chunks
# for each heading, wrap the heading and its siblings into a div, including other heading of 
# a higher level
# if 


from bs4 import BeautifulSoup
import re

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

def compute_tokens(tag):
    if 'tokens' in tag.attrs:
        # content is cached in tag
        text_content = tag.attrs['text_content']
        token_count = tag.attrs['token_count']
        tokens = tag.attrs['tokens']
    else:
        # extract and clean up tag text content, storing it in tag
        text_content = re.sub(r'\s+', ' ', tag.get_text(strip=True))
        tokens = enc.encode(text_content)
        token_count = len(tokens)
        tag.attrs['tokens'] = f"{tokens}"
        tag.attrs['token_count'] = f"{token_count}"
        tag.attrs['text_content'] = f"{text_content}"
    return {
        'text_content': text_content, 
        'tokens': tokens, 
        'token_count': token_count
    }

HEADERS_RE = re.compile('^h[1-6]$')

def mark_parent(tag):
    # ok, parent is already identified as parent
    if 'parent' in tag.attrs:
        return
    
    # set parent flag
    tag.attrs['parent'] = True

    # if we're at the body tag, we're done
    if tag.name == 'body':
        return
    
    # otherwise we keep going
    return mark_parent(tag.parent)

find_next_parent_div = lambda t: t.find_parent(class_='blocks')

def collect_chunks(t, total_token_count, chunks):
    chunk = compute_tokens(t)
    prospective_total = total_token_count + chunk['token_count']
    if prospective_total <= 512:
        t.attrs['processed'] = True
        chunks.append(chunk)
    elif prospective_total > 512:
        # forget about this chunk, it's too big
        return
    if t.next_sibling:
        # there's a sibling, let's see how much we can fit in
        return collect_chunks(t.next_sibling, prospective_total, chunks)
    else:
        # no more siblings so we go up the tree to the next block
        # which includes this one and all the siblings
        # so we reset chunks
        chunks.clear()
        return collect_chunks(find_next_parent_div(t), 0, chunks)
    
def chunk(html_content):
    """Chunk an HTML document into a list of chunks.
    
     chunks are made up of a title, and a body (which is a list of subheadings and paragraphs)
    
    each chunk should have between 256 and 512 tokens (ada tokens) 
    or less if the entire document is less than 256 tokens

    returns a list of chunks, each chunk is a tuple (text_content, tokens, token_count)
    """
    # chunks are organized by headings in a graph
    # we organize leaf nodes contents into chunks 

    soup = BeautifulSoup(html_content, "lxml")

    # make sure html fragments are wrapped in html and body tags
    soup.smooth()
    body = soup.select('body')[0]
    body.attrs['class'] = body.attrs.get('class', []) + ["blocks", "h0-block"]

    parent_div = None

    # https://bugs.launchpad.net/beautifulsoup/+bug/1804303
    # make a copy of the list of tags because we will be modifying the tree
    for t in list(soup.find_all(HEADERS_RE)):
        # get siblings before we wrap the current tag
        siblings = list(t.next_siblings)
        # we nest the current tag into a div representing the heading
        parent_div = t.wrap(soup.new_tag(
            "div", **{"class": f"{t.name}-block blocks"}))

        # we append every sibling to the current div up to the next heading
        for s in siblings:
            if s.name and re.match(HEADERS_RE, s.name):
                if s.name[1] <= t.name[1]:
                    # sibling header is of same or lower level
                    break
            parent_div.append(s)
        
        # we recursively mark all the block div above as a parent block
        # any non-parent block left is a leaf
        mark_parent(parent_div.parent)

    # collect chunks from leafs
    all_chunks = []
    for t in soup.select('.blocks'):
        # this chunk is a parent, we start at the leafs
        if 'parent' in t.attrs:
            continue
        # this chunk is already identified
        if 'processed' in t.attrs:
            continue
        chunks = []
        collect_chunks(t, 0, chunks)
        all_chunks.extend(chunks)

    return (soup, all_chunks)

    

if __name__ == '__main__':
    # open file from first parameter
    import sys
    with open(sys.argv[1]) as f:
        html = f.read()

    soup, chunks = chunk(html) 
    print(soup.prettify())
    print(chunks)
