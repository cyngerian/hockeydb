import pandas as pd
import os

def dataframeToCsv(dict, file, header_list, idx):
    df = pd.DataFrame(dict, index = [idx])
    if os.path.isfile(file):
        mode = 'a'
        header = 0
    else:
        mode = 'w'
        header = header_list
    df.to_csv(file, mode=mode, header=header)

if __name__ == '__main__':
    dataframeToCsv()