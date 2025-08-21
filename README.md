# Simple print
Local development tool for logs printing.

```no-highlight
https://github.com/Sobolev5/simple-print
```

## Install
To install run:
```no-highlight
pip install simple-print
```

### sprint 
Print variables with its names:
```python
master = "yoda" # variable name master
sprint(master) 
sprint(master, c="magenta") 
sprint(master, c="white", b="on_blue") 
sprint(master, c="blue", b="white", a="underline") 
sprint(master, c="blue", b="on_white", a="bold", p=True) 
master_as_s = sprint(master, s=True) # return as string
master_as_s_with_path = sprint(master, s=True, p=True) # return as string with path to file 
``` 
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/sprint.png)   

> `c` color [grey, red, green, yellow, blue, magenta, cyan, white].
> `b` background [on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan].
> `a` attribute  [bold, dark, underline, blink, reverse, concealed].
> `p` path [True/False] with path to file.
> `l` light [True/False] print without fn name and lineno (shortcut lsprint). 
> `i` indent [1..40].
> `s` string [True/False] return as string.
> `r` return [True/False] print and return as string.
> `f` force print [True/False] ignore SIMPLE_PRINT_ENABLED=False for docker production logs for example. 
> `stream` output stream [stdout, stderr, null]. stdout by default. null means no print.

  
#### Example with indent
Indent print:
```python
def test_indent():
    fruits = ["lemon", "orange", "banana"]
    sprint(fruits, c="green")  
    for fruit in fruits:
        sprint(fruit, c="yellow", i=4)

```  
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/indent.png)
  
  
### lsprint 
Light version of sprint.
```python
master = "yoda" # variable name master
lsprint(master)
   
``` 
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/lsprint.png)   


### SprintErr  
Minified error traceback.
```python
from simple_print import SprintErr

@patch("logging.info", MagicMock(side_effect=[Exception("Something went wrong")]))
def test_sprint_err(self):
   with SprintErr(l=30):
      logging.info("")
  
```
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/sprint_err.png)
  
  
### spprint
Pretty print with indent.  
```python
from simple_print import sprrint

spprint(
   {"hello": c"world", "lorem": "ipsum"}, 
   i=20,
)
  
```
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/spprint.png)
    
  
### Env
Stop printing on production:
```sh
export SIMPLE_PRINT_ENABLED=False

```
  
  
### Test 
```sh
pytest -s

```
