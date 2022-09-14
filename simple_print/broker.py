import pika
import orjson
import traceback
from secrets import token_hex
from datetime import datetime
from pydantic import Field, BaseModel
from typing import Optional, Union


class BrokerMessage(BaseModel):
    exchange: Optional[str] = '' 
    routing_key: Optional[str] = 'simple_print'
    tag: Optional[str] = 'tag'
    msg: Optional[dict] = {}
    uuid: Optional[str] = token_hex(16) 
    created: datetime = Field(default_factory=datetime.utcnow)



def throw(message:dict={}, uri:str=None, **kwargs) -> Union[None, str]:
    """ 
    throw [send message to broker]:
    message:dict ~ proxy message to broker [now only rabbitmq]   
    uri: str ~ broker uri [now only rabbitmq]  
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
        broker_msg = BrokerMessage(**message)
        assert uri, "Please specify broker uri"           
        if broker_msg.exchange: 
            assert broker_msg.exchange.isascii() and len(broker_msg.exchange) < 256, "Invalid exchange name"     
        if broker_msg.routing_key:
            assert broker_msg.routing_key.isascii() and len(broker_msg.routing_key) < 256, "Invalid routing_key name"  

        stack = traceback.extract_stack()
        filename, lineno, function_name, code = stack[-2]

        connection = pika.BlockingConnection(pika.URLParameters(uri))
        channel = connection.channel()
        
        if not broker_msg.exchange and broker_msg.routing_key == "simple_print":
            channel.queue_declare(queue="simple_print", durable=True)  

        body = {
            "uuid": broker_msg.uuid,
            "tag": broker_msg.tag,
            "msg": broker_msg.msg,      
            "filename": filename,
            "function_name": function_name,
            "lineno": lineno, 
            "created": broker_msg.created.strftime("%Y-%m-%d %H:%M:%S") 
        }

        try:
            body = orjson.dumps(body, default=str)      
            channel.basic_publish(exchange=broker_msg.exchange, routing_key=broker_msg.routing_key, properties=pika.BasicProperties(expiration=str(60000*60)), body=body)                
            connection.close()
        except Exception as e:
            # catch any exception. do nothing.
            pass


def catch(tag:Union[str, None]="tag", queue:str="simple_print", count:int=10, console:bool=False, uri:str=None, **kwargs) -> Union[None, list[str]]:
    """ 
    catch [get message from broker]:
    tag:str ~ message tag
    queue:str ~ message queue
    count:int ~ messages num
    console:bool ~ print to console
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
    for _ in range(count):
        method_frame, header_frame, body = channel.basic_get(queue)
        if method_frame:
            message = orjson.loads(body.decode())
            if not tag or message["tag"] == tag:
                messages.append(message)
                channel.basic_ack(method_frame.delivery_tag)

    if console:
        [print(body, "\n", "*" * 50) for body in messages]
    else:
        return messages

