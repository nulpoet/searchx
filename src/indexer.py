import re
import pickle
import os
import sys
import math

from stemmer import PorterStemmer
ps = PorterStemmer()

def index(pickle_filename):
    term_dict = {}
    
    filelist = os.listdir('data')
    
    stopwords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(',')
    #TODO: load stopword list
    
    docs = {}
    doc_count = 0
    
    for file in filelist:
        print 'processing ', file
        doc_count += 1
        doc_id = doc_count
        docs[doc_id] = ({'link':file,
                      'vector':{}
                      }) 
        
        
        f = open(os.path.join('data',file))
        
        s = f.read()
        
        wl_ = re.split( """[\s\.,/;:"'\?\{\}\[\]\\\|`~!@#\$%\^&\*\(\)_\+-=]""", s)
        wl = []
        for w in wl_:        
            if not (w in stopwords or w == ''):
                w = w.lower()
                w = ps.stem(w, 0, len(w)-1)
                wl.append(w)
        
        for w in wl:
            
            if not docs[doc_id]['vector'].has_key(w):
                docs[doc_id]['vector'][w] = 0
            docs[doc_id]['vector'][w] += 1
            
            if not term_dict.has_key(w):
                term_dict[w] = { 'df':0, 'tfs':{} }
            
            if not term_dict[w]['tfs'].has_key(doc_id):
                 term_dict[w]['tfs'][doc_id] = 0
            term_dict[w]['tfs'][doc_id] += 1
    
        for k in docs[doc_id]['vector'].keys():
            docs[doc_id]['vector'][k] = 1 + math.log( docs[doc_id]['vector'][k] ) 
    
        norm = 0
        for v in docs[doc_id]['vector'].values():
            norm += v*v
        norm = norm**0.5
        for k in docs[doc_id]['vector'].keys():
            docs[doc_id]['vector'][k] /= norm
            
    
    for w in term_dict.keys():
        term_dict[w]['df'] = len(term_dict[w]['tfs'].keys())
    
    pickle.dump({'doc_count':doc_count, 
                 'term_dict':term_dict,
                 'docs':docs}, 
                open(pickle_filename, 'w'))


if __name__ == '__main__':
    
    try:
        index_file = sys.argv[1]
    except:
        print "usage : python indexer.py <index_file>"
        sys.exit()
        
    index(index_file)
    