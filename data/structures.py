from enum import Enum


class Object:
    """
    The general object representing an object in the system such as a stream or a post
    """

    def get_id():
        """
        Get a globally unique ID for this object.
        """
        pass

    def get_name():
        pass


class Stream(Object):
    """
    Represents a DB representation of a single stream.
    """

    def __init__(self, stream_id, stream_name, upstream, downstream, posts, create_date, is_archived):
        super().__init__()
        self.stream_id = stream_id
        self.stream_name = stream_name
        self.upstream = upstream
        self.downstream = downstream
        self.posts = posts
        self.create_date = create_date
        self.is_archived = is_archived
    
    def get_id(self):
        return self.stream_id
    
    def get_name(self):
        return self.stream_name


class Posts(Object):
    """
    Represents a DB representation of a single post.
    """

    def __init__(self, post_id, post_title, post_text):
        super().__init__()
        self.post_id = post_id
        self.post_name = post_title
        self.post_text = post_text
    
    def get_id(self):
        return self.post_id
    
    def get_name(self):
        return self.post_name


class NodeType(Enum):
    """
    Represents the Object type of a stream node.
    """
    STREAM = 1,
    POST = 2


class Node:
    def __init__(self, type: NodeType, object: Object, parent):
        self.type = type
        self.object = object
        self.parent = parent
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
