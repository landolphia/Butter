import json
import logging
import os.path

COLOR_FILE = "colors.json"
KEYWORD_FILE = "keywords.json"


class Keywords:
    def __init__(self, mode):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Keywords.")

        self.colors = None

        self.load_colors(mode)
        self.load_keywords(mode)
    def load_colors(self, mode):
        f = "./" + str(mode).lower() + "/" + COLOR_FILE
        self.log.debug("Loading colors configuration file [" + f + "].")
        with open(f) as data_file:
            self.colors = json.load(data_file)
    def load_keywords(self, mode):
        f = "./" + str(mode).lower() + "/" + KEYWORD_FILE 
        self.log.debug("Loading keywords configuration file [" + f + "].")
        with open(f) as data_file:
            self.keywords = json.load(data_file)
    def get_keywords(self): return self.keywords
    def get_colors(self): return self.colors
    def get_color(self, kw):
        found = false
        color = None
        for group in self.keywords:
            if (kw in group["keywords"]):
                found = true
                color = group["color"]
                break

        if not found:
            self.log.error("Keyword [" + str(kw) + "] doesn't exist. Can't apply color to cell.")
            sys.exit()

        default = ["#C0C0C0", "#E0E0E0"]

        for c in self.colors:
            if c == color:
                self.log.warning("Found color for [" + str(kw) + "] = [" + str(c) + "]")
                return c

        return default
