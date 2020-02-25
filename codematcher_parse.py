import codematcher as cm
import re
import multiprocessing
import os
from nltk.stem import PorterStemmer
import nltk
import operator
import time
import numpy as np

total_files = 41025
path_from = 'f://jacoma_janalyzer/'
path_to = 'f://jacoma_parse/'
n_threads = 100

type_cd = ['CD']
type_cc = ['CC']
type_in = ['IN']
type_to = ['TO']
type_jj = ['JJ', 'JJR', 'JJS']
type_nn = ['NN', 'NNS', 'NNP', 'NNPS']
type_rb = ['RB', 'RBR', 'RBS']
type_vb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
type_ky = ['KY']
type_all = type_cd + type_cc + type_in + type_to + type_jj + type_nn + type_rb + type_vb + type_ky


def code_comment(idx):
    file = path_from + 'file_' + str(idx) + '_Comment.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_comment = infile.readlines()

        for i in range(len(code_comment)):
            line = str(code_comment[i])
            line = line[line.index(';') + 2:-2]
            line = re.sub(';', ' ', line)
            line = re.sub(' +', ' ', line).strip()
            if line == '':
                line = '[]'
            code_comment[i] = line + '\n'

        cm.save_txt(path_to + 'comment/comment' + str(idx) + '.txt', code_comment)
    print('comment over: ' + str(idx))


def code_javadoc(idx):
    file = path_from + 'file_' + str(idx) + '_Javadoc.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_javadoc = infile.readlines()

        for i in range(len(code_javadoc)):
            line = str(code_javadoc[i])
            line = line[line.index(';') + 1:-1]
            line = re.sub(';', ' ', line)
            line = re.sub(' +', ' ', line).strip()
            code_javadoc[i] = line + '\n'

        cm.save_txt(path_to + 'javadoc/javadoc' + str(idx) + '.txt', code_javadoc)
    print('javadoc over: ' + str(idx))


def code_modifier(idx):
    file = path_from + 'file_' + str(idx) + '_Modifiers.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_modifier = infile.readlines()

        for i in range(len(code_modifier)):
            line = str(code_modifier[i])
            line = line[line.index(';') + 2:-2]
            if line == '':
                line = '[]'
            code_modifier[i] = line + '\n'

        cm.save_txt(path_to + 'modifier/modifier' + str(idx) + '.txt', code_modifier)
    print('modifier over: ' + str(idx))


def code_method(idx):
    file = path_from + 'file_' + str(idx) + '_Method.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code = infile.readlines()

        code_method = list()
        code_package = list()
        for i in range(len(code)):
            line = str(code[i])
            line = line[line.index(';') + 1:-1]
            line = line.split(',')
            method = '[]\n'
            package = '[]\n'
            if len(line) == 3:
                package = line[1] + '\n'
                method = line[2] + '\n'
            code_method.append(method)
            code_package.append(package)

        cm.save_txt(path_to + 'method/method' + str(idx) + '.txt', code_method)
        cm.save_txt(path_to + 'package/package' + str(idx) + '.txt', code_package)
    print('method over: ' + str(idx))


def code_parameter(idx):
    file = path_from + 'file_' + str(idx) + '_Parameter.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_parameter = infile.readlines()

        for i in range(len(code_parameter)):
            line = str(code_parameter[i])
            line = line[line.index(';') + 1:-2]
            if line == '':
                line = '[]'
            code_parameter[i] = line + '\n'

        cm.save_txt(path_to + 'parameter/parameter' + str(idx) + '.txt', code_parameter)
    print('parameter over: ' + str(idx))


def code_return(idx):
    file = path_from + 'file_' + str(idx) + '_Return.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_return = infile.readlines()

        for i in range(len(code_return)):
            line = str(code_return[i])
            line = line[line.index(';') + 1:-1]
            if line == '':
                line = '[]'
            code_return[i] = line + '\n'

        cm.save_txt(path_to + 'return/return' + str(idx) + '.txt', code_return)
    print('return over: ' + str(idx))


