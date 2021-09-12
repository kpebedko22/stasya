import os
import random

CYRILLIC = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def load_text(filename):
    try:
        with open(file=filename, mode='r', encoding='utf-8') as f:
            res = f.read()
        return res
    except FileNotFoundError:
        print('FileNotFoundError: ' + filename)
        return None


def get_frequencies(text: str):

    freqs = {symb: 0 for symb in CYRILLIC}

    for symbol in text:
        if symbol.lower() in CYRILLIC:
            freqs[symbol.lower()] += 1

    return freqs


def simple_replacement_encryption(text: str):

    copy_cyrillic = [symb for symb in CYRILLIC]
    random.shuffle(copy_cyrillic)

    alphabet = {symb: enc for symb, enc in zip(CYRILLIC, copy_cyrillic)}

    res = ''
    for symb in text:
        if symb.lower() in alphabet:
            res += alphabet[symb.lower()] if symb.islower() else alphabet[symb.lower()].upper()
        else:
            res += symb

    return res


def decoding_by_frequencies(text: str, ref_freqs: dict, text_freqs: dict):

    sorted_ref_freqs = {k: v for k, v in sorted(ref_freqs.items(), key=lambda item: item[1], reverse=True)}
    sorted_text_freqs = {k: v for k, v in sorted(text_freqs.items(), key=lambda item: item[1], reverse=True)}
    print('\r\nЭталонные частоты (текст 1)\r\n', sorted_ref_freqs, '\r\n')
    print('\r\nЧастоты для расшифровки (шифротекст 2)\r\n', sorted_text_freqs, '\r\n')

    alphabet = {k: v for k, v in zip(sorted_text_freqs.keys(), sorted_ref_freqs.keys())}

    res = ''
    for symb in text:
        if symb.lower() in alphabet:
            res += alphabet[symb.lower()] if symb.islower() else alphabet[symb.lower()].upper()
        else:
            res += symb

    return res


def main():

    filenames = [
        'texts/ono.txt',
        'texts/ono2.txt',
        'texts/zelenaya-milya.txt',
        'texts/lordoftherings.txt',
        'texts/kapdochka.txt'
    ]

    filename_1 = filenames[random.randint(0, len(filenames) - 1)]  # 'texts/ono.txt'
    filename_2 = filenames[random.randint(0, len(filenames) - 1)]  # 'texts/lordoftherings.txt'

    print('First Text - ', filename_1)
    print('Second Text - ', filename_2)

    text_1 = load_text(filename_1)
    reference_frequencies = get_frequencies(text_1)

    # reference_frequencies = {  'о':0.1097, 'е':0.0845, 'а':0.0801, 'и':0.0735, 'н':0.067,  'т':0.0626, 'с':0.0547, 'р':0.0473,
    #                 'в':0.0454, 'л':0.044,   'к':0.0349, 'м':0.0321, 'д':0.0298, 'п':0.0281, 'у':0.0262, 'я':0.0201,
    #                 'ы':0.019,  'ь':0.0174,  'г':0.017,  'з':0.0165, 'б':0.0159, 'ч':0.0144, 'й':0.0121, 'х':0.0097,
    #                 'ж':0.0094, 'ш':0.0073,  'ю':0.0064, 'ц':0.0048, 'щ':0.0036, 'э':0.0032, 'ф':0.0026, 'ъ':0.0004
    #                 }

    text_2 = load_text(filename_2)
    encoded_text_2 = simple_replacement_encryption(text_2)
    text_2_frequencies = get_frequencies(encoded_text_2)

    decoded_text_2 = decoding_by_frequencies(encoded_text_2, reference_frequencies, text_2_frequencies)

    # print(decoded_text_2[5000: 7000])
    print(decoded_text_2)


if __name__ == "__main__":
    os.system('cls')

    print('\nLab 1\n')

    main()

    print('\n\nEnd\n\n')
