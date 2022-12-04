import pika
import logging
import orjson
import traceback
from secrets import token_hex
from datetime import datetime
from pydantic import Field, BaseModel
from typing import Optional, Union
from .sprint import sprint


class BrokerMessage(BaseModel):
    exchange: Optional[str] = ""
    routing_key: Optional[str] = "simple_print"
    tag: Optional[str] = "tag"
    msg: Optional[dict] = {}
    uuid: Optional[str] = token_hex(16) 
    created: datetime = Field(default_factory=datetime.utcnow)


def throw(message:dict={}, uri:str=None, ttl:int=60, **kwargs) -> Union[None, str]:
    """ 
    throw [send message to broker]:
    message:dict ~ proxy message to broker [now only rabbitmq]   
    uri: str ~ broker uri [now only rabbitmq]  
    ttl: int ~ message time to live (in minutes)
    send json message to amq.direct.simple_print (by default)
    
    message dict schema:
    {
     "exchange": "", # amq.direct by default
     "routing_key": "", # simple_print by default
     "tag": "tag", # tag by default
     "msg": "{'hello':'world'}" # any dict    
    }

    github: https://github.com/Sobolev5/simple-print

    """

    if message:

        assert uri, "Please specify broker uri"         
        assert isinstance(ttl, int) and ttl > 0, "ttl must be positive integer"   

        broker_msg = BrokerMessage(**message)
        if broker_msg.exchange: 
            assert broker_msg.exchange.isascii() and len(broker_msg.exchange) < 256, "Invalid exchange name"     
        if broker_msg.routing_key:
            assert broker_msg.routing_key.isascii() and len(broker_msg.routing_key) < 256, "Invalid routing_key name"  

        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]

        try:
            connection = pika.BlockingConnection(pika.URLParameters(uri))
            channel = connection.channel()      
            if not broker_msg.exchange and broker_msg.routing_key == "simple_print":
                channel.queue_declare(queue="simple_print", durable=True)  
        except Exception as e:
            logging.exception(f"simple-print.broker [CONNECTION ERROR] {e}")     

        try:

            body = {
                "uuid": broker_msg.uuid,
                "tag": broker_msg.tag,
                "msg": broker_msg.msg,      
                "filename": filename,
                "function_name": function_name,
                "lineno": lineno, 
                "created": broker_msg.created.strftime("%Y-%m-%d %H:%M:%S") 
            }

            body = orjson.dumps(body, default=str)      
            channel.basic_publish(exchange=broker_msg.exchange, routing_key=broker_msg.routing_key, properties=pika.BasicProperties(expiration=str(60000*ttl)), body=body)                
            connection.close()
        except Exception as e:
            logging.exception(f"simple-print.broker [THROW ERROR] {e}")     


def catch(tag:Union[str, None]=None, queue:str="simple_print", count:int=10, console:bool=False, uri:str=None, **kwargs) -> list[dict]:
    """ 
    catch [get message from broker]:
    tag:str ~ message tag
    queue:str ~ message queue
    count:int ~ messages num
    console:bool ~ show log (for debug purpose)
    uri: str ~ broker uri [now only rabbitmq]  

    github: https://github.com/Sobolev5/simple-print

    """

    assert uri, "Please specify broker uri"
    assert queue.isascii() and len(queue) < 256, "Invalid queue name"
    
    if tag: 
        assert tag.isascii() and len(tag) < 256, "Invalid tag name"

    messages = []
    connection = pika.BlockingConnection(pika.URLParameters(uri))
    channel = connection.channel()

    if console:
        sprint(connection, f=1)
        sprint(channel, f=1)

    for _ in range(count):
        method_frame, header_frame, body = channel.basic_get(queue)

        if console:
            sprint(body, i=4, f=1)    

        if method_frame:
            message = orjson.loads(body.decode())
            if message:
                if not tag or (message["tag"] == tag):
                    messages.append(message)

                    if console:
                        sprint("asked [OK]", c="green", i=4, f=1)   

                    channel.basic_ack(method_frame.delivery_tag)

    if console:
        for message in messages:
            sprint(message, i=4, f=1)
        len_messages = len(messages)
        sprint(f"len messages {len_messages}", i=4, f=1)

    return messages

