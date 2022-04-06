import cmd
import sys
import time
import uuid
import readline
import editor

from data import db_operations as db
from termcolor import colored
from data.structures import NodeType, Stream, Node, Post

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

def parse_args(args: str):
    return [x.strip() for x in args.split(' ')]


def join_string(*args):
    return ' '.join([str(x) for x in args])


class CLIState:
    def __init__(self):
        db.ensure_root()
        self.tree_root = db.get_streams_tree()

    def boot_stream(self, args):
        stream_id = str(uuid.uuid4())
        stream_name = args[0]
        create_date = int(time.time())

        stream = Stream(stream_id=stream_id,
            stream_name=stream_name,
            upstream=[],
            downstream=[],
            posts=[],
            create_date=create_date,
            is_archived=False)

        db.boot_stream(stream=stream, upstream_id=self.tree_root.object.get_id())
        self.tree_root.add_child(Node(NodeType.STREAM, stream, self.tree_root))

    def boot_post(self, args):
        post_id = str(uuid.uuid4())
        post_name = args[0]
        post_text = editor.edit(contents=b'').decode()

        post = Post(post_id=post_id, post_name=post_name, post_text=post_text, create_date=int(time.time()))
        db.boot_post(post, self.tree_root.object.get_id())

        self.tree_root.add_child(Node(NodeType.POST, post, self.tree_root))
    
    def show(self, args):
        """
        Show information about the current location.
        """
        obj = self.tree_root.object

        print (colored(f'Stream: "{obj.stream_name}"', 'magenta'))
        children = self.tree_root.children

        streams = [x for x in children if x.type == NodeType.STREAM]
        posts = [x for x in children if x.type == NodeType.POST]

        i = 0
        for stream in streams:
            i += 1
            stream = stream.object
            msg = join_string('stream', i, f': [{stream.stream_id[:5]}]', stream.stream_name)
            print (colored(msg, 'yellow'))
        
        print ('')
        i = 0
        for post in posts:
            i += 1
            post = post.object
            msg = join_string('post  ', i, f': [{post.post_id[:5]}]', post.post_name)
            print (colored(msg, 'green'))

    def enter_stream(self, args):
        """
        Enter into a stream.
        """
        obj = args[0]
        child_map = { child.object.get_name() : child for child in self.tree_root.children }
        
        if obj not in child_map:
            print (colored('Cannot enter', 'red'))
        else:
            self.tree_root = child_map[obj]
    
    def enter_post(self, args):
        """
        Enter into a post
        """
        obj = args[0]
        child_map = { child.object.get_name() : child for child in self.tree_root.children }

        if obj not in child_map:
            print (colored('Cannot enter', 'red'))
        else:
            post = db.get_post(child_map[obj].object.get_id())
            post_text = editor.edit(contents=post.post_text.encode('utf-8')).decode()
            post.post_text = post_text

            db.put_post(post)


class StreamyCLI(cmd.Cmd):
    intro = colored('\nWelcome to Streamy!!', 'cyan', attrs=['bold'])
    prompt = colored('$ ', 'cyan', attrs=['bold'])
    file = None

    def preloop(self) -> None:
        self.cli_state = CLIState()

    def do_boot(self, args:str):
        args = parse_args(args)

        bootable_object = args[0]
        if bootable_object == 'stream':
            self.cli_state.boot_stream(args[1:])
        if bootable_object == 'post':
            self.cli_state.boot_post(args[1:])

    def do_show(self, args:str):
        args = parse_args(args)
        self.cli_state.show(args)
    
    def do_enter(self, args:str):
        args = parse_args(args)
        if args[0] == 'stream':
            self.cli_state.enter_stream(args[1:])
        if args[0] == 'post':
            self.cli_state.enter_post(args[1:])
    
    def do_exit(self, args:str):
        sys.exit(0)


if __name__ == '__main__':
    StreamyCLI().cmdloop()
