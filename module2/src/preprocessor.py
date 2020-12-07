import re
import os

STOP_WORDS = os.path.join(os.path.abspath('..'), 'files', 'stop_words.in')


def remove_repeated_characters(line):
    msg = re.sub(r'[k]{2,}', '', line)
    msg = re.sub(r'(.)\1{3,}', r"\1", msg)
    return msg


def remove_punctuation(line):
    return re.sub(r'[,.\'\"!?;:*&()=+\\/_-]+', ' ', line)


def remove_spaces(line):
    return re.sub(r'[ \n\t]+', ' ', line)


def map_numbers(line):
    return re.sub(r'[0-9]+', '<number>', line)


def map_links(line):
    return re.sub(
        r'(https?://(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+['
        r'a-zA-Z0-9]\.[^\s]{2,}|https?://(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})',
        '<link>', line)


def clean_message (line):
    tmp = re.sub(r'RT @[a-zA-Z0-9_]*', '', line) # remove retweets
    tmp = re.sub(r'@[a-zA-Z0-9_]*', '', tmp)     # remove users
    tmp = re.sub(r'#[0-9a-zA-Z]+', '', tmp)      # remove hashtags
    tmp = re.sub(r'&#[0-9]*;', '', tmp)          # remove emojis
    tmp = re.sub(r'&[a-zA-Z0-9]*', '', tmp)  # remove emojis
    return tmp


class Preprocessor:

    stop_words = {}

    def __init__(self):
        self.load_stop_words()

    def load_stop_words(self):
        f = open(STOP_WORDS, "r", encoding="utf-8")
        for line in f:
            self.stop_words[line.lower().rstrip("\n\r").strip()] = 1
        f.close()

    def remove_stop_words(self, line):
        self.load_stop_words()
        words = line.split(" ")
        new_phase = []
        for w in words:
            if w not in self.stop_words:
                new_phase.append(w)
        s = " "
        value = s.join(new_phase)
        return value

    def process(self, msg):
        new_msg = clean_message(msg)
        new_msg = new_msg.lower()
        new_msg = remove_spaces(new_msg)
        new_msg = map_links(new_msg)
        new_msg = map_numbers(new_msg)
        new_msg = remove_punctuation(new_msg)
        new_msg = self.remove_stop_words(new_msg)
        new_msg = remove_repeated_characters(new_msg)
        return new_msg


