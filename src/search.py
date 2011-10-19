import re
import math
import pickle
import sys

from stemmer import PorterStemmer
ps = PorterStemmer()

stopwords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(',')

def mul(v1, v2):
    score = 0
    for k in v1.keys():
        if v2.has_key(k):
            score += v1[k]*v2[k]
    return score 

def search(pickle_filename):
    
    ind = pickle.load(open(pickle_filename))
    
    while(True):
        print "query> "
        s = raw_input()
        
        wl_ = re.split( """[\s\.,/;:"'\?\{\}\[\]\\\|`~!@#\$%\^&\*\(\)_\+-=]""", s)
        q_vector = {}
        for w in wl_:        
            if not (w in stopwords or w == ''):
                w = w.lower()
                w = ps.stem(w, 0, len(w)-1)
                if ind['term_dict'].has_key(w):
                    if not q_vector.has_key(w):
                        q_vector[w] = 0
                    q_vector[w] += 1
#        print 'intermediate : ', q_vector
        
        for term in q_vector.keys():
            q_vector[term] = 1 + math.log(q_vector[term])
            idf = math.log( float(ind['doc_count']) / ind['term_dict'][term]['df'] )
            q_vector[term] *= idf
        
        print q_vector
        
        scores = []
        
        for doc_id in ind['docs'].keys():
            score = mul(q_vector ,ind['docs'][doc_id]['vector'])
            scores.append([doc_id, score])
        
        def key_foo(x):
            x[1]
                
        sorted(scores, key=key_foo)
        
        
        results = []
        
        MAX_RESULTS = 5        
        for i in range(MAX_RESULTS):
            sc = scores.pop()
            results.append( ind['docs'][sc[0]]['link'] )
        
        for r in results:
            print 'r> ', r
    
    
if __name__ == '__main__':
    
    try:
        index_file = sys.argv[1]
    except:
        print "usage : python search.py <index_file>"
        sys.exit()
        
    search(index_file)