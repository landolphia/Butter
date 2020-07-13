import json
import logging
import os.path

COLOR_FILE = "./scrape/colors.json"
KEYWORD_FILE = "./scrape/keywords.json"


class Keywords:
    def __init__(self):
        self.log = logging.getLogger("bLog")
        self.log.debug("Initializing Keywords.")


        self.colors = None

        self.load_colors()
        self.load_keywords()
    def load_colors(self):
        self.log.debug("Loading colors configuration file [" + COLOR_FILE + "].")
        with open(COLOR_FILE) as data_file:
            self.colors = json.load(data_file)
    def load_keywords(self):
        self.log.debug("Loading keywords configuration file [" + KEYWORD_FILE + "].")
        with open(KEYWORD_FILE) as data_file:
            self.keywords = json.load(data_file)
    def get_keywords(self): return self.keywords
    def get_colors(self): return self.colors
    def get_color(self, kw):
        if not (self.keywords[kw]):
            self.log.error("Keyword [" + str(kw) + "] doesn't exist. Can't apply color to cell.")
            sys.exit()

        default = ["#C0C0C0", "#E0E0E0"]

        for c in self.colors:
            if c == self.keywords[kw]:
                self.log.warning("Found color for [" + str(kw) + "] = [" + str(c) + "]")
                return c

        return default
