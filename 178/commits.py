from collections import Counter
import os
import re
from urllib.request import urlretrieve
from dateutil.parser import parse

commits = os.path.join(os.getenv("TMP", "/tmp"), 'commits')
urlretrieve(
    'https://bites-data.s3.us-east-2.amazonaws.com/git_log_stat.out',
    commits
)

# you can use this constant as key to the yyyymm:count dict
YEAR_MONTH = '{y}-{m:02d}'


def get_min_max_amount_of_commits(commit_log: str = commits,
                                  year: str = None) -> (str, str):
    """
    Calculate the amount of inserts / deletes per month from the
    provided commit log.

    Takes optional year arg, if provided only look at lines for
    that year, if not, use the entire file.

    Returns a tuple of (least_active_month, most_active_month)
    """
    with open(commit_log, 'r') as file:
        git_commits = file.read()

    rows = git_commits.splitlines()

    counter = Counter()
    for row in rows:
        date = parse(row[8:32])
        splitted = row.split(', ')
        insertions = splitted[1].split()[0]

        try:
            deletions = splitted[2].split()[0]
        except IndexError:
            deletions = 0

        sum_of_changes = int(insertions) + int(deletions)

        if date.year == year:
            year_month = YEAR_MONTH.format(y=date.year, m=date.month)

            counter.update({year_month: sum_of_changes})
        elif year is None:
            year_month = YEAR_MONTH.format(y=date.year, m=date.month)
            counter.update({year_month: sum_of_changes})

    most_common = counter.most_common()
    return most_common[-1][0], most_common[0][0]
