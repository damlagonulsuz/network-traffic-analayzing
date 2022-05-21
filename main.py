import math

import pyshark
import numpy as np
import pandas as pd


capture = pyshark.FileCapture('C:/Users/damla/Desktop/Bitirme Projesi/Bitirme Projesi/Önceki Tez/60sec.pcap', only_summaries=True)

print("Enter an interval time in miliseconds ")
intervalTime = int(input())
intervalTime=float(intervalTime/1000)
k=int(0)
print("Enter an sample value")
sample = int(input())
sample2=int(sample)


baslangıç=int(0)
packetCount = []
totalByte = []
byteList = []
arrivalTime = []
arrivalTimeİndex = []
samplesSumList=[]
sum=int(0)
max=int(0)
maxList=[]
residual=int(0)
residualList=[]
result=[]


for packet in capture:
    line = str(packet)
    formattedLine = line.split(" ")
    byteList.append(formattedLine[5])
    arrivalTime.append(formattedLine[1])


for ix, time in enumerate(arrivalTime):
    if (ix==0):
        continue
    timeInt = int(float(time))
    index = timeInt / float(intervalTime)
    index = int(index)

    if (index + 1) <= len(packetCount):
        packetCount[index] += 1
        totalByte[index] += float(byteList[ix])
    else:
        packetCount.append(1)
        totalByte.append(float(byteList[ix]))

while k<len(totalByte)-sample+1:
    for z in range(baslangıç,sample2):
        sum=sum+totalByte[z]

    samplesSumList.append(sum)
    sum=int(0)
    baslangıç=baslangıç+1
    sample2=sample2+1
    k=k+1


for i in range(0,len(totalByte)-sample+1):
    max = samplesSumList[i]/sample
    final=max*2
    maxList.append(final)


for l in range(0,len(totalByte)-sample):
    residual=maxList[l]-totalByte[l+sample]
    residualList.append(residual)


print("total byte",totalByte)
print("residual",residualList)

# mean absolute error

diff = 0 # gerçek değer ve tahmin arasındaki farklar
add_diff = 0 # gerçek değer ve tahmin arasındaki farkların toplamı
mae_error = []
diff_list = []
for i in range(len(residualList)):
    diff = abs(totalByte[i] - residualList[i])
    diff_list.append(diff)
    add_diff = add_diff + diff_list[i]


mae_error = add_diff / (60/intervalTime)
print('diff list: ', diff_list)
print('add diff: ', add_diff)
print('mae error', mae_error)

# standart deviation fot total byte(current value)
sumOfTotalByte = 0
diff_square = 0
std = 0
std_result = []
for i in range(len(totalByte)):
    sumOfTotalByte = sumOfTotalByte + totalByte[i]
    mean = sumOfTotalByte / len(totalByte)
    diff_square = ((totalByte[i] - mean)**2) / (len(totalByte) - 1)

for k in range(int(60 / intervalTime)):
    std = math.sqrt(diff_square)
    std_result.append(std)

print("sss", len(std_result))
print('sumof: ', sumOfTotalByte)
print('mean: ', mean)
print('diff square', diff_square)
print('standart deviation: ', std)

# standart deviation for residual (prediction) list

sumOfResidual = 0
mean_res = 0
diff_square_res = 0
std_res = 0
std_res_result = []
for i in range(len(residualList)):
    sumOfResidual = sumOfResidual + residualList[i]
    mean_res = sumOfResidual / len(residualList)
    diff_square_res = ((residualList[i] - mean_res)**2) / (len(residualList) - 1)

for k in range(int(60 / intervalTime)):
    std_res = math.sqrt(diff_square_res)
    std_res_result.append(std_res)


print("a", len(std_res_result))
print('sumof_res: ', sumOfResidual)
print('mean: ', mean_res)
print('diff square', diff_square_res)
print('standart deviation residual: ', std_res)




for u in range(sample):
        residualList.insert(u," ")

for q in range(len(residualList)):
    if str(residualList[q])==" ":
        result.append("-")
    elif residualList[q]>0:
        result.append("1")
    else:
        result.append("0")

print(len(totalByte), len(maxList), len(residualList), len(result), len(std_result), len(std_res_result))
data=pd.DataFrame({

    "Current Byte":totalByte,
    "Max Value":maxList,
    "Residual":residualList,
    "Result":result,
    "SD for Byte":std_result,
    "SD for Residual":std_res_result

})
data.to_csv('interval5-sample1.csv',index=False)