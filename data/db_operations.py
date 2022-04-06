import time
import data.tables as tables

from data.structures import Stream, Node, NodeType

streams_table = tables.get_streams_table()
posts_table = tables.get_posts_table()

# Low level operations

def get_stream(stream_id: str):
    resp = streams_table.get_item(Key={
        'stream_id': stream_id
    })
    
    if 'Item' not in resp:
        return None

    item = resp['Item']
    return Stream(item['stream_id'],
        item['stream_name'],
        item['upstream'],
        item['downstream'],
        item['posts'],
        item['create_date'],
        item['is_archived'])


def put_stream(stream: Stream):
    streams_table.put_item(Item={
        'stream_id': stream.stream_id,
        'stream_name': stream.stream_name,
        'upstream': stream.upstream,
        'downstream': stream.downstream,
        'posts': stream.posts,
        'create_date': stream.create_date,
        'is_archived': stream.is_archived
    })


def get_post(post_id: str):
    pass


# High level operations

def ensure_root():
    """
    Ensures there's a global root object in the table.
    """
    if get_stream('root') is None:
        root_stream = Stream(
            'root',
            'root',
            [],
            [],
            [],
            int(time.time()),
            False)
        put_stream(root_stream)


def boot_stream(stream: Stream, upstream_id: str):
    put_stream(stream)

    upstream = get_stream(upstream_id)
    upstream.downstream.append(stream.get_id())
    put_stream(upstream)


def get_streams_tree(root_stream_id=None):
    """
    Build a tree starting from a given root (optional).
    """
    ensure_root()

    root_stream_id = 'root' if root_stream_id is None else root_stream_id

    stream = get_stream(root_stream_id)
    root_node = Node(NodeType.STREAM, stream, None)

    _build_streams_tree(root_node)

    return root_node


def _build_streams_tree(node: Node):
    if node.type == NodeType.POST:
        # Posts are terminal
        return

    for child_stream in node.object.downstream:
        stream = get_stream(child_stream)
        
        child_node = Node(NodeType.STREAM, stream, node)
        node.add_child(child_node)

        _build_streams_tree(child_node)
