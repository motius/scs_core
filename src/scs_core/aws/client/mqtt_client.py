"""
Created on 6 Oct 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://github.com/aws/aws-iot-device-sdk-python
"""

import AWSIoTPythonSDK.MQTTLib as MQTTLib

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

from scs_core.data.json import JSONify


# --------------------------------------------------------------------------------------------------------------------

class MQTTClient(object):
    """
    classdocs
    """

    __PORT =                        8883

    __QUEUE_SIZE =                  -1                      # recommended: infinite
    __QUEUE_DROP_BEHAVIOUR =        MQTTLib.DROP_OLDEST     # not required for infinite queue
    __QUEUE_DRAINING_FREQUENCY =    1                       # recommended: 2 (Hz)

    __RECONN_BASE =                 1                       # recommended: 1 (sec)
    __RECONN_MAX =                  32                      # recommended: 32 (sec)
    __RECONN_STABLE =               20                      # recommended: 20 (sec)

    __DISCONNECT_TIMEOUT =          30                      # recommended: 10 (sec)
    __OPERATION_TIMEOUT =           30                      # recommended: 5 (sec)

    __PUB_QOS =                     1
    __SUB_QOS =                     1


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, *subscribers):
        """
        Constructor
        """
        self.__client = None
        self.__subscribers = subscribers


    # ----------------------------------------------------------------------------------------------------------------

    def connect(self, auth):
        # client...
        self.__client = AWSIoTMQTTClient(auth.client_id)

        # configuration...
        self.__client.configureEndpoint(auth.endpoint, self.__PORT)

        self.__client.configureCredentials(auth.root_ca_file_path, auth.private_key_path, auth.certificate_path)

        self.__client.configureAutoReconnectBackoffTime(self.__RECONN_BASE, self.__RECONN_MAX, self.__RECONN_STABLE)

        self.__client.configureOfflinePublishQueueing(self.__QUEUE_SIZE)
        self.__client.configureDrainingFrequency(self.__QUEUE_DRAINING_FREQUENCY)

        self.__client.configureConnectDisconnectTimeout(self.__DISCONNECT_TIMEOUT)
        self.__client.configureMQTTOperationTimeout(self.__OPERATION_TIMEOUT)

        # subscriptions...
        for subscriber in self.__subscribers:
            self.__client.subscribe(subscriber.topic, self.__SUB_QOS, subscriber.handler)

        # connect...
        self.__client.connect()


    def disconnect(self):
        self.__client.disconnect()


    # ----------------------------------------------------------------------------------------------------------------

    def publish(self, publication):
        payload = JSONify.dumps(publication.payload)

        self.__client.publish(publication.topic, payload, self.__PUB_QOS)


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        subscribers = '[' + ', '.join(str(subscriber) for subscriber in self.__subscribers) + ']'

        return "MQTTClient:{subscribers:%s}" % subscribers


# --------------------------------------------------------------------------------------------------------------------

class MQTTSubscriber(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, topic, handler):
        """
        Constructor
        """
        self.__topic = topic
        self.__handler = handler


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def topic(self):
        return self.__topic


    @property
    def handler(self):
        return self.__handler


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MQTTSubscriber:{topic:%s, handler:%s}" % (self.topic, self.handler)
