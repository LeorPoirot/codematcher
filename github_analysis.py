import codematcher as cm
import os
import nltk
import collections

type_cd = ['CD']
type_cc = ['CC']
type_in = ['IN']
type_to = ['TO']
type_jj = ['JJ', 'JJR', 'JJS']
type_nn = ['NN', 'NNS', 'NNP', 'NNPS']
type_rb = ['RB', 'RBR', 'RBS']
type_vb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']


def update_vocab_by_tokens(vocab, tokens):
    for token in tokens: # deaultdict may simplify the code
        if token in vocab.keys():
            vocab[token] += 1
        else:
            vocab[token] = 1


def update_vocab_by_token(vocab, token):
    if token in vocab.keys():
        vocab[token] += 1
    else:
        vocab[token] = 1


def stat_method(file_from, folder_to, total_num=-1):
    base = folder_to
    vword = dict()
    vsent = dict()
    vtype_cc = dict()
    vtype_cd = dict()
    vtype_in = dict()
    vtype_to = dict()
    vtype_jj = dict()
    vtype_nn = dict()
    vtype_rb = dict()
    vtype_vb = dict()
    vtype_ot = dict()
    methods = cm.load_pkl(file_from)
    total = len(methods) if total_num == -1 else total_num
    for i in range(0, total):
        print(str(i) + '-' + str(total))
        tokens = methods[i]
        update_vocab_by_tokens(vword, tokens)
        tokens_type = nltk.pos_tag(tokens)
        sent = []

        for ttype in tokens_type:
            if ttype[1] in type_cc:
                update_vocab_by_token(vtype_cc, ttype[0])
                sent.append('cc')
            elif ttype[1] in type_cd:
                update_vocab_by_token(vtype_cd, ttype[0])
                sent.append('cd')
            elif ttype[1] in type_jj:
                update_vocab_by_token(vtype_jj, ttype[0])
                sent.append('jj')
            elif ttype[1] in type_nn:
                update_vocab_by_token(vtype_nn, ttype[0])
                sent.append('nn')
            elif ttype[1] in type_rb:
                update_vocab_by_token(vtype_rb, ttype[0])
                sent.append('rb')
            elif ttype[1] in type_vb:
                update_vocab_by_token(vtype_vb, ttype[0])
                sent.append('vb')
            elif ttype[1] in type_in:
                update_vocab_by_token(vtype_in, ttype[0])
                sent.append('in')
            elif ttype[1] in type_to:
                update_vocab_by_token(vtype_to, ttype[0])
                sent.append('to')
            else:
                update_vocab_by_token(vtype_ot, str(ttype[0]) + '-' + str(ttype[1]))
                sent.append(ttype[1])

        lsent = '-'.join(sent)
        update_vocab_by_token(vsent, lsent)

        print(str(i) + '-' + str(total) + ': '
              + str(len(vword.keys())) + '-'
              + str(len(vsent.keys())) + ' '
              + str(len(vtype_cd.keys())) + '-'
              + str(len(vtype_in.keys())) + '-'
              + str(len(vtype_to.keys())) + '-'
              + str(len(vtype_jj.keys())) + '-'
              + str(len(vtype_nn.keys())) + '-'
              + str(len(vtype_rb.keys())) + '-'
              + str(len(vtype_vb.keys())) + '-'
              + str(len(vtype_ot.keys())) + '-')
    cm.save_pkl(base + 'method_vword.pkl', vword)
    cm.save_pkl(base + 'method_vsent.pkl', vsent)
    cm.save_pkl(base + 'method_vtype_cd.pkl', vtype_cd)
    cm.save_pkl(base + 'method_vtype_in.pkl', vtype_in)
    cm.save_pkl(base + 'method_vtype_to.pkl', vtype_to)
    cm.save_pkl(base + 'method_vtype_jj.pkl', vtype_jj)
    cm.save_pkl(base + 'method_vtype_nn.pkl', vtype_nn)
    cm.save_pkl(base + 'method_vtype_rb.pkl', vtype_rb)
    cm.save_pkl(base + 'method_vtype_vb.pkl', vtype_vb)
    cm.save_pkl(base + 'method_vtype_ot.pkl', vtype_ot)


