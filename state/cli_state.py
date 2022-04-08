import time
import uuid

from util.editor_util import editor_open

from data.structures import NodeType, Stream, Node, Post
from data import db_operations as db
from util.term_util import TermPrinter as prn

def new_stream(stream_id, stream_name):
    return Stream(stream_id=stream_id,
        stream_name=stream_name,
        upstream=[],
        downstream=[],
        posts=[],
        create_date=int(time.time()),
        is_archived=False)


def uniq():
    return str(uuid.uuid4())


class CLIState:
    def __init__(self):
        db.ensure_root()
        self.tree_root = db.get_streams_tree()
    
    def __current_node(self):
        return self.tree_root
    
    def child_streams(self):
        children = self.__current_node().children
        return [x for x in children if x.type == NodeType.STREAM]
    
    def child_posts(self):
        children = self.__current_node().children
        return [x for x in children if x.type == NodeType.POST]
    
    def __show_list(self, node_list, print_fn):
        i = 0
        for node in node_list:
            i += 1
            node = node.object
            print_fn(f'{i}: [{node.get_id()[:5]}] {node.get_name()}')
    
    def stream_exists(self, stream_name):
        return stream_name in set([s.object.get_name() for s in self.child_streams()])

    def post_exists(self, post_name):
        return post_name in set([s.object.get_name() for s in self.child_posts()])

    def current_object(self):
        return self.__current_node().object

    def boot_stream(self, args):
        stream = new_stream(uniq(), args[0])

        db.boot_stream(stream=stream, upstream_id=self.current_object().get_id())
        self.tree_root.add_child(Node(NodeType.STREAM, stream, self.__current_node()))

    def boot_post(self, args):
        post_text = editor_open(content=b'')

        post = Post(post_id=uniq(), post_name=args[0], post_text=post_text, create_date=int(time.time()))
        db.boot_post(post, self.current_object().get_id())

        self.tree_root.add_child(Node(NodeType.POST, post, self.__current_node()))
    
    def show(self, args):
        obj = self.current_object()

        prn.magenta(f'Stream: "{obj.stream_name}"\n')
        streams = self.child_streams()
        posts = self.child_posts()

        self.__show_list(streams, prn.yellow)

        print('')

        self.__show_list(posts, prn.green)

    def enter_stream(self, args):
        obj = args[0]
        child_map = { child.object.get_name() : child for child in self.child_streams() }
        
        if obj not in child_map:
            prn.red('Cannot ennter !!')
        else:
            self.tree_root = child_map[obj]
    
    def enter_post(self, args):
        obj = args[0]
        child_map = { child.object.get_name() : child for child in self.child_posts() }

        if obj not in child_map:
            prn.red('Cannot enter !!')
        else:
            post = db.get_post(child_map[obj].object.get_id())
            post_text = editor_open(content=post.post_text.encode('utf-8'))
            post.post_text = post_text

            db.put_post(post)
    
    def enter_back(self):
        if self.tree_root.parent is not None:
            self.tree_root = self.tree_root.parent
