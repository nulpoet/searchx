import re
import pickle
import os


def index(pickle_filename):
    d = {}
    
    filelist = os.listdir('data')
    
    stopwords = "a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your".split(',')
    #TODO: load stopword list
    
    docs = {}
    doc_count = 0
    
    for file in filelist:
        print 'processing ', file
        doc_count += 1
        doc_id = doc_count
        docs[file] = doc_id
        
        f = open(os.path.join('data',file))
        
        s = f.read()
        
        wl_ = re.split( """[\s\.,/;:"'\?\{\}\[\]\\\|`~!@#\$%\^&\*\(\)_\+-=]""", s)
        wl = []
        for w in wl_:        
            if w in stopwords or w == '':
                wl.append(w)
        
        for w in wl:
            if not d.has_key(w):
                d[w] = { 'df':0, 'tfs':{} }
            
            if not d[w]['tfs'].has_key(doc_id):
                 d[w]['tfs'][doc_id] = 0
            d[w]['tfs'][doc_id] += 1
    
    for w in d.keys():
        d[w]['df'] = len(d[w]['tfs'].keys())
    
    pickle.dump({'doc_count':doc_count, 
                 'd':d}, 
                open(pickle_filename, 'w'))
