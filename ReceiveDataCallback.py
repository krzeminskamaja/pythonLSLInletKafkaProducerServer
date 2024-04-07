"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
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

        while killEventSet==False:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            #message = msgpack.loads({'sample':sample,'timestamp':timestamp})
            producer.sendToKafka({'outletName':outletName, 'sample':sample,'timestamp':timestamp},topicName,kafkaPort)

