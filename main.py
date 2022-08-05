import requests
from bs4 import BeautifulSoup
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from VocabWord import VocabWord
from MainExcel import get_words


def filter_definition(word, definition):
    """
    takes the definition of the word out of the longer, complex sentence Merriam-Webster offers
    :param word: the word being looked up by the user
        example: diaphanous
    :param definition: the long, complex sentence offered by Merriam-Webster
        example: The definition of diaphanous is to...*definition*...See more examples
    :return: only the definition of the word
    """
    cut_out_beginning = f'The meaning of {word.upper()} is '  # remove the phrase introducing the definition
    return definition.replace(cut_out_beginning, '').split('.')[0]  # remove everything after the first period


def convert_conjugation_pos(conjugation):
    """
    takes the part of speech of the conjugation and abbreviates it if necessary
    :param conjugation: the conjugation of the word searched
    :return: the abbreviated or unaffected form of the conjugation part of speech
    """
    part_of_speech_dictionary = {
        "adjective": "adj.",
        "adverb": "adv.",
        "noun": "noun",
        "verb": "verb"
    }
    return part_of_speech_dictionary[conjugation]


def get_vocab_word_data(word):
    url = 'https://www.merriam-webster.com/dictionary/' + word
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    part_of_speech = soup.find('a', {'class': 'important-blue-link'}).text

    definition = soup.find('meta', {'name': 'description'})['content']

    conjugations_results = soup.find_all('div', attrs={'class': 'uro'})
    conjugations = []  # need a list of all available conjugations
    for conjugation in conjugations_results:
        conjugation_word = conjugation.find('span', attrs={'class': 'ure'}).text  # the actual conjugation
        conjugation_pos = conjugation.find('span', attrs={'class': 'fl'}).text  # pos means 'part of speech' ;)
        conjugation_result = conjugation_word + " (" + convert_conjugation_pos(conjugation_pos) + ")"
        conjugations.append(conjugation_result)
    vw = VocabWord(word, part_of_speech, filter_definition(word, definition), conjugations)
    return vw


assignment_vocab = input('Please enter the Pathname of your Excel spreadsheet: \n')  # the file (assignment)
# this file only has the vocab words and the column headers, nothing else
assignment_wb = load_workbook(assignment_vocab)
assignment_ws = assignment_wb['AP Vocab Lesson #1']
how_many_words = int(input('How many vocab words will you be studying?  '))
words = get_words(assignment_ws, how_many_words)  # the list of the words for the assignment
vocab_words = []  # the list of the words AND their part of speech, definition, and conjugations
for this_word in words:
    print(this_word)
    vocab_words.append(get_vocab_word_data(this_word))

# Part of Speech
for row in range(3, how_many_words+3):  # go from rows 2 through last row
    index_in_vocab_words = row - 3  # when row is 3, we are on the first vocab word, so index 0
    vocab_word = vocab_words[index_in_vocab_words]

    # Part of Speech
    assignment_ws['B' + str(row)].value = vocab_word.pos
    # Definition
    assignment_ws['C' + str(row)].value = vocab_word.definition
    # Conjugations
    assignment_ws['D' + str(row)].value = str(vocab_word.conjugations)

    # Wrap the text in the cells
    assignment_ws['C' + str(row)].alignment = Alignment(wrap_text=True)
    assignment_ws['D' + str(row)].alignment = Alignment(wrap_text=True)

assignment_wb.save(assignment_vocab)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    print('\nComplete!')
