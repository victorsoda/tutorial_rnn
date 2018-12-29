import os
import re
import collections

DATA_PATH = '../data/'

TRAIN_PATH = DATA_PATH + 'train/'
VALID_PATH = DATA_PATH + 'valid/'
TEST_PATH = DATA_PATH + 'test/'

punc = ['\n', '“', '”', '[', ']']
punc_pattern = r"([。！？\s+]/w)"

cnt_thres = 6


def del_punc(word):
    ret = word
    for p in punc:
        ret = ret.replace(p, '')
    return ret


def articles_to_sentence_file(path, thres, is_training, train_cnter=None):
    all_words = []
    for file in os.listdir(path):
        with open(path + file, 'r', encoding='gbk') as f:
            article = f.read()
            lines = article.split('\n')
            sentences = []
            for line in lines:
                if re.search(punc_pattern, line) is not None:
                    s = re.split(punc_pattern, line)
                    s.append("")
                    s = ["".join(i) for i in zip(s[0::2], s[1::2])][:-1]
                    sentences.extend(s)
                elif len(line) > 3:  # 防止空行
                    sentences.append(line)
            for s in sentences:
                s = s.split('  ')[:-1]
                while '' in s:
                    s.remove('')
                wordlist = [del_punc(x.split('/')[0]) for x in s]
                wordlist.append('\n')
                all_words.extend(wordlist)
    counter = collections.Counter(all_words)
    # fre_counter = collections.Counter(counter.values())   # 记录出现i次的单词有多少个
    # dec = 0
    # for i in range(1, thres):
    #     print(str(fre_counter[i]) + " words emerge " + str(i) + " times")
    #     dec += fre_counter[i]

    print("vocab_size =", len(counter.items()))
    # print("after threshold =", len(counter.items()) - dec)

    with open('data/' + path.split('/')[-2] + '_data.txt', 'w', encoding='utf-8') as f:
        for w in all_words:
            if counter[w] < thres:  # 降低vocab_size的大小，当thres=6时训练集的vocab_size = 11250 + 1（原来为49003）
                f.write('<unk> ')
                continue
            elif not is_training and w not in train_cnter:  # 对于valid和test，不在训练集中出现的高频词也记为<unk>
                f.write('<unk> ')
                continue
            f.write(w + ' ')
    print("Finished writing " + path.split('/')[-2] + '_data.txt')
    return counter


if __name__ == '__main__':
    train_counter = articles_to_sentence_file(TRAIN_PATH, cnt_thres, is_training=True)
    _ = articles_to_sentence_file(VALID_PATH, cnt_thres, is_training=False, train_cnter=train_counter)
    _ = articles_to_sentence_file(TEST_PATH, cnt_thres, is_training=False, train_cnter=train_counter)