def code_parsed(idx):
    file = path_from + 'file_' + str(idx) + '_ParsedCode.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_parsed = infile.readlines()

        for i in range(len(code_parsed)):
            line = str(code_parsed[i])
            line = line[line.index(';') + 1:-1]
            body = []
            if ';' in line:
                line = line.split(';')
                for j in range(len(line)):
                    l = line[j].split(',')
                    if len(l) == 3:
                        body.append(l[1])
            body = ','.join(body)
            if body == '':
                body = '[]'
            code_parsed[i] = body + '\n'

        cm.save_txt(path_to + 'parsed/parsed' + str(idx) + '.txt', code_parsed)
    print('parsed over: ' + str(idx))


def code_source(idx):
    file = path_from + 'file_' + str(idx) + '_SourceCode.csv'
    if not os.path.exists(file):
        return
    with open(file, 'r', encoding='utf-8') as infile:
        code_source = infile.readlines()

        for i in range(len(code_source)):
            line = str(code_source[i])
            line = line[line.index(';') + 1:-1]
            if '[]' == line:
                code_source[i] = '[]\n'
            else:
                sub = line.split(';')
                cmt = ''
                for s in sub:
                    if s == '':
                        cmt += ';'
                        continue
                    s = s.strip()
                    if not s.startswith('//') and not s.startswith('/*') and not s.startswith('*') and \
                            not s.startswith('@') and not s.endswith('*') and not s.endswith('*/'):
                        cmt += s
                cmt = re.sub(' +', ' ', cmt).strip()
                cmt = re.sub(';+', ';', cmt)
                code_source[i] = cmt + '\n'

        cm.save_txt(path_to + 'source/source' + str(idx) + '.txt', code_source)
    print('source over: ' + str(idx))


def multi_comment():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('comment: ' + str(i))
        pool.apply_async(code_comment, (i,))
    pool.close()
    pool.join()


def multi_javadoc():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('javadoc: ' + str(i))
        pool.apply_async(code_javadoc, (i,))
    pool.close()
    pool.join()


def multi_modifier():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('modifier: ' + str(i))
        pool.apply_async(code_modifier, (i,))
    pool.close()
    pool.join()


def multi_method():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('method: ' + str(i))
        pool.apply_async(code_method, (i,))
    pool.close()
    pool.join()


def multi_parameter():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('parameter: ' + str(i))
        pool.apply_async(code_parameter, (i,))
    pool.close()
    pool.join()


def multi_return():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('return: ' + str(i))
        pool.apply_async(code_return, (i,))
    pool.close()
    pool.join()


def multi_parsed():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('parsed: ' + str(i))
        pool.apply_async(code_parsed, (i,))
    pool.close()
    pool.join()


def multi_source():
    pool = multiprocessing.Pool(processes=n_threads)
    for i in range(total_files):
        print('source: ' + str(i))
        pool.apply_async(code_source, (i,))
    pool.close()
    pool.join()


def jdk(path_from, path_to):
    with open(path_from, 'r', encoding='utf-8') as infile:
        jdk = infile.readlines()
        vocab = {}
        for line in jdk:
            line = str(line).split(',')
            vocab[line[0].lower()] = str(cm.filter_digit_english(line[1])).lower().replace(' ', '')
        cm.save_pkl(path_to, vocab)


