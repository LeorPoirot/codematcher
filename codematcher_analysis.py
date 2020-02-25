import codematcher as cm
import os
import nltk

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


def stat_method(folder_from, folder_to, total_files):
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
    for i in range(0, total_files):
        print(str(i) + '-' + str(total_files))
        path = folder_from + 'method' + str(i) + '.txt'
        if os.path.exists(path):
            lines = cm.load_txt(path)
            for line in lines:
                tokens = cm.camel_split_for_tokens(line)
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

            print(str(i) + '-' + str(total_files) + ': '
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


def stat_parsed(path_jdk, folder_from_method, folder_to_parsed, folder_to, total_files):
    base = folder_to
    vocab_api = dict()
    vocab_jdk = dict()
    all = 0
    all_api = 0
    all_jdk = 0
    relate = 0
    jdk = dict(cm.load_pkl(path_jdk))
    for i in range(0, total_files):
        path = folder_from_method + 'method' + str(i) + '.txt'
        if os.path.exists(path):
            methods = cm.load_txt(folder_from_method + 'method' + str(i) + '.txt')
            lines = cm.load_txt(folder_to_parsed + 'parsed' + str(i) + '.txt')
            for j in range(len(methods)):
                all += 1

                line = lines[j].replace('\n', '')
                if line is not '[]':
                    tokens = cm.get_tokens(cm.camel_split(methods[j]))
                    for token in tokens:
                        if line.find(token) >= 0:
                            relate += 1
                            break

                    flag_api = 0
                    flag_jdk = 0
                    apis = line.split(',')
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
                                    if api in vocab_jdk.keys():
                                        vocab_jdk[api] += 1
                                    else:
                                        vocab_jdk[api] = 1
                                else:
                                    if api in vocab_api.keys():
                                        vocab_api[api] += 1
                                    else:
                                        vocab_api[api] = 1
                    all_api += flag_api
                    all_jdk += flag_jdk

                print(str(i) + '-41025 ' + str(j) + '-' + str(len(methods)) + ' '
                      + str(all) + '-' + str(all_api) + '-' + str(all_jdk) + '-' + str(relate) + ' '
                      + str(len(vocab_api.keys())) + '-'
                      + str(len(vocab_jdk.keys())))

    cm.save_pkl(base + 'parsed_vocab_api.pkl', vocab_api)
    cm.save_pkl(base + 'parsed_vocab_jdk.pkl', vocab_jdk)


def stat_parameter_return(path_jdk, folder_method, folder_parameter, folder_return, folder_to, total_files):
    base = folder_to
    vocab_api = dict()
    vocab_jdk = dict()
    vocab_name = dict()
    all = 0
    con = 0
    jdk = dict(cm.load_pkl(path_jdk))
    for i in range(0, total_files):
        path = folder_method + 'method' + str(i) + '.txt'
        if os.path.exists(path):
            lines_method = cm.load_txt(folder_method + 'method' + str(i) + '.txt')
            lines_parameter = cm.load_txt(folder_parameter + 'parameter' + str(i) + '.txt')
            lines_return = cm.load_txt(folder_return + 'return' + str(i) + '.txt')
            for j in range(len(lines_method)):
                print(str(i) + '-' + str(
                    total_files) + ' -' + str(j) + ' ' + str(len(lines_method)) + ' ' + str(con) + ' - ' + str(
                    all) + ' '
                      + str(len(vocab_api.keys())) + '-'
                      + str(len(vocab_jdk.keys())) + '-'
                      + str(len(vocab_name.keys())))
                all += 1
                line_method = lines_method[j]
                tokens = cm.get_tokens(cm.camel_split(line_method))

                line_paras = lines_parameter[j].replace('\n', '')
                para_types = []
                para_names = []

                line_return = lines_return[j]
                line_return = line_return.replace('\n', '')
                para_types.append(line_return)

                line = line_paras + ' ' + line_return
                for token in tokens:
                    if line.find(token) >= 0:
                        con += 1
                        break

                if '[]' not in line_paras:
                    if ';' in line_paras:
                        line_paras = line_paras.split(';')
                        for line_para in line_paras:
                            paras = line_para.split(',')
                            if len(paras) == 2:
                                para_types.append(paras[0])
                                para_names.append(paras[1])
                    else:
                        paras = line_paras.split(',')
                        if len(paras) == 2:
                            para_types.append(paras[0])
                            para_names.append(paras[1])

                for type in para_types:
                    if type in jdk.keys():
                        if type in vocab_jdk.keys():
                            vocab_jdk[type] += 1
                        else:
                            vocab_jdk[type] = 1
                    else:
                        if type in vocab_api.keys():
                            vocab_api[type] += 1
                        else:
                            vocab_api[type] = 1

                for name in para_names:
                    if name in vocab_name.keys():
                        vocab_name[name] += 1
                    else:
                        vocab_name[name] = 1

    cm.save_pkl(base + 'para_vocab_api.pkl', vocab_api)
    cm.save_pkl(base + 'para_vocab_jdk.pkl', vocab_jdk)
    cm.save_pkl(base + 'para_vocab_name.pkl', vocab_name)


def stat_comment(folder_method, folder_comment, folder_javadoc, total_files):
    all = 0
    cmt = 0
    jdc = 0
    cmt_and_jdc = 0
    cmt_or_jdc = 0
    cmt_relate = 0
    jdc_relate = 0
    for i in range(0, total_files):
        path = folder_method + 'method' + str(i) + '.txt'
        if os.path.exists(path):
            comments = cm.load_txt(folder_comment + 'comment' + str(i) + '.txt')
            javadocs = cm.load_txt(folder_javadoc + 'javadoc' + str(i) + '.txt')
            methods = cm.load_txt(folder_method + 'method' + str(i) + '.txt')
            for j in range(len(methods)):
                all += 1
                comment = comments[j].replace('\n', '')
                javadoc = javadocs[j].replace('\n', '')
                if '[]' != comment:
                    cmt += 1
                if '[]' != javadoc:
                    jdc += 1
                if '[]' != comment and '[]' != javadoc:
                    cmt_and_jdc += 1
                if '[]' != comment or '[]' != javadoc:
                    cmt_or_jdc += 1

                cmt_r = 0
                jdc_r = 0
                tokens = cm.get_tokens(cm.camel_split(methods[j]))
                for token in tokens:
                    if comment.find(token) >= 0:
                        cmt_r = 1
                        break
                for token in tokens:
                    if javadoc.find(token) >= 0:
                        jdc_r = 1
                        break
                if cmt_r == 1:
                    cmt_relate += 1
                if jdc_r == 1:
                    jdc_relate += 1
                print(str(i) + '-' + str(total_files) + ' ' + str(j) + '-' + str(len(methods)) + ' ' +
                      str(all) + '-' + str(cmt) + '-' + str(jdc) + ' ' +
                      str(cmt_and_jdc) + '-' + str(cmt_or_jdc) + ' ' +
                      str(cmt_relate) + '-' + str(jdc_relate))
                # 41024-41025 53181-53182 16611025-1976819-3639794 528600-5088013 701489-2421430


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
    path_data = '../codematcher_data/'

    # stat_method(folder_from=path_data + 'codebase_parse/method/',
    #             folder_to=path_data + 'codebase_analysis/',
    #             total_files=41025)

    stat_parsed(path_jdk=path_data + 'jdk_vocab.pkl',
                folder_from_method=path_data + 'codebase_parse/method/',
                folder_to_parsed=path_data + 'codebase_parse/parsed/',
                folder_to=path_data + 'codebase_analysis/',
                total_files=41025)

    stat_parameter_return(path_jdk=path_data + 'dk_vocab.pkl',
                          folder_method=path_data + 'codebase_parse/method/',
                          folder_parameter=path_data + 'codebase_parse/parameter/',
                          folder_return=path_data + 'codebase_parse/return/',
                          folder_to=path_data + 'codebase_analysis/',
                          total_files=41025)

    stat_comment(folder_method=path_data + 'codebase_parse/method/',
                 folder_comment=path_data + 'codebase_parse/comment/',
                 folder_javadoc=path_data + 'codebase_parse/javadoc/',
                 total_files=41025)

    analyze_method(path_parsed_vocab=path_data + 'codebase_analysis/parsed_vocab_jdk.pkl',
                   path_method=path_data + 'codebase_analysis/method_vtype_vb_stemed.pkl')

    analyze_parsed(path_parsed_vocab=path_data + 'codebase_analysis/parsed_vocab_jdk.pkl',
                   path_parsed=path_data + 'codebase_analysis/parsed_vocab_jdk_item.pkl')
