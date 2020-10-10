# publead
A simple tool that helps you identify the research lead in a research group, by looking at the author names in the publications of the group.

## Usage
The main script, find_lead.py, loads a text file containing BibTeX entries of papers. A sample input file is included ("data/in/papers.txt")

It then creates a dictionary of all authors, and counts the number of papers where each author is the last author and also the second-to-last author.

In the end, it writes the dictionary into a CSV file. The output CSV file will be written to "data/out/author stats.csv"

## Remarks
- Papers with only 1 author won't count towards the last author count of their author.
- Papers with only 2 authors won't count towards the second-to-last author count of their authors.
