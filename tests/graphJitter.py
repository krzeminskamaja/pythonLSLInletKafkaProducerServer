import json
import matplotlib.pyplot as plt
import numpy as np

@np.vectorize
def constant_function(x):
    return 0.707

@np.vectorize
def constant_function_zero(x):
    return 0

files=['sin10Hzattempt6.txt','sinPlusHalf10Hzattempt6.txt','sinPlusPie10Hzattempt6.txt']
jitterTimestamps=[]
jitterSinvalues=[]
for file in files:
#read all file lines
    with open(file) as f:
        timestamps=[]
        sinValues=[]
        timestampLSL = 0
        timestampSystem = 0 
        lines = f.readlines()
        for index, line in enumerate(lines):
            if(line.strip()==""):
                continue
            sample=line[32:]
            #print(sample)
            sampleAsJson = json.loads(sample)
            #print(sampleAsJson)
            #kafkaTimestamp = line[11:25]
            #print(kafkaTimestamp)
            #if index==0:
            #    timestampLSL = sampleAsJson["timestampLSL"]
            #    timestampSystem = sampleAsJson["timestampSystem"]
            #else:
            lslAbsolute = sampleAsJson["timestamp"] + sampleAsJson["time_correction"]
            sinValue = float(sampleAsJson['sample'][0])
            timestamps.append(lslAbsolute)
            sinValues.append(sinValue)
            #print(sinValue)
            #print(float(kafkaTimestamp))
            #print(lslAbsolute)
            #sampleLatency = float(kafkaTimestamp)-lslAbsolute*1000
            #print(sampleLatency)
            #latency.append(sampleLatency)
            #print(sampleLatency)
        jitterTimestamps.append(timestamps)
        jitterSinvalues.append(sinValues)

plt.title("Plotting jitter with sin functions each delayed by i*pi/2")
for timestampsIndex,timestamps in enumerate(jitterTimestamps):
    print(timestampsIndex)
    print(jitterSinvalues[timestampsIndex])
    if timestampsIndex%3==0:
        color="red"
    elif timestampsIndex%3==1: 
        color="green"
    else:
        color="blue"
    plt.plot(timestamps, jitterSinvalues[timestampsIndex], color=color)



t1 = np.arange(jitterTimestamps[0][0], jitterTimestamps[len(jitterTimestamps)-1][len(jitterTimestamps[len(jitterTimestamps)-1])-1], 0.01)
plt.plot(t1, constant_function(t1),color="blue")
plt.plot(t1, constant_function_zero(t1),color="blue")

plt.legend()
plt.show()