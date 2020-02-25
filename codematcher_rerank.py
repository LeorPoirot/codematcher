import codematcher as cm
import re
import operator
import time


def api_check(parsed):
    parsed = parsed.split(',')
    n_prop = 0
    n_all = 0
    for api in parsed:
        if '.' in api:
            n_all += 1
            api = api[:api.find('.')].strip()
            if api in ['com', 'org', 'sun', 'jdk', 'java', 'javax']:
                n_prop += 1

    if n_all > 0:
        n_prop = n_prop / n_all
    return n_prop


def matcher_name(words, line, cmd):
    cmd = str(cmd).replace('.*', ' ').strip().split(' ')
    line = str(line).replace('\n', '')

    word_usage = len(cmd) / len(words)
    line_coverage = len(''.join(cmd)) / len(line)
    score = word_usage * line_coverage
    return score


def matcher_api(query, line, jdk):
    line = str(line).replace('\n', '').lower()
    index = []
    freq = 0
    count = 0
    for word in query:
        pattern = re.compile(word.lower())
        wi = [i.start() for i in pattern.finditer(line)]
        if len(wi) > 0:
            freq += len(wi) * len(word)
            count += 1
            index.append(wi)
    word_usage = count / len(query)
    line_coverage = freq / len(line)
    max_sequence = len(sequence(index)) / len(query)

    apis = line.split(';') # split can be , or ;
    api_count = 0
    jdk_count = 0
    for api in apis:
        if '.' in api:
            api_count += 1
            if '(' in api or '[' in api or '<' in api:
                api = api[:api.rfind('.')]
            if api in jdk:
                jdk_count += 1
    jdk_percent = 0
    if api_count > 0:
        jdk_percent = jdk_count / api_count

    score = word_usage * line_coverage * max_sequence * jdk_percent
    return score


def matcher_string(query, line):
    line = str(line).replace('\n', '').lower()
    index = []
    freq = 0
    count = 0
    for word in query:
        pattern = re.compile(word.lower())
        wi = [i.start() for i in pattern.finditer(line)]
        if len(wi) > 0:
            freq += len(wi) * len(word)
            count += 1
            index.append(wi)
    word_usage = count / len(query)
    line_coverage = freq / len(line)
    max_sequence = len(sequence(index)) / len(query)

    score = word_usage * line_coverage * max_sequence
    return score


def matcher(query, line):
    keywords = query[0]
    apis = query[1]

    line = line.lower()
    p_api = round(api_check(line), 2)
    [pw_keyword, pl_keyword] = match(keywords, line)
    [pw_api, pl_api] = match(apis, line)

    s_keyword = round(pw_keyword * pl_keyword, 2)
    s_api = round(pw_api * pl_api, 2)
    score = [s_keyword, s_api, p_api]

    return score


def match(words, line):
    word_prop = 0
    line_prop = 0

    n_word = len(cm.get_tokens(line))
    if len(words) > 0 and n_word > 0:
        word_idx = list()

        for word in words:
            pattern = re.compile(word.lower())
            wi = [i.start() for i in pattern.finditer(line)]
            if len(wi) > 0:
                word_idx.append(wi)
                line_prop += len(wi)

        if line_prop > 0:
            seq = sequence(word_idx)
            word_prop = len(seq) / len(words)
            line_prop = line_prop / n_word

    return [word_prop, line_prop]


def sequence(seq):
    orders = []
    scores = []
    for i in range(len(seq)):
        scores.append(0)
        for si in seq[i]:
            orders.append([si])
        for k in range(len(orders)):
            sik = orders[k][-1]

            for j in range(i + 1, len(seq)):
                for l in range(len(seq[j])):
                    sjl = seq[j][l]

                    if sik < sjl:
                        temp = []
                        temp.extend(orders[k])
                        temp.append(sjl)
                        orders.append(temp)
    for o in orders:
        scores[len(o) - 1] += 1
    return scores


def reranking(path_parsed_queries, path_queries, path_jdk, path_fuzzy_search, path_rerank):
    queries = cm.load_pkl(path_parsed_queries)
    jdk = cm.load_pkl(path_jdk)
    for i in range(len(queries)):
        query = queries[i]
        words = []
        for word in query:
            words.append(word[0])
        queries[i] = words

    queries_txt = cm.load_txt(path_queries)
    lines = []

    for i in range(99): # 50
        respond = cm.load_pkl(path_fuzzy_search + 'respond' + str(i) + '.pkl')
        query_cmd = cm.load_pkl(path_fuzzy_search + 'cmd' + str(i) + '.pkl')
        query = queries[i]
        query_txt = queries_txt[i]

        scores = list()
        for j in range(len(respond)):
            print(str(i) + '-50, iter-1, ' + str(j) + '-' + str(len(respond)))
            res = respond[j]['_source']
            line = res['method']
            cmd = query_cmd[j]
            scores.append([j, matcher_name(query, line, cmd)])
        scores.sort(key=operator.itemgetter(1), reverse=True)

        scores = scores[:100]

        for j in range(len(scores)):
            print(str(i + 1) + '-99, iter-2, ' + str(j) + '-' + str(len(scores)))
            idx = scores[j][0]
            res = respond[idx]['_source']
            line = res['parsed']
            scores[j].append(matcher_api(query, line, jdk))
        scores.sort(key=operator.itemgetter(1, 2), reverse=True)

        if '\n' not in query_txt:
            query_txt += '\n'
        lines.append(query_txt)
        results = min(len(scores), 10)
        if len(scores) > 0:
            for j in range(results):
                idx = scores[j][0]
                lines.append(respond[idx]['_source']['source'])
        lines.append('\n')

    cm.save_txt(path_rerank, lines)


if __name__ == '__main__':
    path_data = './github_data/'  # '../codematcher_data/'

    now = time.time()

    reranking(path_parsed_queries=path_data + 'queries_parse.pkl', # queries_comple_parse.pkl
              path_queries=path_data + 'queries.txt', # raw queries list
              path_jdk=path_data + 'jdk_vocab.pkl',
              path_fuzzy_search=path_data + 'codebase_search/', # search_comple
              path_rerank=path_data + 'search.txt') # search_comple

    later = time.time()
    diff = later - now
    print(diff)
