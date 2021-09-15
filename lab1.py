import os
import random

CYRILLIC = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']


def load_text(filename):
    """ 
    Функция считывания текста из файла с названием filename
    Обернуто в структуру try-except чтобы в случае ошибки отловить ее
    ошибка - файл не найден
    вернет None, хотя по хорошему надо сделать выход из проги
    
    Открывает файл на чтение 'r' с кодировкой 'utf-8'
    """
    try:
        with open(file=filename, mode='r', encoding='utf-8') as f:
            res = f.read()
        return res
    except FileNotFoundError:
        print('FileNotFoundError: ' + filename)
        return None


def get_frequencies(text: str):
    """ 
    Получить частоты букв
    """

    # Создаем словарь, где ключи - это буквы кирилицы
    # а значения равны нулям
    # т.е. каждая буква встречается ноль раз
    # 
    # { 'а' : 0,
    #   'б' : 0,
    #   ...
    #   'я' : 0
    # }
    freqs = {symb: 0 for symb in CYRILLIC}

    # text - это строка
    # питон позволяет фориком пройтись по каждому символу
    # поэтому для каждого символа в тексте
    # приводим символ к нижнему регистру функцией lower()
    # и проверяем что он есть в массиве русских букв CYRILLIC
    # если символ есть (условие верно), засчитываем этот символ в словарь
    # 
    # обращение к словарю осуществляется как и в массиве
    # в квадратных скобках указывается ключ
    # т.к. в словаре у нас записаны буквы в нижнем регистре - используем также функцию lower()
    # если буква и так нижнего регистра то вообще пофиг
    for symbol in text:
        if symbol.lower() in CYRILLIC:
            freqs[symbol.lower()] += 1

    # ну и возвращаем этот словарь
    # примерно выглядит так
    # { 'а' : 47,
    #   'б' : 8,
    #   ...
    #   'я' : 15
    # }
    return freqs


def simple_replacement_encryption(text: str):
    """ 
    Выполнить шифровку текста text алгоритмом простой замены
    т.к. нигде не сказано как именно происходит замена
    то будем рандомно назначать каждой букве новое значение 
    """

    # сделаем копию массива русских букв 
    # (не очень красиво, но надежно - массив будет абсолюто новый и не будет содержать ссылок на массив CYRILLIC)
    # и перемешаем их функцией shuffle из библиотеки random
    copy_cyrillic = [symb for symb in CYRILLIC]
    random.shuffle(copy_cyrillic)

    # делаем словарь где каждой букве алфавита сопоставляется ее новое значение
    # { 'а' : 'р',
    #   'б' : 'ш',
    #   ...
    #   'я' : 'г'
    # }
    # 
    # тут работает функция zip которая два итерируемых объекта позволяет проходить одновременно
    # т.е. мы берем букву алфавита и букву из перемешанного массива
    # и сопоставляем их
    alphabet = {symb: enc for symb, enc in zip(CYRILLIC, copy_cyrillic)}

    # строка res - будет зашифрованным текстом
    res = ''

    # для каждого символа текста проверяем
    # что символ в нижнем регистре есть в полученном алфавите в качестве ключа
    for symb in text:
        if symb.lower() in alphabet:

            # к результату цепляем новую букву в нижнем/верхнем регистре 
            # в зависимости от того какая была в исходном тексте
            res += alphabet[symb.lower()] if symb.islower() else alphabet[symb.lower()].upper()
        else:

            # иначе просто цепляем символ будь то запятая/пробел/точка и тд
            res += symb

    # возвращаем зашифрованный текст
    return res


def decoding_by_frequencies(text: str, ref_freqs: dict, text_freqs: dict):
    """ 
    Декодирование (расшифровка) с помощью частотного анализа
    где 
    text - это зашифрованный текст
    ref_freqs - частоты в качестве эталонных
    text_freqs - частоты в тексте

    Очевидно что надо восстановить каждой букве зашифрованного текста ее настоящую
    """

    # отсортируем частоты по убыванию
    # получим что-то типа
    # 
    # для эталонных частот
    # { 'о' : 147,
    #   'е' : 130,
    #   ...
    #   'ё' : 1
    # }
    # 
    # для частот зашифрованного текста
    # { 'т' : 147,
    #   'г' : 130,
    #   ...
    #   'ш' : 1
    # }
    # 
    sorted_ref_freqs = {k: v for k, v in sorted(ref_freqs.items(), key=lambda item: item[1], reverse=True)}
    sorted_text_freqs = {k: v for k, v in sorted(text_freqs.items(), key=lambda item: item[1], reverse=True)}
    print('\r\nЭталонные частоты (текст 1)\r\n', sorted_ref_freqs, '\r\n')
    print('\r\nЧастоты для расшифровки (шифротекст 2)\r\n', sorted_text_freqs, '\r\n')

    # составим словарь
    # где ключами будут буквы зашифрованного текста
    # а значениями - 'реальные' буквы - ну чисто по частотам...
    alphabet = {k: v for k, v in zip(sorted_text_freqs.keys(), sorted_ref_freqs.keys())}

    # схема такая же - пройтись по каждой букве текста и для нее поставить новое
    # типа расшифровать
    res = ''
    for symb in text:
        if symb.lower() in alphabet:
            res += alphabet[symb.lower()] if symb.islower() else alphabet[symb.lower()].upper()
        else:
            res += symb

    # вернуть результат
    return res


def main():

    # список с разными текстами
    filenames = [
        'texts/ono.txt',
        'texts/ono2.txt',
        'texts/zelenaya-milya.txt',
        'texts/lordoftherings.txt',
        'texts/kapdochka.txt'
    ]

    # рандомно выбрать два текста
    # первый будет в качестве эталона
    # второй - будем зашифровывать и расшифровывать
    filename_1 = filenames[random.randint(0, len(filenames) - 1)]  # 'texts/ono.txt'
    filename_2 = filenames[random.randint(0, len(filenames) - 1)]  # 'texts/lordoftherings.txt'

    print('First Text - ', filename_1)
    print('Second Text - ', filename_2)

    # загрузим первый текст и получим его частоты
    text_1 = load_text(filename_1)
    reference_frequencies = get_frequencies(text_1)

    # reference_frequencies = {  'о':0.1097, 'е':0.0845, 'а':0.0801, 'и':0.0735, 'н':0.067,  'т':0.0626, 'с':0.0547, 'р':0.0473,
    #                 'в':0.0454, 'л':0.044,   'к':0.0349, 'м':0.0321, 'д':0.0298, 'п':0.0281, 'у':0.0262, 'я':0.0201,
    #                 'ы':0.019,  'ь':0.0174,  'г':0.017,  'з':0.0165, 'б':0.0159, 'ч':0.0144, 'й':0.0121, 'х':0.0097,
    #                 'ж':0.0094, 'ш':0.0073,  'ю':0.0064, 'ц':0.0048, 'щ':0.0036, 'э':0.0032, 'ф':0.0026, 'ъ':0.0004
    #                 }

    # загрузим второй текст, зашифруем и получим его частоты
    text_2 = load_text(filename_2)
    encoded_text_2 = simple_replacement_encryption(text_2)
    text_2_frequencies = get_frequencies(encoded_text_2)

    # расшифруем второй текст через эталонные частоты
    decoded_text_2 = decoding_by_frequencies(encoded_text_2, reference_frequencies, text_2_frequencies)

    # print(decoded_text_2[5000: 7000])
    print(decoded_text_2)


if __name__ == "__main__":
    os.system('cls')

    print('\nLab 1\n')

    main()

    print('\n\nEnd\n\n')
