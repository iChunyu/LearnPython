"""
Remove extra braces and replace extra authors with 'et al'

XiaoCY 2021-07-05
"""


import sys


def get_and_index(authors, max_count):
    cnt = 0
    idx = -1

    k = authors.find('and')
    while k >= 0:
        cnt += 1
        if cnt == max_count:
            idx = k
        k = authors.find('and', k+1)

    return idx


def clean_bib(in_filename, out_filename, max_author):
    if in_filename[-4:] != '.bib':
        print('Wrong file given.')
        return

    item_cnt = 0

    with open(in_filename) as in_file:
        bib = in_file.readlines()

    out_file = open(out_filename, 'w')
    for line in bib:
        # count items and ensure two blank lines between items
        if line[0] == '@':
            item_cnt += 1
            if item_cnt == 1:
                out_file.write(line)
            else:
                out_file.write('\n\n'+line)

        # remove extra braces and replace extra authors with 'et al'
        if '=' in line:
            idx_eq = line.find('=') + 1
            val = line[idx_eq:].strip()
            val = val.replace('{', '').replace('}', '')
            if val[-1] == ',':
                comma_end = True
                val = val[:-1]
            else:
                comma_end = False

            if 'author' in line:
                idx_and = get_and_index(val, max_author-1)
                if idx_and > 0:
                    val = val[:idx_and] + 'and et al'

            if comma_end:
                out_file.write(line[:idx_eq] + ' {' + val + '},\n')
            else:
                out_file.write(line[:idx_eq] + ' {' + val + '}\n')

    print(str(item_cnt) + ' items have been updated.')


def main():
    # sys.argv[0] = clean_bib.py
    if len(sys.argv) == 2:
        clean_bib(sys.argv[1], sys.argv[1], 3)
    elif len(sys.argv) == 3:
        clean_bib(sys.argv[1], sys.argv[2], 3)
    elif len(sys.argv) == 4:
        clean_bib(sys.argv[1], sys.argv[2], int(sys.argv[3]))


if __name__ == '__main__':
    main()
