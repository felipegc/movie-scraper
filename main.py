import requests
import base64
import os

from flask import escape, abort
import localpackages.pub_sub_service_request as pub_sub_service_request
import localpackages.imdb_service_request as imdb_service_request


def init_scraping(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    """

    request_args = request.args

    if len(request_args) == 0:
        return abort(400, 'Make sure to specify the param: year')
    elif request_args and 'year' not in request_args:
        return abort(400, 'Year is a mandatory param')

    year = request_args['year']
    amount_titles = imdb_service_request.get_amount_titles(year)
    offsets = imdb_service_request.get_offsets_by_page_size(amount_titles)

    for offset in offsets:
        pub_sub_service_request.publish_offset(offset)

    return 'The jobs to process the pages were submitted'


def scraping_pagination(event, context):
    """Background Cloud Function to be triggered by Pub/Sub.
    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    Returns:
        None. The output is written to Cloud Logging.
    """
    import base64

    print("""This Function was triggered by messageId {} published at {} to {}
    """.format(context.event_id, context.timestamp, context.resource["name"]))

    if 'data' in event:
        name = base64.b64decode(event['data']).decode('utf-8')
    else:
        name = 'World'
    print('Hello {}!'.format(name))