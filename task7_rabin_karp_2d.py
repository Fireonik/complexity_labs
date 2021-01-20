def column_hash(matrix, column, row):
    hash, curr, radix = [], 0, 256

    for i in range(0, column):
        for j in reversed(range(0, row)):
            curr = curr + (radix ** (row - j - 1) * ord(matrix[j][i])) % 101
        hash.append(curr % 101);
        curr = 0
    return hash


def is_the_pattern(text, row, column, match_found):
    text = [text[i][column:pattern_columns + column] for i in range(row, pattern_rows + row)]

    if text == pattern:
        match_found = 1
        print("Pattern found at ", row, ",", column,)
    return match_found


def rolling_column_hash(text_hash, next_row):
    radix = 256

    for j in range(len(text_hash)):
        text_hash[j] = (text_hash[j] * radix + ord(text[next_row][j])) % 101
        text_hash[j] = text_hash[j] - (radix ** (pattern_rows) * ord(text[next_row - pattern_rows][j])) % 101
        text_hash[j] = text_hash[j] % 101
    return text_hash


def search(text, pattern):
    pattern_hash, text_hash = [], []
    pattern_value, text_value, match_found = 0, 0, 0
    radix = 256

    text_hash = column_hash(text, text_columns, pattern_rows)
    pattern_hash = column_hash(pattern, pattern_columns, pattern_rows)

    for i in range(len(pattern_hash)):
        pattern_value = pattern_value + (radix ** (len(pattern_hash) - i - 1) * pattern_hash[i] % 101)
    pattern_value = pattern_value % 101

    for i in range(pattern_rows - 1, text_rows):
        column, text_value = 0, 0

        for j in range(len(pattern_hash)):
            text_value = text_value + (radix ** (len(pattern_hash) - j - 1) * text_hash[j]) % 101
        text_value = text_value % 101

        if text_value == pattern_value:
            match_found = is_the_pattern(text, i + 1 - pattern_rows, column, match_found)

        else:
            for k in range(len(pattern_hash), len(text_hash)):

                text_value = text_value * radix + (text_hash[k]) % 101
                text_value = text_value - (radix ** (len(pattern_hash)) * (text_hash[k - len(pattern_hash)])) % 101
                text_value = text_value % 101
                column = column + 1

                if pattern_value == text_value:
                    match_found = is_the_pattern(text, i + 1 - pattern_rows, column, match_found)

        if i + 1 < text_rows:
            text_hash = rolling_column_hash(text_hash, i + 1)

    if match_found == 0:
        print("Pattern not found")


text = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
pattern = [['E', 'F'], ['H', 'I']]

text_rows, text_columns = 3, 3
pattern_rows, pattern_columns = 2, 2

search(text, pattern)