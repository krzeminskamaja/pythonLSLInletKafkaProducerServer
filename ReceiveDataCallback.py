"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
import msgpack
from kafpaProducer import KafkaProducerMinimal

class ReceiveLSLStreamToKafka:
    def receiveFromInletProduceToKafka(outletName,topicName,kafkaPort):
        # first resolve an EEG stream on the lab network
        print("looking for an {outletName} stream")
        streams = resolve_stream('type', outletName)

        producer = KafkaProducerMinimal 

        # create a new inlet to read from the stream
        inlet = StreamInlet(streams[0])

        while True:
            # get a new sample (you can also omit the timestamp part if you're not
            # interested in it)
            sample, timestamp = inlet.pull_sample()
            print(timestamp, sample)
            #message = msgpack.loads({'sample':sample,'timestamp':timestamp})
            producer.sendToKafka({'sample':sample,'timestamp':timestamp})
            print(timestamp, sample)

