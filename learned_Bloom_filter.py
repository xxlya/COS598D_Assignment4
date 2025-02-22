import numpy as np
import pandas as pd
import argparse
from Bloom_filter import BloomFilter


parser = argparse.ArgumentParser()
parser.add_argument('--data_path', action="store", dest="data_path", type=str, required=True,
                    help="path of the dataset")
parser.add_argument('--threshold_min', action="store", dest="min_thres", type=float, required=True,
                    help="Minimum threshold for positive samples")
parser.add_argument('--threshold_max', action="store", dest="max_thres", type=float, required=True,
                    help="Maximum threshold for positive samples")
parser.add_argument('--size_of_LBF', action="store", dest="R_sum", type=int, required=True,
                    help="size of the LBF")




results = parser.parse_args()
DATA_PATH = results.data_path
min_thres = results.min_thres
max_thres = results.max_thres
R_sum = results.R_sum


'''
Load the data and select training data
'''
data = pd.read_csv(DATA_PATH)
negative_sample = data.loc[(data['label']==-1)]
positive_sample = data.loc[(data['label']==1)]
train_negative = negative_sample.sample(frac = 0.3)


def Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample):
    FP_opt = train_negative.shape[0]

    for threshold in np.arange(min_thres, max_thres+10**(-6), 0.01):
        query = positive_sample.loc[(positive_sample['score'] <= threshold),'query']
        n = len(query)
        bloom_filter = BloomFilter(n, R_sum)
        bloom_filter.insert(query)
        
        '''
        Please finish the code to find bloom_filter_opt, thres_opt
        '''

            
        '''
        Ends here
        '''
    return bloom_filter_opt, thres_opt




'''
Implement learned Bloom filter
'''
if __name__ == '__main__':
    '''Stage 1: Find the hyper-parameters (spare 30% samples to find the parameters)'''
    bloom_filter_opt, thres_opt = Find_Optimal_Parameters(max_thres, min_thres, R_sum, train_negative, positive_sample)

    '''Stage 2: Run LBF on all the samples''
    ### Test queries
    ML_positive = negative_sample.loc[(negative_sample['score'] > thres_opt), 'query']
    bloom_negative = negative_sample.loc[(negative_sample['score'] <= thres_opt), 'query']
    score_negative = negative_sample.loc[(negative_sample['score'] < thres_opt), 'score']
    BF_positive = bloom_filter_opt.test(bloom_negative, single_key = False)
    FP_items = sum(BF_positive) + len(ML_positive)
    FPR = FP_items/len(negative_sample)
    print('False positive items: {}; FPR: {}; Size of quries: {}'.format(FP_items, FPR, len(negative_sample)))
