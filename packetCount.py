import math
import pyshark
import pandas as pd


capture = pyshark.FileCapture('C:/Users/damla/Desktop/Thesis_181805037_171805016/Data/60sec.pcap', only_summaries=True)

print("Enter an interval time in miliseconds ")# milisayniyeye çeviriyoruz
intervalTime = int(input())
intervalTime=float(intervalTime/1000)
k=int(0)
print("Enter an sample value")
sample = int(input())


sample2 = int(sample)
baslangıç = int(0)
packetCount = []
totalByte = []
byteList = []
arrivalTime = []
arrivalTimeİndex = []
samplesSumList = []
sum = int(0)
max = int(0)
maxList = []
residual = int(0)
residualList = []
result = []
evaluationMetrik = int(0)


for packet in capture:
    line = str(packet)
    formattedLine = line.split(" ")
    byteList.append(formattedLine[5])
    arrivalTime.append(formattedLine[1])


for ix, time in enumerate(arrivalTime):
    if (ix == 0):
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

#kaydırmalı bir şekilde tahminleme yaptık.
while k<len(packetCount)-sample+1:
    for z in range(baslangıç, sample2):
        sum = sum+packetCount[z]

    samplesSumList.append(sum)
    sum=int(0)
    baslangıç = baslangıç+1
    sample2 = sample2+1
    k+=1


for i in range(0,len(packetCount)-sample+1):
    max = samplesSumList[i]/sample
    final = max*2
    maxList.append(final)

#residual

for l in range(0, len(packetCount)-sample):
    residual = maxList[l]-packetCount[l+sample]
    residualList.append(residual)



# mean absolute error

diff = 0 # gerçek değer ve tahmin arasındaki farklar
add_diff = 0 # gerçek değer ve tahmin arasındaki farkların toplamı
mae_error = []
diff_list = []
for i in range(len(residualList)):
    diff = abs(packetCount[i] - residualList[i])
    diff_list.append(diff)
    add_diff = add_diff + diff_list[i]

mae_error = add_diff / (60/intervalTime)

print('mae error', mae_error)

# standart deviation fot total byte(current value)
sumOfPacketCount = 0
diff_square = 0
std = 0
std_result = []
for i in range(len(totalByte)):
    sumOfPacketCount = sumOfPacketCount + packetCount[i]
    mean = sumOfPacketCount / len(packetCount)
    diff_square = ((packetCount[i] - mean) ** 2) / (len(packetCount) - 1)

for k in range(int(60 / intervalTime)):
    std = math.sqrt(diff_square)
    std_result.append(std)

# standart deviation for residual (prediction) list

sumOfResidual = 0
mean_res = 0
diff_square_res = 0
std_res = 0
std_res_result = []
mean_absolute_error = []
for i in range(len(residualList)):
    sumOfResidual = sumOfResidual + residualList[i]
    mean_res = sumOfResidual / len(residualList)
    diff_square_res = ((residualList[i] - mean_res)**2) / (len(residualList) - 1)

for k in range(int(60 / intervalTime)):
    std_res = math.sqrt(diff_square_res)
    std_res_result.append(std_res)


for i in range(int(60 / intervalTime)):
    mean_absolute_error.append(mae_error)


for u in range(sample):
        residualList.insert(u," ")

#çıkan residual değerlerine göre tahminleme gerçek değerin ne kadar altında ne kadar üstünde değerlendiri, üstündeyse 1 altındaysa 0 yazdırdık.
for q in range(len(residualList)):
    if str(residualList[q]) == " ":
        result.append("-")
    elif residualList[q] > 0:
        result.append("1")
    else:
        result.append("0")


for i in range(len(std_res_result)):
    if (len(packetCount) != len(std_res_result)):
        packetCount.append("")

for i in range(len(std_res_result)):
    if (len(result) != len(std_res_result)):
        result.append(-1)

for u in range(sample-1):
    maxList.insert(u, " ")


for i in range(len(std_res_result)):
    if (len(maxList) != len(std_res_result)):
        maxList.append('')

for i in range(len(result)):
    if result[i] == '0':
        evaluationMetrik = evaluationMetrik+1

print(len(packetCount), len(maxList), len(result), len(std_result), len(std_res_result), len(mean_absolute_error))

print("res",result)

data=pd.DataFrame({

    "Current Packets":packetCount,
    "Max Value": maxList,
    "Result": result,
    "Mean Absolute Error":mean_absolute_error,
    "SD for Byte":std_result,
    "SD for Residual":std_res_result

})
data.to_csv('P-interval0.1-sample5.csv', index=False)
