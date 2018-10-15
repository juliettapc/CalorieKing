"""
Parses the bad users list and provides a function for querying if a user is in
the list.
"""

# Matching comment lines:
import re
is_comment_line = re.compile(r'\s*#')
is_id_line = re.compile(r'([0-9a-f\-]+)\s*(.*)\n')

bad_ids = dict()

list_fh = open('bad-users.txt', 'r')
for line in list_fh:
    # Skip comment lines
    if is_comment_line.match(line):
        continue
    m = is_id_line.match(line)
    if m == None:
        continue
    # Store the explanation under the user id:
    bad_ids[m.group(1)] = m.group(2)

def is_bad_user (ck_id):
    if ck_id in bad_ids:
        return True
    return False

def why_bad_user (ck_id):
    if ck_id in bad_ids:
        return bad_ids[ck_id]
    return ck_id + ' is a good user...?'


# Some tests
if __name__ == '__main__':
    """
    A quick test to make sure that baduserlist.py works properly
    """

    from baduserslist import *

    print "1..2"

    message = "ok 1 - user f00a9af0-a is in bad list"
    if not is_bad_user('f00a9af0-a'):
        message = "not " + message
    print message

    message = "ok 2 - message for f00a9af0-a is accurate"
    if not why_bad_user('f00a9af0-a') == 'too many zero entries':
        message = "not " + message
    print message

