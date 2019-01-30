import sys

def stat(log, data, threshold):
    TP, TN, FP, FN = 0, 0, 0, 0
    with open(log, 'r') as fl, open(data, 'r') as fd:
        log_lines = fl.readlines()
        data_lines = fd.readlines()

        data_dict = {}
        for data_line in data_lines:
            query = data_line.split(',')[0]
            target = data_line.split(',')[1]
            label = int(data_line.split(',')[2])
            data_dict[query + ',' + target] = label

        for log_line in log_lines:
            q = log_line.split(',')[0]
            t = log_line.split(',')[1]
            similarity = float(log_line.split(',')[2])
            if similarity >= threshold:
                guess = 1 # clone
            else:
                guess = 0 # not clone
            truth = data_dict[q + ',' + t]
            if truth == 1:
                if guess == 1:
                    TP += 1
                else:
                    FN += 1
            else:
                if guess == 1:
                    FP += 1
                else:
                    TN += 1

        prec = (float)(TP + TN) / (TP + TN + FP + FN)
        print TP
        print TN
        print FP
        print FN
        print "Precision: " + str(prec)


if __name__ == '__main__':
    stat(sys.argv[1], sys.argv[2], float(sys.argv[3]))


