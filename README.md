# Simple print
Powerful debugging & logging tool for Python.  
Userful for `bash` console messages (debug) & `rabbitmq` proxy messages (logging).

```no-highlight
https://github.com/Sobolev5/simple-print
```

# For local development 
## Install
To install run:
```no-highlight
pip install simple-print
```

### Print variables
Function params:
> `c` color [grey, red, green, yellow, blue, magenta, cyan, white]  
> `b` background [on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan]  
> `a` attribute  [bold, dark, underline, blink, reverse, concealed]  
> `p` path [with path to file]  
> `i` indent [indent 1..40]  
> `s` string [return as string]  
> `f` force print [override DEBUG=False]  

```python
from simple_print import sprint 

master = "yoda"
sprint(master) 
sprint(master, c="blue") 
sprint(master, c="blue", b="on_white") 
sprint(master, c="blue", b="on_white", a="underline") 
sprint(master, c="blue", b="on_white", a="bold", p=True) 
my_string = sprint(master, s=True) # return as string
my_string = sprint(master, s=True, p=True) # return as string with path to file 
```
Result:   
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/common.png)   
`p` param is `False` by default, but you can override this behavior with `SIMPLE_PRINT_PATH_TO_FILE=True` in your local environment.

### Example with indent
For indent use `i` param:
```python

def test_indent():
    fruits = ["lemon", "orange", "banana"]
    sprint(fruits, c="green")  
    for fruit in fruits:
        sprint(fruit, c="yellow", i=4)
```
Result:   
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/indent.png)

### Disable printing
Stop printing:
```sh
export DEBUG=False
```
### Test 
```sh
pytest test/test_print.py -s
```
# For catch messages on production server 
## Install
To install run:
```no-highlight
pip install simple-print[broker]
```

Add the following line at the top of your *.py file:
```python
from simple_print import throw, catch 
```
Now you can send messages to rabbitmq queue `amq.direct`.`simple_print` (by default):
```python
throw({"tag":"tag", "msg":{"any_key":"any val"}, uri="amqp://admin:pass@0.0.0.0:5672/vhost") # default queue
throw({"exchange":"any_exchange", "routing_key":"any_key", "tag":"tag", "msg":{"any_key":"any val"}}, uri="amqp://admin:pass@0.0.0.0:5672/vhost") # with custom routing key
 ``` 
Catch last 10 messages from RabbitMQ:
```python
catch(tag="tag", count=10, uri="amqp://admin:pass@0.0.0.0:5672/vhost") # default queue
catch(queue="queue", tag="tag", count=10, console=True, uri="amqp://admin:pass@0.0.0.0:5672/vhost") # custom queue
```
### Test 
```sh
pytest test/test_broker.py -s
```

# TODO
> Kafka support & PyQt support

   
# Try my free time tracker
My free time tracker for developers [Workhours.space](https://workhours.space/). 
