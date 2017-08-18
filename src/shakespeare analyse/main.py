# -*- coding: utf-8 -*-

from reader import Doc
from analyse import analyse


def interactive_search():
    
    inverse_dict = Doc.get_inverse_dit()
    # interactive
    while True:
        print('Type "EXIT to exit"')
        key = input('search word: ')
        if key == "EXIT":
            break
        if key not in inverse_dict:
            print('the word you search is not presented in documents.')
        else:
            result = inverse_dict[key]
            print(f'word "{key}" found in those document(s):')
            for r in result:
                print(r)
            

if __name__ == '__main__':
    analyse()
    interactive_search()