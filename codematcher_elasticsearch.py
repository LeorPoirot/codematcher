from __future__ import print_function
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
import codematcher as cm
import hashlib
import time


class SearchEngine:
    def __init__(self, index_name):
        self.index_name = index_name # "search_engine"
        self.doc_type = "code"
        self.ip = "localhost:9200"
        self.es = Elasticsearch([self.ip])
        self.id = 0

    def create_index(self):
        body = {"mappings": {self.doc_type: {"properties": {
            "comment": {"type": "text"},
            "javadoc": {"type": "text"},
            "method": {"type": "text"},
            "modifier": {"type": "text"},
            "package": {"type": "text"},
            "parameter": {"type": "text"},
            "parsed": {"type": "text"},
            "return": {"type": "text"},
            "source": {"type": "text"}
        }}}}
        self.es.indices.create(index=self.index_name, body=body, ignore=400)

    def create_simple_index(self):
        body = {"mappings": {self.doc_type: {"properties": {
            "method": {"type": "text"},
            "parsed": {"type": "text"},
            "source": {"type": "text"}
        }}}}
        self.es.indices.create(index=self.index_name, body=body, ignore=400)

    def delete_index(self, index_name):
        self.es.indices.delete(index_name)

    def fill_data(self, path_formatted_repos):
        for i in range(10):
            print(str(i) + '-9')
            body = cm.load_pkl(path_formatted_repos + 'body' + str(i) + '.pkl')
            helpers.bulk(self.es, body, request_timeout=1000)

    def fill_simple_data(self, path):
        body = list()
        code = cm.load_txt(path + 'rawcode.txt')
        apiseq = cm.load_pkl(path + 'apiseq.pkl')
        meth = cm.load_pkl(path + 'raw_methname.pkl')
        assert len(code) == len(apiseq) and len(code) == len(meth)
        for j in range(len(code)):
            body.append({
                "_index": self.index_name,
                "_type": self.doc_type,
                "_source": {
                    "method": meth[j],
                    "parsed": apiseq[j],
                    "source": code[j]
                }
            })
        helpers.bulk(self.es, body, request_timeout=1000)

    def format_data(self, path_pased_repos, path_formatted_repos, total_files, repo_split_size):
        body = list()
        count = 0
        index = 0
        path = path_pased_repos
        for i in range(total_files):
            print(str(i))
            if os.path.exists(path + 'comment/comment' + str(i) + '.txt'):
                wcomment = cm.load_txt(path + 'comment/comment' + str(i) + '.txt')
                wjavadoc = cm.load_txt(path + 'javadoc/javadoc' + str(i) + '.txt')
                wmethod = cm.load_txt(path + 'method/method' + str(i) + '.txt')
                wmodifier = cm.load_txt(path + 'modifier/modifier' + str(i) + '.txt')
                wpackage = cm.load_txt(path + 'package/package' + str(i) + '.txt')
                wparameter = cm.load_txt(path + 'parameter/parameter' + str(i) + '.txt')
                wparsed = cm.load_txt(path + 'parsed/parsed' + str(i) + '.txt')
                wreturn = cm.load_txt(path + 'return/return' + str(i) + '.txt')
                wsource = cm.load_txt(path + 'source/source' + str(i) + '.txt')

                for j in range(len(wcomment)):
                    body.append({
                        "_index": self.index_name,
                        "_type": self.doc_type,
                        "_source": {
                            "comment": wcomment[j],
                            "javadoc": wjavadoc[j],
                            "method": wmethod[j],
                            "modifier": wmodifier[j],
                            "package": wpackage[j],
                            "parameter": wparameter[j],
                            "parsed": wparsed[j],
                            "return": wreturn[j],
                            "source": wsource[j]
                        }
                    })

                count += 1
                if count == repo_split_size:
                    cm.save_pkl(path_formatted_repos + 'body' + str(index) + '.pkl', body)
                    index += 1
                    count = 0
                    body = list()
        cm.save_pkl(path_formatted_repos + 'body' + str(index) + '.pkl', body)

    def search(self, keywords, apis):
        query = {
            "query": {"bool": {"should": [{"regexp": {"method": keywords}},
                                          {"regexp": {"parameter": keywords}},
                                          {"regexp": {"return": keywords}}],
                               "must": {"regexp": {"parsed": apis}},
                               "minimum_should_match": 2}}
        }

        scan_resp = helpers.scan(self.es, query, index=self.index_name, scroll="10m")
        respond = []
        for hit in scan_resp:
            respond.append(hit)
        print(len(respond))

        if len(respond) <= 100:
            query = {
                "query": {"bool": {"should": [{"regexp": {"method": keywords}},
                                              {"regexp": {"parameter": keywords}},
                                              {"regexp": {"return": keywords}}],
                                   "minimum_should_match": 3}}
            }

            scan_resp = helpers.scan(self.es, query, index=self.index_name, scroll="10m")
            respond = []
            for hit in scan_resp:
                respond.append(hit)
            print(len(respond))

        return respond

    def search_all(self):
        cmd = "getPlatformNewline"
        query = {"query": {"regexp": {"method": cmd.lower()}}}
        scanResp = helpers.scan(self.es, query, index=self.index_name, scroll="10m")
        respond = []
        for hit in scanResp:
            respond.append(hit)
        print(len(respond))
        print()

    def fuzzy_search(self, path_queries, path_jdk, respond_top_n, path_save):
        queries = cm.load_pkl(path_queries)
        jdk = cm.load_pkl(path_jdk)
        total = respond_top_n
        for i in range(len(queries)):
            query = queries[i]
            query_words = list(query[0])
            query_sorts = list(query[1])

            cmd = '.*' + '.*'.join(query_words) + '.*'
            data = []
            cmds = []
            source_hash = []
            respond, query_cmd = self.search_respond(cmd, source_hash, jdk)
            data.extend(respond)
            cmds.extend(query_cmd)
            idx = 0
            while len(data) < total and len(query_words) - idx > 0:
                temp = []
                if idx == 0:
                    s = [query_sorts[0]]
                else:
                    s = query_sorts[:idx]
                for j in range(len(query_words)):
                    if j not in s:
                        temp.append(query_words[j])
                cmd = '.*' + '.*'.join(temp) + '.*'  # add .* devant
                respond, query_cmd = self.search_respond(cmd, source_hash, jdk)
                data.extend(respond)
                cmds.extend(query_cmd)
                idx += 1
            cm.save_pkl(path_save + 'respond' + str(i) + '.pkl', data)
            cm.save_pkl(path_save + 'cmd' + str(i) + '.pkl', cmds)
            print(str(i) + '-' + str(len(queries)) + ' ' + str(len(data)))

    def search_respond(self, cmd, source_hash, jdk):
        query = {"query": {"regexp": {"method": cmd.lower()}}}
        scan_resp = helpers.scan(self.es, query, index=self.index_name, scroll="10m", request_timeout=1000)
        respond = []
        query_cmd = []
        for hit in scan_resp:
            source = str(hit['_source']['source'])
            hash_val = hashlib.md5(source.encode('utf-8')).digest()
            if hash_val not in source_hash:
                source_hash.append(hash_val)
                respond.append(hit)
                query_cmd.append(cmd)
        return respond, query_cmd


if __name__ == '__main__':
    path_data = './github_data/' # '../codematcher_data/'

    now = time.time()

    se = SearchEngine('deepcs_search_engine2')  # search_engine

    # process repos data based on index format
    # se.format_data(path_pased_repos=path_data + 'codebase_parse/',
    #                path_formatted_repos=path_data + 'codebase_elasticsearch/',
    #                total_files=41025,
    #                repo_split_size=4000)

    # create ElasticSearch index
    # se.create_simple_index()

    # fill formatted data into indexed ElasticSearch
    # se.fill_simple_data(path=path_data + 'codebase_parse/')
    # se.fill_data(path_formatted_repos=path_data + 'codebase_elasticsearch/')
    print('locked and loaded!!!')
    # do the fuzzy search on indexed data with queries
    # store results
    se.fuzzy_search(path_queries=path_data + 'queries_parse_sort.pkl',
                    path_jdk=path_data + 'jdk_vocab.pkl',
                    respond_top_n=10,
                    path_save=path_data + 'codebase_search/')

    later = time.time()
    diff = later - now
    print(diff)
