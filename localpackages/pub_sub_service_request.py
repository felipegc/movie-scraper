import os
import json
from google.cloud import pubsub_v1

# Instantiates a Pub/Sub client
publisher = pubsub_v1.PublisherClient()
# TODO(felipegc) should these both be in an external file?
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
TOPIC_OFFSET = 'scraping_pagination_topic'


def publish(topic_name, message_json):
    # References an existing topic
    topic_path = publisher.topic_path(PROJECT_ID, topic_name)
    message_bytes = message_json.encode('utf-8')

    # Publishes a message
    try:
        print(f'Publishing {message_json} to topic {topic_name}')
        publish_future = publisher.publish(topic_path, data=message_bytes)
        publish_future.result()  # Verify the publish succeeded

        return 'Message published.'
    except Exception as e:
        print(e)
        return (e, 500)


def publish_offset(start):
    message_json = json.dumps({
        'data': {'offset': start},
    })
    msg = publish(TOPIC_OFFSET, message_json)

    return msg