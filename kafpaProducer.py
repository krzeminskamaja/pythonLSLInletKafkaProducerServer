from asyncio import log
import json
from kafka import KafkaProducer
#from kafka.errors import KafkaError
import msgpack

class KafkaProducerMinimal:


    def sendToKafka(msg,topicName='quickstart-events',kafkaPort=9092):
        #producer = KafkaProducer(bootstrap_servers=['localhost:9092'],api_version=(0,11,5),value_serializer=lambda m: json.dumps(m).encode('ascii'),max_block_ms = 120000)
        #TODO: refactor this to create one common object outside of this methods
        producer = KafkaProducer(bootstrap_servers=['localhost:'+str(kafkaPort)],api_version=(0,11,5),value_serializer=lambda m: json.dumps(m).encode('ascii'))

        # Asynchronous by default
        _ = producer.send(topicName, msg)

# Block for 'synchronous' sends
# try:
#   record_metadata = future.get(timeout=10)
#except KafkaError:
    # Decide what to do if produce request failed...
#    print(KafkaError)
#    pass

# Successful result returns assigned partition and offset
# print (record_metadata.topic)
# print (record_metadata.partition)
# print (record_metadata.offset)

# produce keyed messages to enable hashed partitioning
# producer.send('my-topic', key=b'foo', value=b'bar')

# encode objects via msgpack
# producer = KafkaProducer(value_serializer=msgpack.dumps)
# producer.send('msgpack-topic', {'key': 'value'})

# produce json messages
#producer = KafkaProducer(value_serializer=lambda m: json.dumps(m).encode('ascii'))
#producer.send('json-topic', {'key': 'value'})

# produce asynchronously
#for _ in range(100):
#    producer.send('my-topic', b'msg')

def on_send_success(record_metadata):
    print(record_metadata.topic)
    print(record_metadata.partition)
    print(record_metadata.offset)

def on_send_error(excp):
    log.error('I am an errback', exc_info=excp)
    # handle exception

# produce asynchronously with callbacks
# producer.send('my-topic', b'raw_bytes').add_callback(on_send_success).add_errback(on_send_error)

# block until all async messages are sent
# producer.flush()

# configure multiple retries
# producer = KafkaProducer(retries=5)