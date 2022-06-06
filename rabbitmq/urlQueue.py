import json

from rabbitmq.connector import Connector

class UrlQueue(Connector):
    """
    Create RabbitMQ Connector Wrapper for UrlQueue
    """

    def setupUrlQueue(self):
        """
        Setup UrlQueue with RabbitMQ AMQP protocol
        """
        # Declare Queue
        e = self.channel.exchange_declare(exchange='urls', exchange_type='fanout')
        q = self.channel.queue_declare(queue='')
        self.channel.queue_bind(exchange='urls', queue=q.method.queue)

    def publishUrl(self, type, url):
        payload = json.dumps({
            'type': type,
            'url': url,
        })
        self.channel.basic_publish(exchange='urls', routing_key='', body=payload)

    # Callback Def
    #
    # callback(type, url)
    def consumeUrl(self, callback):
        def callback_func(ch, method, properties, body):
            # Decode Json Payload
            payload = json.loads(body)
            callback(payload.get('type'), payload.get('url'))

        self.channel.basic_consume(callback_func, queue='', no_ack=True)
        self.channel.start_consuming()
