import random
import re
import pickle
import argparse


class Text:
    def __init__(self, filename):
        self.words = {}

        with open(filename, 'r', encoding='UTF-8') as file:
            content = file.read()

        words = self.get_cleaned_words(content)
        for i, word in enumerate(words):
            if i + 1 < len(words):
                self[word] = words[i + 1]

    def save(self, filename):
        with open(filename, 'wb') as output:
            pickle.dump(self, output, pickle.HIGHEST_PROTOCOL)

    def all_words(self):
        return list(self.words.keys())

    def __setitem__(self, key, value):
        if key in self.words:
            self.words[key].append(value)
        else:
            self.words[key] = [value]

    def __getitem__(self, item):
        item_list = self.words.get(item)

        if item_list is not None:
            return random.choice(item_list)

    def merge(self, cls):
        self.words.update(cls.words)

    @staticmethod
    def get_cleaned_words(line):
        all_words = re.findall(r"[\w']+", line)
        final_words = []
        for word in all_words:
            if word.isalpha():
                final_words.append(word.lower())

        return final_words


class Generator:
    def __init__(self, text_filename, another_text_filename):
        with open(text_filename, 'rb') as text_file:
            self.text1 = pickle.load(text_file)

        with open(another_text_filename, 'rb') as another_text_file:
            self.text2 = pickle.load(another_text_file)

        self.text1.merge(self.text2)

    def generate(self, text_length):

        if text_length < 1:
            return

        final_text = [random.choice(self.text1.all_words())]

        while True:
            final_text.append(self.text1[final_text[-1]])
            if len(final_text) == text_length:
                return " ".join(final_text)


parser = argparse.ArgumentParser(description='Text generation')
parser.add_argument('-learn', nargs=2, help='Tokenization of the file. The first argument is initial text filename, '
                                            'the second is tokenized text filename')

parser.add_argument('-generate', nargs=3, help='Generate text. The first two arguments are tokenized text filenames. '
                                               'The third argument is words count of generated text.')

if parser.parse_args().learn is not None:
    file_names = parser.parse_args().learn
    text = Text(file_names[0])
    text.save(file_names[1])

elif parser.parse_args().generate is not None:
    arguments = parser.parse_args().generate
    generator = Generator(arguments[0], arguments[1])
    print(generator.generate(int(arguments[2])))
