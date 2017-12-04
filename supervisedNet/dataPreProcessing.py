import csv

flapDat = open('flappyData77.csv','r')
flapDat = csv.reader(flapDat,delimiter=',')
dataset = list(flapDat)


#let's just get the x,y, and jump values for now
dataset = [j[0:3] for j in dataset]



#convert the booleans to digits
tCh = 0
fCh = 0
for i in range(0,len(dataset)):
    for j in range(0,len(dataset[0])):
        if dataset[i][j] == 'True':
            dataset[i][j] = '1'
            tCh += 1
        elif dataset[i][j] == 'False':
            dataset[i][j] = '0'
            fCh += 1
print('True changed', tCh)
print('False changed', fCh)
    

#dataset = [[int(float(j)) for j in i] for i in dataset]

writer = csv.writer(open('output77.csv', 'w'))
writer.writerows(dataset)



# 21_2
##T changed 52
##F changed 822

## 77
##True changed 185
##False changed 2763
