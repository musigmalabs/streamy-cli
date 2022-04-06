# Streamy CLI

## Logical Strucutre

Hierarchical structure to organize subjects in streams and posts.

<image src="images/hierarchy.png" width="600" />

A stream under another stream is referred to as down-stream. A parent stream is called an up-stream.

## Data Model

Stream

- stream_id
- name
- upstream
- downstream
- posts
- create_date
- is_archived

Post

- post_id
- text

## CLI

The top level command are:

- `boot`: Create new things like streams, posts and widgets.
- `jump`: Jump in and out of the hierarchy.
- `enter`: Specific actions for pages.
