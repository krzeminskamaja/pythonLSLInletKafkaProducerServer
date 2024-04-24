"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream,local_clock
import datetime
import msgpack
from kafpaProducer import KafkaProducerMinimal

class ReceiveLSLStreamToKafka:
    def __init__(self):
        self.isActive = True
    def receiveFromInletProduceToKafka(self,outletName,topicName,kafkaPort,killEventSet):
        # first resolve an EEG stream on the lab network
        print(f'looking for an {outletName} stream')
        streams = resolve_stream('type', outletName)

        producer = KafkaProducerMinimal 

        # create a new inlet to read from the stream
        inlet = StreamInlet(streams[0])
        # send stream info as a first message
        info = inlet.info()
        producer.sendToKafka({'outletName':outletName, 'info':info.as_xml(), 'timestampLSL': local_clock(), 'timestampPython':datetime.datetime.now().strftime("%Y/%d/%m, %H:%M:%S:%f")},topicName,kafkaPort)

        while killEventSet==False:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            time_correction = inlet.time_correction()
            print(sample)
            print(timestamp)
            print(time_correction)
            #message = msgpack.loads({'sample':sample,'timestamp':timestamp})
            producer.sendToKafka({'outletName':outletName, 'sample':sample,'timestamp':timestamp,'time_correction':time_correction},topicName,kafkaPort)

