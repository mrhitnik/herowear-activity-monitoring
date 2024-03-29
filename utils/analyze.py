import numpy as np


def analyze(data):
    data_mean = np.mean(data)
    data_var = np.var(data)
    #print(data_mean, " ", data_var)

    load = 'Low'
    if data_mean > 1:
        load = 'Medium'
    if data_mean > 1.5:
        load = 'Heavy'

    variation = 'Consistent'
    if data_var > 1:
        variation = 'Varying'

    return load, variation

def load_analysis(al, l, v):

    if l == 'low':
        al += -10
    elif l == 'Medium':
        al += 5
    elif l == 'Heavy':
        al += 15

    if v == 'Consistent':
        al += -5
    else:
        al += 10

    return np.max([al,0])