def query_parse(path_from, path_parsed_vocab, path_method_vocab, path_to):
    queries = cm.load_txt(path_from)
    vjdk = dict(cm.load_pkl(path_parsed_vocab))
    vword = dict(cm.load_pkl(path_method_vocab))
    stemmer = PorterStemmer()
    str_replace = ['in java', 'using java', 'java', 'how to', 'how do', 'what is']

    data_queries = list()
    p = 0
    for i in range(len(queries)):
        print(str(i))
        query = queries[i]
        for str_re in str_replace:
            query = query.replace(str_re, '')
        data = []
        tokens = cm.get_tokens(query)
        p += len(tokens)
        tokens = nltk.pos_tag(tokens)

        for token in tokens:
            tvalue = token[0]
            ttype = token[1]
            if ttype in type_all:
                para = 0
                impact = 0
                stem = stemmer.stem(tvalue)
                if stem in vword:
                    para = 1
                    impact = vword[stem]
                else:
                    freq = []
                    syns = cm.get_synonyms(stem)
                    for syn in syns:
                        score = 0
                        stem = cm.get_stemmed(syn)
                        if stem in vword:
                            score = vword[stem]
                            freq.append(score)
                    idx_max_freq = -1
                    if len(freq) > 0:
                        idx_max_freq = freq.index(max(freq))
                    if idx_max_freq > -1:
                        tvalue = syns[idx_max_freq]
                        para = 1
                        impact = vword[tvalue]
                if ttype in type_nn and stem in vjdk:
                    para = 2
                    impact = vjdk[stem]
                tvalue = cm.get_stemmed(tvalue)

                vector = [tvalue, ttype, para, impact]
                data.append(vector)
        data_queries.append(data)
    cm.save_pkl(path_to, data_queries)


def query_parse_tree(path_from, path_to):
    lines = cm.load_pkl(path_from)

    # sorting words
    for i in range(len(lines)):
        items = lines[i]

        mid_list1 = list()
        mid_list2 = list()
        word_list1 = list()
        word_list2 = list()
        other_list1 = list()
        other_list2 = list()
        for j in range(len(items)):
            item = items[j]
            if item[1] in type_cc + type_to + type_in:
                if item[2] is 1:
                    mid_list1.append([j, items[j][3]])
                else:
                    mid_list2.append([j, items[j][3]])
            elif item[1] in type_vb + type_nn:
                if item[2] is 1:
                    word_list1.append([j, items[j][3]])
                else:
                    word_list2.append([j, items[j][3]])
            else:
                if item[2] is 1:
                    other_list1.append([j, items[j][3]])
                else:
                    other_list2.append([j, items[j][3]])

        mid_list1.sort(key=operator.itemgetter(1))
        mid_list2.sort(key=operator.itemgetter(1))
        word_list1.sort(key=operator.itemgetter(1))
        word_list2.sort(key=operator.itemgetter(1))
        other_list1.sort(key=operator.itemgetter(1))
        other_list2.sort(key=operator.itemgetter(1))

        sort_list = mid_list1 + mid_list2 + other_list1 + other_list2 + word_list1 + word_list2
        for j in range(len(sort_list)):
            sort_list[j] = sort_list[j][0]

        query_list = list()
        for item in items:
            query_list.append(item[0])

        lines[i] = [query_list, sort_list]
    cm.save_pkl(path_to, lines)


def get_sort_list(items, m_list, sort_list):
    m_list.sort(key=operator.itemgetter(1))
    for m in m_list:
        idx = m[0]
        if len(items[idx]) > 1:
            for j in range(len(items[idx]) - 1):
                sort_list.append(items[idx][j][4])
    for m in m_list:
        idx = m[0]
        sort_list.append(items[idx][-1][4])


if __name__ == '__main__':
    path_data = './github_data/'  # '../codematcher_data/'

    now = time.time()

    # parse code components
    # multi_comment()
    # multi_javadoc()
    # multi_modifier()
    # multi_method()
    # multi_parameter()
    # multi_return()
    # multi_parsed()
    # multi_source()

    # parse JDK APIs
    # jdk(path_from=path_data + 'jdk.txt',
    #     path_to=path_data + 'jdk_vocab.pkl')

    # parse queries
    # convert each word in each query into pattern like [name, type,  grade, impact]
    query_parse(path_from=path_data + 'queries.txt',  # queries_comple.txt
                path_parsed_vocab=path_data + 'codebase_analysis/parsed_vocab_jdk_item.pkl',
                path_method_vocab=path_data + 'codebase_analysis/method_vocab_stemed.pkl',
                path_to=path_data + 'queries_parse.pkl')

    # pair each words in a query an important grade as [word1, word2, ..., wordN] -> [grade1, grade2, ..., gradeN]
    query_parse_tree(path_from=path_data + 'queries_parse.pkl',
                     path_to=path_data + 'queries_parse_sort.pkl')

    later = time.time()
    diff = later - now
    print(diff)
