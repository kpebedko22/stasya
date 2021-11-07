import os


def get_sorted_frequencies(text: str):
    """ 
    Получить отсортированные частоты всех символов
    """
    freqs = dict()

    for symbol in text:
        s = symbol.lower()
        freqs[s] = freqs.get(s, 0) + 1

    len_text = len(text)
    freqs = {k: (v / len_text) for k, v in sorted(freqs.items(), key=lambda item: item[1], reverse=True)}

    return freqs


def convert_frequencies(freqs: dict):
    return ''.join(k for k in freqs.keys()), [v for v in freqs.values()]


def get_last_symbol(counts: list):
    total = sum(counts)

    length = len(counts)
    count, last_char_index = 0, 0

    for i in range(length // 2):
        count += counts[i]
        if (count - (total / 2) >= 0):
            last_char_index = i + 1
            break
    return last_char_index


def devide_chars(x, y, itr, code):
    '''makes the tree recursively'''
    if len(x) == 2:
        return {x[0]: code + '0', x[1]: code + '1'}
    if len(x) == 1:
        return {x: code}
    index = get_last_symbol(y)

    right = devide_chars(x[index+1:], y[index+1:], itr + 1, code + '1')
    left = devide_chars(x[:index+1], y[:index+1], itr + 1, code + '0')
    right.update(left)
    return right


def get_cypher(text: str):

    freqs = get_sorted_frequencies(text)
    symbols, counts = convert_frequencies(freqs)

    last_symb = get_last_symbol(counts)
    right_s, right_c = symbols[last_symb:], counts[last_symb:]
    left_s, left_c = symbols[:last_symb], counts[:last_symb]

    r = devide_chars(right_s, right_c, 1, '1')
    l = devide_chars(left_s, left_c, 1, '0')
    r.update(l)

    for s, c in zip(symbols, counts):
        print('Символ \'{}\'. Частота {}. Код {}'.format(s, round(c, 4), r[s]))

    print('\r\nЗакодированная строка', text)
    for letter in text:
        print(r[letter.lower()], end=' ')


def main():
    text = "THE ESSENTIAL FEATURE"
    # text = "способ кодирования"
    get_cypher(text)


if __name__ == "__main__":
    os.system('cls')

    print('\nLab 2\n')

    main()

    print('\n\nEnd\n\n')
