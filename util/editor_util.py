import editor

def editor_open(content):
    return editor.edit(contents=content).decode()
