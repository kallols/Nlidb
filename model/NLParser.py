import os
from nltk.tag.stanford import StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser

class NLParser:

    java_path = "C:\\Program Files\\Java\\jdk1.8.0_102\\bin\\java.exe"
    os.environ['JAVAHOME'] = java_path
    os.environ['STANFORD_MODELS'] = '/home/ashwin/Desktop/Nlidb/lib/stanford/stanfordstanford-postagger-full-2016-10-31/models/english-caseless-left3words-distsim.tagger:' \
                                    '/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar:' \
                                    '/home/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models/edu/stanford/nlp/models/parser/nndep/english_UD.gz'
    os.environ['CLASSPATH'] = '/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-parser-full-2016-10-31/stanford-parser.jar:' \
                              '/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-postagger-full-2016-10-31/stanford-postagger.jar:' \
                              '/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models.jar:' \
                              '/home/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-parser-full-2016-10-31/stanford-parser-3.7.0-models/edu/stanford/nlp/models/parser/nndep/english_UD.gz'

    path_to_model_tagger = "/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-postagger-full-2016-10-31/models/english-caseless-left3words-distsim.tagger"
    path_to_jar_tagger = "/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-postagger-full-2016-10-31/stanford-postagger.jar"
    tagger = StanfordPOSTagger(path_to_model_tagger, path_to_jar_tagger)
    tagger.java_options = '-mx4096m'  ### Setting higher memory limit for long sentences
    sentence = 'This is testing'

    parser = StanfordDependencyParser(path_to_jar='/home/ashwin/Desktop/Nlidb/lib/stanford/stanford-parser-full-2016-10-31/stanford-parser.jar')
    def __init__(self):
       # print self.tagger.tag(self.sentence.split())

       print [parse.tree() for parse in self.parser.raw_parse("The quick brown fox jumps over the lazy dog.")]


a = NLParser()

