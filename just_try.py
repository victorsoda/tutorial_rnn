import collections
import numpy as np

# data = ['a', 'a', 'a', 'b', 'c', 'c']
#
# counter = collections.Counter(data)
# print(counter.items())
# count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
# print(count_pairs)
# words, _ = list(zip(*count_pairs))
#
# word_to_id = dict(zip(words, range(len(words))))
#
# a = [word_to_id[word] for word in data if word in word_to_id]
# print(a)
#
#
# x = np.arange(1, 7)
# print(x)
# x = x.reshape([2, 3])
# print(x)

with open('data/train_data.txt', 'r', encoding='utf-8') as f:
    data = f.read().split(' ')
    counter = collections.Counter(data)
    print(counter['<unk>'])
    print(len(counter.items()))
    count_pairs = sorted(counter.items(), key=lambda x: (-x[1], x[0]))
    for pair in count_pairs[-100:]:
        print(pair)
    fre_counter = collections.Counter(counter.values())  # 记录出现i次的单词有多少个
    for i in range(1, 6):
        print(str(fre_counter[i]) + " words emerge " + str(i) + " times")
