'''
Created on Apr 21, 2016

@author: dugue
'''
def maximum_contiguous_subsequence_sum(anomaly):
    max_ending_here = max_so_far = 0
    a = b = 0
    a_ending_here=0
    for idx, ano in enumerate(anomaly):
        max_ending_here = max(0, max_ending_here + ano)
        if max_ending_here ==0:
            a_ending_here=idx
        if max_ending_here > max_so_far:
            a=a_ending_here+1
            max_so_far = max_ending_here
            b = idx
    max_interval = (a, b)
    return max_interval

anomaly=[0, -1, 2,20,20,50, -3, -6, -8, -5, -2, 20,6, 10, 5, -5, -12, -2, 8, -10, -20,20,50,-200,10]
neg_anomaly=map(lambda x: -x, anomaly)
print anomaly
print neg_anomaly
print maximum_contiguous_subsequence_sum(anomaly)
print maximum_contiguous_subsequence_sum(neg_anomaly)