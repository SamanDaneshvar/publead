"""Identify the research lead in a research group, by looking at the author names in the publications of the group.

This script loads a text file of BibTeX entries of papers. It then creates a dictionary of all authors, and counts
the number of papers were each author is the last author and also the second-to-last author.
In the end, it writes the dictionary into a CSV file.

Remarks:
- Papers with only 1 author won't count towards the last author count of their author.
- Papers with only 2 authors won't count towards the second-to-last author count of their authors.
"""

from publead import utils

import time
import re
import os
import csv


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
        A dictionary mapping authors to the number of papers were they were the last and second-to-last author:
            Key: Name of author
            Value: List of two integers. The first integer counts last author, the second counts second-to-last author
    """

    # Create empty dictionaries
    last_and_s2l_count = {}
    last_author_count = {}
    second_to_last_author_count = {}

    for authors_of_paper in authors_of_papers:
        # *string.split* will return a list of sub-strings, separated by ' and '
        authors = authors_of_paper.split(' and ')

        # Initialize: add all new authors to the dictionary with a value of [0, 0] (a list of two integers)
        for author in authors:
            if author not in last_and_s2l_count:
                last_and_s2l_count[author] = [0, 0]

        # Count the last author. We will ignore the papers that have only 1 author.
        if len(authors) > 1:
            last_author = authors[-1]
            # Increment the value in the dictionary. Note that all authors have already been added to the dictionary.
            # The first element in the list refers to the last-author count
            last_and_s2l_count[last_author][0] = last_and_s2l_count[last_author][0] + 1

        # Count the second-to-last author. We will ignore the papers that have only 1 or 2 authors.
        if len(authors) > 2:
            second_to_last_author = authors[-2]
            # Same as above
            # The second element in the list refers to the second-to-last-author count
            last_and_s2l_count[second_to_last_author][1] = last_and_s2l_count[second_to_last_author][1] + 1

    logger.info('Processed %s authors', len(last_and_s2l_count))

    return last_and_s2l_count


def write_stats_dictionary_to_csv(last_and_s2l_count):
    """Write the dictionary of last and second-to-last author counts to a CSV file"""

    # Constant
    OUTPUT_FILE_PATH = 'data/out/author stats.csv'

    # Create the directory if it does not exist.
    os.makedirs(os.path.dirname(OUTPUT_FILE_PATH), exist_ok=True)

    rows_to_write = []  # Create an empty list

    # Convert the dictionary into a list of rows. Each row will also be a list of items.
    for author, count_list in last_and_s2l_count.items():
        row = []  # Create an empty list
        # Assemble the row for this author
        row.append(author)
        row.extend(count_list)  # *extend* appends all items inside a iterable to the list
        # Append the row to *rows_to_write* and move on
        rows_to_write.append(row)

    # Assemble the header row
    header = ['Author', 'Last author count', 'Second-to-last author count']

    # Write to the CSV file
    with open(OUTPUT_FILE_PATH, 'w', newline='', encoding='utf-8') as csv_output_file:
        csv_writer = csv.writer(csv_output_file)
        csv_writer.writerow(header)
        csv_writer.writerows(rows_to_write)


def main():
    """The main function."""

    authors_of_papers = get_authors_of_papers()
    last_and_s2l_count = author_stats(authors_of_papers)
    write_stats_dictionary_to_csv(last_and_s2l_count)

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
