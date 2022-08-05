

def get_words(ws, how_many_words):
    """
    uses the Excel file to see what the vocab words are for the assignment
    :return: a list of all the words for the assignment
    """
    words = []  # the list of the vocab words from the assignment
    for row in range(3, how_many_words+3):  # go from rows 2 through last row
        word = ws['A' + str(row)].value
        words.append(word)
    return words


if __name__ == '__main__':
    pass