def stat_parsed(path_jdk, file_from, folder_to, total_num=-1):
    base = folder_to
    all_api = 0
    all_jdk = 0
    relate = 0
    vocab_api = collections.defaultdict(int)
    vocab_jdk = collections.defaultdict(int)

    jdk = dict(cm.load_pkl(path_jdk))
    methods = cm.load_pkl(file_from + 'methname.pkl')
    lines = cm.load_pkl(file_from + 'apiseq.pkl')

    assert len(lines) == len(methods)
    total = len(methods) if total_num == -1 else total_num

    for i in range(0, total):
        method_tokens = methods[i]
        apiseq = lines[i].lower()

        if apiseq is not '[]':
            for token in method_tokens:
                if apiseq.find(token) >= 0:
                    relate += 1
                    break

            flag_api = 0
            flag_jdk = 0
            apis = apiseq.split(';')
            if len(apis) > 0:
                for api in apis:
                    if '.' in api:
                        flag_api = 1
                        if api.endswith(')'):
                            api = api[0:api.find('(')]
                        if api.endswith(']'):
                            api = api[0:api.find('[')]
                        if api.endswith('>'):
                            api = api[0:api.find('<')]

                        if api in jdk.keys():
                            flag_jdk = 1
                            vocab_jdk[api] += 1
                        else:
                            vocab_api[api] += 1
            all_api += flag_api
            all_jdk += flag_jdk

        print(str(i) + '-' + str(total) + ' '
                + '-' + str(all_api)  + '-' + str(relate) + ' '
                + str(len(vocab_api.keys())) + '-'
                + str(len(vocab_jdk.keys())))

    cm.save_pkl(base + 'parsed_vocab_api.pkl', vocab_api)
    cm.save_pkl(base + 'parsed_vocab_jdk.pkl', vocab_jdk)


def analyze_method(path_parsed_vocab, path_method):
    vdata = dict(cm.load_pkl(path_parsed_vocab))
    vdata = sorted(vdata.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    vwords = dict()
    for k, v in dict(vdata).items():
        key = cm.get_stemmed(k).lower()
        if key in vwords.keys():
            vwords[key] += v
        else:
            vwords[key] = v
    cm.save_pkl(path_method, vwords)


def analyze_parsed(path_parsed_vocab, path_parsed):
    vdata = dict(cm.load_pkl(path_parsed_vocab))
    vdata = sorted(vdata.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    vjdks = dict()
    for k, v in dict(vdata).items():
        key = cm.get_stemmed(k[str(k).rfind('.') + 1:].lower())
        if key not in vjdks.keys():
            vjdks[key] = v
    cm.save_pkl(path_parsed, vjdks)


if __name__ == '__main__':
    path_data = './github_data/'
    # 19726-6051 307-186-2-5276-15599-576-4206-311-
    # stat_method(file_from=path_data + 'codebase_parse/methname.pkl',
    #             folder_to=path_data + 'codebase_analysis/')


    # stat_parsed(path_jdk=path_data + 'jdk_vocab.pkl',
    #             file_from=path_data + 'codebase_parse/',
    #             folder_to=path_data + 'codebase_analysis/')



    # analyze_method(path_parsed_vocab=path_data + 'codebase_analysis/method_vword.pkl',
    #                path_method=path_data + 'codebase_analysis/method_vocab_stemed.pkl')

    # analyze_parsed(path_parsed_vocab=path_data + 'codebase_analysis/parsed_vocab_jdk.pkl',
    #                path_parsed=path_data + 'codebase_analysis/parsed_vocab_jdk_item.pkl')

    ################# parsed_vocab_jdk consists of pairs of jdk_api and frequency ###########
    print()

