import re
import shlex

def split_words_and_quoted_text(text):
    """Split string text by space unless it is
       wrapped inside double quotes, returning a list
       of the elements.

       For example
       if text =
       'Should give "3 elements only"'

       the resulting list would be:
       ['Should', 'give', '3 elements only']
    """
    text_with_double_quates = re.findall(r'\".+\"', text)[0]
    text_without_double_quates = text.replace(text_with_double_quates, '').split(' ')
    for num, word in enumerate(text_without_double_quates):
        if word == '':
            text_without_double_quates[num] = text_with_double_quates.strip('"')

    return text_without_double_quates


# Solution from pybit.es using shlex
def split_words_and_quoted_text(text):
    return shlex.split(text)