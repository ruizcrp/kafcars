import json
from time import sleep
import requests

from kafka import KafkaProducer

def connect_kafka_producer():
    _producer = None
    try:
        _producer = KafkaProducer(bootstrap_servers=['localhost:29092'], api_version=(0, 10))
    except Exception as ex:
        print('Exception while connecting Kafka')
        print(str(ex))
    finally:
        return _producer

def publish_message(producer_instance, topic_name, key, value):
    try:
        key_bytes = bytes(key, encoding='utf-8')
        value_bytes = bytes(value, encoding='utf-8')
        producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
        producer_instance.flush()
        print('Message published successfully.')
    except Exception as ex:
        print('Exception in publishing message')
        print(str(ex))

vehicle_dictionary={
    "SWISS10_BUS": "Bus",
    "SWISS10_MR": "Motorcycle",
    "SWISS10_PW": "Passenger car",
    "SWISS10_PWA": "Passenger car with trailer",
    "SWISS10_LFW": "Delivery van",
    "SWISS10_LFWA": "Delivery van with trailer",
    "SWISS10_LFWAL": "Delivery van with semitrailer",
    "SWISS10_LKW": "Truck",
    "SWISS10_LZ": "Lorry train",
    "SWISS10_SZ": "Semitrailer"
}

if __name__ == '__main__':
    URL="https://vdp.zh.ch/pws/public-service/readOnlineVbvData/M1419?sampleOnly=false"
    kafka_producer = connect_kafka_producer()
    response= requests.get(URL,stream=True)
    for data in response.iter_content(chunk_size=4096):
        data=str(data)
        print(data)
        data=data[2:-3]
        if data.startswith('{"effectiveTime'):
            try:
                json_object=json.loads(data)
            except:
                print("A catched exception occurred converting json")
            
            vehicleType=json_object['swiss10Class']
            vehicleLength=json_object['length']
            effectiveTime=json_object['effectiveTime']
            output_json=json.dumps({'vehicleType':vehicle_dictionary[vehicleType],
                'vehicleLength':json_object['length'],
                'effectiveTime':json_object['effectiveTime']})
            #output_json='{"vehicleType":"'+vehicle_dictionary[vehicleType]+'","vehicleLength":'+str(vehicleLength)+'","effectiveTime":"'+str(effectiveTime)+'"}'
            publish_message(kafka_producer,"vehicletopic","vehiclecount",output_json)
    if kafka_producer is not None:
        kafka_producer.close()