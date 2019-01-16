"""Identify the research lead in a research group, by looking at the author names in the publications of the group,
and counting the number of papers were each author was the last author and also the second-to-last author.
"""

from publead import utils

import time
import re


def get_authors_of_papers():
    """Gets authors of papers

    This function loads the input file (containing all BibTeX entries), extracts the authors of each paper using regex.

    Returns:
        A list of strings. Each string contains all authors of a paper, in the form of
        "Author1 Name and Author2 Name and ..."
    """

    # Constants
    INPUT_FILE_PATH = 'data/in/papers.txt'

    # Load the entire input file
    with open(INPUT_FILE_PATH, 'r') as input_file:
        haystack = input_file.read()

    # The pattern to get the author line from BibTeX entries
    pattern = r"""
            (?<=                    # Lookbehind (won't be included in the match)
                (?:author|editor)   # "author" or "editor". In Python, you need to use a non-capturing group for this.
                \t                  # Tab
                =                   # =
                [ ]                 # Space (since the verbose flag ignores whitespace characters)
                {                   # {
            )

            .*                      # The dot meta-character matches any character except line breaks (optional)

            (?=                     # Lookahead (won't be included in the match)
                \},                 # },
            )
        """

    regex = re.compile(pattern, re.VERBOSE)

    # *findall* returns all non-overlapping matches as a list of strings
    authors_of_papers = regex.findall(haystack)

    logger.info('Processed %s papers', len(authors_of_papers))

    return authors_of_papers


def author_stats(authors_of_papers):
    """Counts last authors and second-to-last authors

    Args:
        authors_of_papers: A list of strings. Each string should contain all authors of a paper, in the form of
        "Author1 Name and Author2 Name and ..."
    Returns:
        last_author_count: A dictionary mapping authors to the number of papers were they were the last author.
            Papers with only one author will be ignored in this.
        second_to_last_author_count: The same as above, but for second to last authors.
            Papers with only two authors will be ignored in this.
    """

    # Create empty dictionaries
    last_author_count = {}
    second_to_last_author_count = {}

    for authors_of_paper in authors_of_papers:
        # *string.split* will return a list of sub-strings, separated by ' and '
        authors = authors_of_paper.split(' and ')

        # Count the last author. We will ignore the papers that have only 1 author.
        if len(authors) > 1:
            last_author = authors[-1]

            # If the last author already exists in the count dictionary, increment the value. If not, add it to the
            # dictionary with value 1
            if last_author in last_author_count:
                last_author_count[last_author] = last_author_count[last_author] + 1
            else:
                last_author_count[last_author] = 1

        # Count the second-to-last author. We will ignore the papers that have only 1 or 2 authors.
        if len(authors) > 2:
            second_to_last_author = authors[-2]

            # Same as above
            if second_to_last_author in second_to_last_author_count:
                second_to_last_author_count[second_to_last_author] = \
                    second_to_last_author_count[second_to_last_author] + 1
            else:
                second_to_last_author_count[second_to_last_author] = 1

    return last_author_count, second_to_last_author_count


def main():
    """The main function.

    Every time the script runs, it will call this function.
    """

    authors_of_papers = get_authors_of_papers()
    last_author_count, second_to_last_author_count = author_stats(authors_of_papers)

    # Log run time
    logger.info('@ %.2f seconds: Run finished', time.process_time())


''' 
The following lines will be executed only if this .py file is run as a script,
and not if it is imported as a module.
• __name__ is one of the import-related module attributes, which holds the name of the module.
• A module's __name__ is set to '__main__' when it is running in
the main scope (the scope in which top-level code executes).  
'''
if __name__ == '__main__':
    logger = utils.configure_root_logger()
    utils.set_working_directory()
    main()
