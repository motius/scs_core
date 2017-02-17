"""
Created on 13 Nov 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

south-coast-science-dev
43308b72-ad41-4555-b075-b4245c1971db
"""

import urllib.parse

from scs_core.osio.client.rest_client import RESTClient
from scs_core.osio.data.topic import Topic


# --------------------------------------------------------------------------------------------------------------------

class TopicManager(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, api_key):
        """
        Constructor
        """
        self.__rest_client = RESTClient(http_client, api_key)


    # ----------------------------------------------------------------------------------------------------------------

    def find_for_org(self, org_id):
        path = '/v2/orgs/' + org_id + '/topics'

        # request...
        self.__rest_client.connect()

        response_jdict = self.__rest_client.get(path)

        self.__rest_client.close()

        topics_jdict = response_jdict.get('topics')
        topics = [Topic.construct_from_jdict(topic_jdict) for topic_jdict in topics_jdict] if topics_jdict else []

        return topics


    def create(self, topic):
        path = '/v2/topics'

        # request...
        self.__rest_client.connect()

        response = self.__rest_client.post(path, topic.as_json())

        self.__rest_client.close()

        success = response == topic.path

        return success


    def delete(self, topic_path):
        path = '/v1/topics/' + urllib.parse.quote(topic_path, '')

        # request...
        self.__rest_client.connect()

        response = self.__rest_client.delete(path)

        self.__rest_client.close()

        success = response == ''

        return success


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "TopicManager:{rest_client:%s}" % self.__rest_client
