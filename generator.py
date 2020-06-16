import numpy.random as nprand


class Generator:
    EOS = ['.', '!', '?', '...']
    PUNCTUATION = [',', '.', '!', '?', '...']

    def __init__(self, text_file):
        text_lines = open(text_file, 'r', encoding='utf8').read().splitlines()
        self.word_list = sum([line.split() for line in text_lines], [])
        self.variants = dict()
        self.probabilities = dict()
        self._prepare_word_list()
        self._wrap_into_dict()
        self._count_probabilities()

    def _prepare_word_list(self):
        self.word_list = list(filter(lambda x: x != '', self.word_list))
        for i in range(len(self.word_list)):
            j = 1
            while j < len(self.word_list[i]) and not self.word_list[i][-j].isalpha():
                j += 1
            if j == 1 and self.word_list[i][-j].isalpha():
                self.word_list[i] = [self.word_list[i]]
            else:
                j -= 1
                self.word_list[i] = [self.word_list[i][:-j], self.word_list[i][-j]]
        self.word_list = sum(self.word_list, [])

    def _wrap_into_dict(self):
        for i in range(len(self.word_list) - 1):
            if self.word_list[i] in self.variants:
                if self.word_list[i + 1] in self.variants[self.word_list[i]]:
                    self.variants[self.word_list[i]][self.word_list[i + 1]] += 1
                else:
                    self.variants[self.word_list[i]][self.word_list[i + 1]] = 1
            else:
                self.variants[self.word_list[i]] = {self.word_list[i + 1]: 1}

    def _count_probabilities(self):
        for word, variant in self.variants.items():
            common_amount = sum(variant.values())
            self.probabilities[word] = []
            for next_word, frequency in variant.items():
                self.probabilities[word].append(frequency / common_amount)
            self.variants[word] = list(variant.keys())

    def generate_random_word(self, previous_word=None):
        if previous_word is None:
            ret = nprand.choice(list(self.variants.keys()))
            while ret in self.PUNCTUATION:
                ret = nprand.choice(list(self.variants.keys()))
            return ret
        return nprand.choice(self.variants[previous_word],
                             p=self.probabilities[previous_word])

    def generate_random_sentence(self):
        current_word = None
        sentence = []
        while current_word not in self.EOS:
            current_word = self.generate_random_word(current_word)
            if current_word in self.PUNCTUATION:
                sentence[-1] = sentence[-1] + current_word
            else:
                sentence.append(current_word)
        return ' '.join(sentence).capitalize()

    def generate_random_text(self, sentence_amount=None):
        if sentence_amount is None:
            sentence_amount = nprand.randint(5, 15)
        text = ''
        for i in range(sentence_amount):
            text += self.generate_random_sentence()
        return text
