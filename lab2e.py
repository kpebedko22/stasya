from collections import Counter
import operator
import os

class ShanonFanno():

    def __init__(self):
        self.sum_logs_with_pis = 0
        self.size_after_compress = 0
        self.sorted_s = ""
        self.char_dict = dict()

    def devide_chars(self, x, itr, code):
        if len(x) == 2:
            return {x[0]: code + '0', x[1]: code + '1'}
        if len(x) == 1:
            return {x: code}
        index = self.break_the_node(x)

        right = self.devide_chars(x[index+1:], itr + 1, code + '1')
        left = self.devide_chars(x[:index+1], itr + 1, code + '0')
        left.update(right)
        return left

    def make_count(self):
        self.char_dict = dict(Counter(self.sentence))
        char_ls = sorted(self.char_dict.items(), key=operator.itemgetter(1), reverse=True)
        sorted_s = ""
        for i in char_ls:
            sorted_s += i[0]
        return self.char_dict, sorted_s

    def break_the_node(self, node):
        total = 0
        for i in node:
            total += self.char_dict[i]
        length = len(node)
        count = 0
        last_char_index = 0
        for i in range(length//2):
            count += self.char_dict[self.sorted_s[i]]
            if (count - (total/2) >= 0):
                last_char_index = i + 1
                break
        return last_char_index

    def do_the_work(self, s):

        self.sentence = s
        self.total = len(s)
        self.char_dict, self.sorted_s = self.make_count()

        last_char_index = self.break_the_node(self.sorted_s)
        left = self.sorted_s[:last_char_index]
        right = self.sorted_s[last_char_index:]

        left_tree = self.devide_chars(left, 1, "0")
        right_tree = self.devide_chars(right, 1, "1")
        
        left_tree.update(right_tree)
        self.write_final_logs(left_tree)

    def write_final_logs(self, code):
        for k, v in code.items():
            print('Символ \'{}\'. Вхождения символа: {}. Код {}'.format(k,self.char_dict[k], v))

        print('\r\nЗакодированная строка', self.sentence)
        for letter in self.sentence:
            print(code[letter], end=' ')


def main():
    text = "THE ESSENTIAL FEATURE"
    # text = "способ кодирования"
    sh = ShanonFanno()
    sh.do_the_work(text)


if __name__ == "__main__":
    os.system('cls')

    print('\nLab 2\n')

    main()

    print('\n\nEnd\n\n')
