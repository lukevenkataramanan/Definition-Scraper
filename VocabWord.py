class VocabWord:
    def __init__(self, word, pos, definition, conjugations):
        self.word = word
        self.pos = pos  # part of speech
        self.definition = definition
        self.conjugations = ''
        for conjugation in conjugations:
            self.conjugations += conjugation + ', '
        # cut out last comma and space (2 characters)
        self.conjugations = self.conjugations[0: len(self.conjugations)-2]

    def __str__(self):
        return "Vocab Word: " + self.word + "\nPart of Speech: " + self.pos + \
               "\nDefinition: " + self.definition + "\nConjugations: " + str(self.conjugations)


if __name__ == '__main__':
    myWord = VocabWord('adjudication', 'noun', 'definition of adjudication', ['conj (1)', 'conj (2)', 'conj (3)'])
