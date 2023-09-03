# Simple print
Print value with variable name.  
Userful for fast debugging.

```no-highlight
https://github.com/Sobolev5/simple-print
```

## Install
To install run:
```no-highlight
pip install simple-print
```

### Print variables with names
Full code example [you can see here](tests/test_sprint.py)
```python
master = "yoda" # variable name master
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

Fn params:
> `c` color [grey, red, green, yellow, blue, magenta, cyan, white]  
> `b` background [on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan]  
> `a` attribute  [bold, dark, underline, blink, reverse, concealed]  
> `p` path [with path to file]  
> `i` indent [indent 1..40]  
> `s` string [return as string]  
> `f` force print [ignore SIMPLE_PRINT_ENABLED=False for docker production logs for example]  


### Example with indent
For indent use `i` param. Full code example [you can see here](tests/test_sprint.py)
```python

def test_indent():
    fruits = ["lemon", "orange", "banana"]
    sprint(fruits, c="green")  
    for fruit in fruits:
        sprint(fruit, c="yellow", i=4)
```
Result:   
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/indent.png)


### Pretty error tb
Show errors with pretty traceback:  
```python
from simple_print import SprintErr

with SprintErr():
    raise ValueError
```


### ENV
Stop printing:  
```sh
export SIMPLE_PRINT_ENABLED=False
```
  
Always show path to file:  
```sh
export SIMPLE_PRINT_SHOW_PATH_TO_FILE=True
```

### Test 
```sh
tox
```
