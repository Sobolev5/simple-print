# simple-print

A simple function that will help you with debugging.

```no-highlight
https://github.com/Sobolev5/simple-print
```

# How to use it

To install run:
```no-highlight
pip install simple-print
```


Add the following line at the top of your file:
```python
from simple_print.functions import sprint, sprint_f 
```


And simple print your variables:
```python
a = 5
sprint(a)    
sprint(a, 'red') # colors: 'grey', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'. 
sprint_f(a) 
sprint_f(a, 'green')
```


Open your development console and see the result:
```python
a=5 :: line 15
a=5 :: line 15
a=5 :: line 15 :: /my_project/news/views.py
a=5 :: line 15 :: /my_project/news/views.py
```

That's all.