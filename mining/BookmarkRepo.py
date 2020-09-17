import os.path

class BookmarkRepo:
    bookmark_file = ""

    def __init__(self, bookmark_file):
        self.bookmark_file = bookmark_file

    def save_bookmark(self, i):
        with open( self.bookmark_file, "w") as text_file:
            text_file.write("{}".format(i+1))

    def load_bookmark(self):
        if not os.path.isfile(self.bookmark_file):
            self.save_bookmark(0)
        with open( self.bookmark_file, "r") as file:
            return int(file.read())