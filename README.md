## 使用说明

#### 1. codematcher_analysis.py 用于解析原始数据集中方tokens的频率 github竞赛的数据集我仿照写了github_analysis 用这个就行了
- stat_method(), get statistics of method name in codebase.
- stat_parsed(), get statistics of method body in codebase.
- analyze_method(), get vocabulary of method name according to the output of stat_method().
- analyze_parsed(), get vocabulary of method body according to the output of stat_parsed().

#### 5. Preprocess queries and parsed methods by codematcher_parse.py
- query_parse(), preprocess queries and get metadata for each token in queries.
- query_parse_tree(), generate query keywords with importance order.

#### 6. Index codebase by codematcher_elasticsearch.py es 我已经附在工程目录里了，你只要解压然后把 根目录下的bin目录加入环境变量然后启动
- format_data(), save reprocessed method components to Json data structure.
- create_index(), create codebase index for elasticsearch. 为了简化直接用 create_simple_index()
- fill_data(), fill the formatted data to the elasticsearch. 简化直接用 fill_simple_data()
- fuzzy_search(), perform fuzzy search on the indexed code with parsed queries.

#### 7. Rerank search results by codematcher_rerank.py
- reranking(), reorder the search results returned by the fuzzy_search() and generate the final results in 'search.txt'
- '_search_codematcher_parsed_lzw.txt' in Baidu Pan [link](https://pan.baidu.com/s/105_15RPwgc5O8pqOi_meMw) shows the final result.





