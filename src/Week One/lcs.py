# -*- coding: utf-8 -*-
# @Author: jason-xuan
# @Date:   2017-07-17 01:42:38
# @Last Modified by:   jason-xuan
# @Last Modified time: 2017-07-17 03:26:12
import numpy as np
import pandas as pd
from itertools import product


def lcs(left: str, right: str) -> str:
    m, n = len(left), len(right)
    #最长匹配的长度
    max_len = 0
    #最长匹配对应在s1中的最后一位
    p = 0
    # a m*n table
    table = np.zeros((m + 1, n + 1)).astype(np.int)

    for i, j in product(range(m), range(n)):

        if left[i] == right[j]:
            table[i+1, j+1] = table[i,j] + 1

            if table[i+1, j+1] > max_len:
                max_len = table[i+1, j+1]
                p = i + 1

    return left[p-max_len:p]


def test(test_name: str, left: str, right: str, answer: str):
    result = lcs(left, right)
    print(f"""--------------------------------------------------------------------------------
test name:              {test_name}
left string:            {left}
right string:           {right}
longest substring:      {result}
test passed::           {answer == result}""")
    return answer == result


def test_all():
    test_data = pd.read_csv('test.csv')
    test_data[test_data.isnull()] = ''

    pass_num = 0
    len_data = len(test_data)

    for _, line in test_data.iterrows():
        flag = test(line['test_name'], line['left'], line['right'], line['result'])
        if flag: pass_num += 1


    print(f'test finished. total tests:\t{len_data},\tpassed tests:\t{pass_num},\t{pass_num/len_data *100}% passed')


if __name__ == '__main__':
    test_all()
