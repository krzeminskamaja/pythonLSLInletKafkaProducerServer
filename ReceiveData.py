"""Example program to show how to read a multi-channel time series from LSL."""

from pylsl import StreamInlet, resolve_stream
import msgpack
from kafpaProducer import KafkaProducerMinimal


def main():
    # first resolve an EEG stream on the lab network
    print("looking for an ET stream...")
    streams = resolve_stream('type', 'ET')

    producer = KafkaProducerMinimal 

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    while True:
        # get a new sample (you can also omit the timestamp part if you're not
        # interested in it)
        sample, timestamp = inlet.pull_sample()
        #message = msgpack.loads({'sample':sample,'timestamp':timestamp})
        producer.sendToKafka({'sample':sample,'timestamp':timestamp})
        print(timestamp, sample)


if __name__ == '__main__':
    main()
