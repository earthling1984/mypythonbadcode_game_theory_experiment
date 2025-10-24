import html
def using_path(path):
    print("path is",path)
    escaped_path = html.escape(path)
    print("Escaped path is",escaped_path)
    return escaped_path