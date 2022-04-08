import cmd
import sys

from state.cli_state import CLIState
from util.term_util import color
from util.term_util import TermPrinter as prn

def parse_args(args: str):
    return [x.strip() for x in args.split(' ')]


def autocomplete_list(raw_list, phrase):
    if phrase == '':
        return raw_list

    return [item for item in raw_list if item.startswith(phrase)]


def extract_phrase(cmd_line):
    line = cmd_line.split(' ')
    loc = len(line) - 1

    return line[loc]


class StreamyCLI(cmd.Cmd):
    intro = color('\nWelcome to Streamy!!', 'cyan', attrs=['bold'])
    prompt = color('$ ', 'cyan', attrs=['bold'])
    file = None

    def preloop(self) -> None:
        self.cli_state = CLIState()
    
    def do_ls(self, args:str):
        args = parse_args(args)
        self.cli_state.show(args)
    
    def do_stream(self, args:str):
        args = parse_args(args)
        stream_name = args[0]

        if self.cli_state.stream_exists(stream_name):
            self.cli_state.enter_stream(args[1:])
        else:
            self.cli_state.boot_stream(args[1:])

    def complete_stream(self, text, line, beg_idx, end_idx):
        child_streams = self.cli_state.child_streams()
        phrase = extract_phrase(line)

        return autocomplete_list([x.object.get_name() for x in child_streams], phrase)

    def do_post(self, args:str):
        args = parse_args(args)
        post_name = args[0]

        print(post_name, self.cli_state.post_exists(post_name))
        if self.cli_state.post_exists(post_name):
            self.cli_state.enter_post(args)
        else:
            self.cli_state.boot_post(args)

    def complete_post(self, text, line, beg_idx, end_idx):
        child_posts = self.cli_state.child_posts()
        phrase = extract_phrase(line)

        return autocomplete_list([x.object.get_name() for x in child_posts], phrase)
    
    def do_cd(self, args:str):
        args = parse_args(args)
        enterable_name = args[0]

        if enterable_name == '..':
            self.cli_state.enter_back()
        elif self.cli_state.stream_exists(enterable_name):
            self.cli_state.enter_stream(args)
        else:
            prn.red('Cannot enter !!')
    
    def complete_cd(self, text, line, beg_idx, end_idx):
        child_posts = [x.object.get_name() for x in self.cli_state.child_posts()]
        child_streams = [x.object.get_name() for x in self.cli_state.child_streams()]

        phrase = extract_phrase(line)
        return autocomplete_list(child_streams + child_posts, phrase)

    def do_mk(self, args:str):
        args = parse_args(args)
        bootable_object = args[0]

        if bootable_object == 'stream':
            self.cli_state.boot_stream(args[1:])
        if bootable_object == 'post':
            self.cli_state.boot_post(args[1:])

    def complete_mk(self, text, line, beg_idx, end_idx):
        line = line.split(' ')
        loc = len(line) - 1

        current_phrase = line[loc]
        if loc == 1:
            return autocomplete_list(['post', 'stream'], current_phrase)

        return []

    def do_exit(self, args:str):
        sys.exit(0)


if __name__ == '__main__':
    StreamyCLI().cmdloop()
