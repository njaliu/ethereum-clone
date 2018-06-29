import sys
import os
import copy
import traceback
import eclone

evm_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime/result"
evm_opt_dir = "/home/aliu/Research/Projects/eclone-eval/evm-bytecode-clone/bin-runtime-optimize/result"

N_contracts = 100
THRESHOLD = 0.5

def fse_eval():
    count = 0
    correct = 0
    argv_bak = sys.argv
    for root, dirs, files in os.walk(evm_dir):
        path = root.split(os.sep)
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            sys.argv = argv_bak
            if count >= N_contracts:
                return
            print(len(path) * '---', file)
            #print(os.path.abspath(root + '/' + file))
            query = os.path.abspath(root + '/' + file)
            print(query)
            target = query.replace(evm_dir, evm_opt_dir)
            print(target)

            try:
                argv_qt = copy.copy(argv_bak)
                argv_qt.extend(['--clone', query, target])
                sys.argv = copy.copy(argv_qt)
                qt_json = eclone.main()

                argv_qq = copy.copy(argv_bak)
                argv_qq.extend(['--clone', query, query])
                sys.argv = copy.copy(argv_qq)
                qq_json = eclone.main()
            except Exception as e:
            	traceback.print_exc()
            	continue

            if qq_json["score"] == 0:
            	continue
            	
            if (qq_json["score"] - qt_json["score"]) / qq_json["score"] <= THRESHOLD:
                print("Clone Found: " + query + ", " + target)
                correct += 1
            else:
                print("Clone Not Found: " + query + ", " + target)

            #sys.argv.extend(['--clone', query, target])
            #print sys.argv
            
            #eclone_json = eclone.main()
            #print eclone_json
            #print("## EClone Clone Detection: " + str(eclone_json["score"]))
            #print("## Number of basic block in query: " + str(eclone_json["nquery"]))
            #print("## Number of basic block in target: " + str(eclone_json["ntarget"]))
            count += 1

    #eclone.main()
    print("EClone Accuracy: " + str( correct / float(count) ))


if __name__ == '__main__':
    fse_eval()