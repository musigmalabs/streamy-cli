import cmd
import time
import uuid

from data import db_operations as db
from data.structures import NodeType, Stream, Node

def parse_args(args: str):
    return [x.strip() for x in args.split(' ')]


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

    
    def show(self, args):
        """
        Show information about the current location.
        """
        obj = self.tree_root.object

        print ('Stream', obj.stream_name)
        children = self.tree_root.children

        streams = [x for x in children if x.type == NodeType.STREAM]
        posts = [x for x in children if x.type == NodeType.POST]

        i = 0
        for stream in streams:
            stream = stream.object
            print ('stream', i, ':\t', stream.stream_id[:5], ':\t', stream.stream_name)

    def enter(self, args):
        """
        Enter into a stream or post.
        """
        obj = args[0]
        child_map = { child.object.get_name() : child for child in self.tree_root.children }
        
        if obj not in child_map:
            print ('Cannot enter')
        else:
            self.tree_root = child_map[obj]


cli_state = CLIState()


class StreamyCLI(cmd.Cmd):
    intro = 'Welcome to Streamy!!'
    prompt = '$ '
    file = None

    def do_boot(self, args:str):
        args = parse_args(args)

        bootable_object = args[0]
        if bootable_object == 'stream':
            cli_state.boot_stream(args[1:])

    def do_show(self, args:str):
        args = parse_args(args)
        cli_state.show(args)
    
    def do_enter(self, args:str):
        args = parse_args(args)
        cli_state.enter(args)


if __name__ == '__main__':
    StreamyCLI().cmdloop()
