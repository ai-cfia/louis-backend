import json
from bs4 import BeautifulSoup
import re

import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

HEADERS_RE = re.compile('^h[1-6]$')

def compute_tokens(tag):
    """Compute the tokens and token count of a tag, caching the result in the tag"""
    if 'tokens' in tag.attrs:
        # content is cached in tag
        text_content = tag.attrs['text_content']
        token_count = int(tag.attrs['token_count'])
        tokens = json.loads(tag.attrs['tokens'])
    else:
        # extract and clean up tag text content, storing it in tag
        text_content = re.sub(r'\s+', ' ', tag.get_text()).strip()
        tokens = enc.encode(text_content)
        token_count = len(tokens)
        tag.attrs['tokens'] = str(tokens)
        tag.attrs['token_count'] = str(token_count)
        tag.attrs['text_content'] = text_content
    return {
        'text_content': text_content,
        'tokens': tokens,
        'token_count': token_count
    }

def mark_parent(tag):
    """Mark the parent of a tag as a parent, recursively"""
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

def mark_processed(tag):
    """Mark a tag as processed, recursively"""
    tag.attrs['processed'] = True
    child_blocks = tag.find_all(class_='blocks')
    for c in child_blocks:
        c.attrs['processed'] = True

def split_chunk_into_subchunks(chunk, min_tokens=256, max_tokens=512):
    """some leafs might be bigger than desired. split text into smaller chunks"""
    assert chunk['token_count'] > max_tokens
    text_content = chunk['text_content']
    sentences = text_content.split('.')
    buckets = [[]]
    bucket = buckets[0]
    bucket_size = 0
    for text_content in sentences:
        tokens = enc.encode(text_content)
        token_count = len(tokens)
        if bucket_size + token_count > max_tokens:
            # we're over the limit, we start a new bucket
            bucket = []
            buckets.append(bucket)
            bucket_size = 0

        bucket.append({
            'text_content': text_content,
            'tokens': tokens,
            'token_count': token_count
        })
        bucket_size += token_count
    chunks = []
    for b in buckets:
        chunk = combine_chunks_into_single_chunk(b)
        chunks.append(chunk)
    return chunks

def collect_chunks_from_tag(t, total_token_count, chunks):
    """Collect chunks of text, starting from a tag, until the total token count is at most 512"""
    if 'processed' not in t.attrs:
        chunk = compute_tokens(t)
        prospective_total = total_token_count + int(chunk['token_count'])
        if prospective_total <= 512:
            chunks.append(chunk)
            mark_processed(t)
        elif prospective_total > 512:
            # too big, we skip it and let next iteration handle it
            return
    else:
        # this is already processed, nothing changes and we skip to the next sibling
        # or more likely the next parent
        prospective_total = total_token_count

    if t.next_sibling:
        # there's a sibling, let's see how much we can fit in
        return collect_chunks_from_tag(t.next_sibling, prospective_total, chunks)
    else:
        # no more siblings so we go up the tree to the parent block
        # which includes this one and all the siblings
        # so we reset chunks
        parent_div = find_next_parent_div(t)
        if parent_div:
            parent_chunks = []
            collect_chunks_from_tag(parent_div, 0, parent_chunks)
            if len(parent_chunks) > 0:
                chunks.clear()
                chunks.extend(parent_chunks)
            return
        else:
            # we're at the top of the tree
            return

def block_by_heading(soup):
    """Wrap each heading and its siblings into a div, including other heading of a higher level"""
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
        # any non-parent block left at the end will be a leaf
        mark_parent(parent_div.parent)

def combine_chunks_into_single_chunk(chunks):
    """Combine list of chunks into a single chunk"""
    assert len(chunks) > 0

    # we return when there's only a single chunk left
    if len(chunks) == 1:
        chunk = chunks[0]
        return chunk

    chunk = chunks[0]
    for next_chunk in chunks[1:]:
        chunk['text_content'] += " " + next_chunk['text_content']
        chunk['tokens'] += next_chunk['tokens']
        chunk['token_count'] += next_chunk['token_count']
        assert chunk['token_count'] <= 512
    return chunk

def segment_blocks_into_chunks(blocks):
    """Segment blocks into chunks of 256-512 tokens"""
    # collect chunks from leafs
    all_chunks = []
    for t in blocks:
        # this chunk is a parent, we start at the leafs
        if 'parent' in t.attrs:
            continue
        # this chunk is already taken care of
        if 'processed' in t.attrs:
            continue
        chunk = compute_tokens(t)
        if chunk['token_count'] <= 512:
            if chunk['token_count'] >= 256:
                # perfect sized chunk
                all_chunks.append(chunk)
                mark_processed(t)
            else: # < 256:
                # chunk too small
                chunks = []
                # we collect siblings until we reach 256 tokens
                collect_chunks_from_tag(t, chunk['token_count'], chunks)
                chunk = combine_chunks_into_single_chunk(chunks)
                all_chunks.append(chunk)
        else:
            # chunk too big
            chunks = []
            split_chunk_into_subchunks(chunk, chunks)
            mark_processed(t)
            all_chunks.extend(chunks)

    return all_chunks

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

    block_by_heading(soup)

    chunks = segment_blocks_into_chunks(soup.select('.blocks'))

    return (soup, chunks)



if __name__ == '__main__':
    # open file from first parameter
    import sys
    with open(sys.argv[1]) as f:
        html = f.read()

    soup, chunks = chunk(html)
    print(soup.prettify())
    print(chunks)
