import sys
import math
import statistics
from decimal import Decimal

training_filename = sys.argv[1]
testing_filename = sys.argv[2]
mode = sys.argv[3]

with open(training_filename, 'r') as f:
    training_file = f.read().splitlines()
    
with open(testing_filename, 'r') as f:
    testing_file = f.read().splitlines()

num_of_train_samples = len(training_file)
num_of_attributes = len(training_file[0].split(','))-1
num_of_test_samples = len(testing_file)

training = []
testing = []
final_decision = []

for index,each in enumerate(training_file):
    temp = training_file[index].split(",")
    temp2 = []
    for index2 in range(len(temp)-1):
        temp2.append(float(temp[index2]))
    temp2.append(temp[index2+1])
    training.append(temp2)
        
for index,each in enumerate(testing_file):
    temp = testing_file[index].split(",")
    temp2 = []
    for index2 in range(len(temp)):
        temp2.append(float(temp[index2]))
    testing.append(temp2)

num_of_yes = 0
num_of_no = 0

for i in training:
    if i[num_of_attributes] == 'yes':
        num_of_yes+=1
    elif i[num_of_attributes] == 'no':
        num_of_no+=1
    
eucli = [None] * num_of_train_samples

def calc_eucli(line):   
    for i in range(num_of_train_samples):
        summed = 0
        for j in range(num_of_attributes): 
            summed += (line[j] - training[i][j])**2
            if j == num_of_attributes-1:
                eucli[i] = (math.sqrt(summed))                
    #print(eucli)
    

def find_nearest_neighbours(n,sample_index):
    min_list = []
    decision = 0
    eucli2 = []
    
    for each in eucli:
        eucli2.append(each)
    
    for i in range(n):
        smallest = min(eucli2)
        for index,each in enumerate(eucli):
            if each == smallest:
                min_list.append(index)
                eucli2.remove(smallest)
                break

    for i in min_list:
        if training[i][num_of_attributes] == 'yes':
            decision += 1
        elif training[i][num_of_attributes] == 'no':
            decision -= 1
        else:
            continue
    if decision >= 0:
        final_decision.append('yes')
    else:
        final_decision.append('no')
        
def calc_all_samples(testing,n):
    for sample_index in range(num_of_test_samples):       
        calc_eucli(testing[sample_index])
        find_nearest_neighbours(n,sample_index)

mean_y = [None] * num_of_attributes
std_y = [None] * num_of_attributes
mean_n = [None] * num_of_attributes
std_n = [None] * num_of_attributes

def stds(alist):
    sum1= 0
    mean1 = statistics.mean(alist)
    for i in alist:
        sum1 += (i-mean1)**2
    return math.sqrt(sum1/(len(alist)-1))

def calc_mean_std():
    for j in range(num_of_attributes):
        mylist_y = []
        mylist_n = []
        for i in range(num_of_train_samples):
            if training[i][num_of_attributes] == 'yes':
                mylist_y.append(training[i][j])
            elif training[i][num_of_attributes] == 'no':
                mylist_n.append(training[i][j])
        mean_y[j] = statistics.mean(mylist_y)
        std_y[j] = stds(mylist_y)
        mean_n[j] = statistics.mean(mylist_n)
        std_n[j] = stds(mylist_n)
                        
def prob_dense():
    NB_decision = []
    product_y = 1
    product_n = 1
    e = 2.71828
    for i in range(num_of_test_samples):
        for j in range(num_of_attributes):            
            if std_y[j] != 0:
                try:
                    product_y *=(1/(std_y[j]*math.sqrt(2*math.pi)))*e**(-((testing[i][j]-mean_y[j])**2) / (2*(std_y[j]**2)))
                    # if i == 0:
                    #     print((1/(std_y[j]*math.sqrt(2*math.pi)))*e**(-((testing[i][j]-mean_y[j])**2) / (2*(std_y[j]**2))))
                    #     print('Ystd:{},train:{},mean:{}'.format(std_y[j],testing[i][j],mean_y[j]))
                except OverflowError:
                    print('Ystd:{},train:{},mean:{}'.format(std_y[j],testing[i][j],mean_y[j]))
                    a=1
            if std_n[j] != 0:
                try:
                    product_n *= (1/(std_n[j]*math.sqrt(2*math.pi)))*e**(-((testing[i][j]-mean_n[j])**2) / (2*(std_n[j]**2)))
                    #if i == 0:
                        # print((1/(std_n[j]*math.sqrt(2*math.pi)))*e**(-((testing[i][j]-mean_n[j])**2) / (2*(std_n[j]**2))))
                        # print('Nstd:{},train:{},mean:{}'.format(std_n[j],testing[i][j],mean_n[j]))
                except OverflowError:
                    print('Nstd:{},train:{},mean:{}'.format(std_n[j],testing[i][j],mean_n[j]))
                    a=1
        product_y *= (num_of_yes/num_of_train_samples)
        product_n *= (num_of_no/num_of_train_samples)
        
        if product_y >= product_n:
            NB_decision.append('yes')
        else:
            NB_decision.append('no')
        # if i == 0:
        #     print(product_n)
        product_y = 1
        product_n = 1
        
    return NB_decision
            
        
if len(mode) == 3:
    n = int(mode[0])
    calc_all_samples(testing,n)
    for eachdecision in final_decision:
        print(eachdecision)
elif len(mode) == 2 and mode == "NB":
    calc_mean_std()
    final_NB = prob_dense()
    for each in final_NB:
        print(each)



    
                



        
        
    

