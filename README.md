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

### Features
- Variable value on the first line, metadata (type, file, line, function, time) on the second line
- Clickable file paths in terminal output — Cmd+click (macOS) or Ctrl+click (Linux/Windows) to jump to source  
- Colors, backgrounds, attributes, indentation

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
> `l` light [True/False] print without fn name and lineno (shortcut lprint).   
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
  
  
### lprint 
Light version of sprint (no metadata line). Also available as `lsprint` for backward compatibility.
```python
master = "yoda" # variable name master
lprint(master)
   
``` 
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/lprint.png)   


### SprintErr  
Minified error traceback with box frame.
```python
from simple_print import SprintErr

bob = []
with SprintErr(l=30):
    bob[2]  # pretty error traceback (show 30 lines)
  
```
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/sprint_err.png)
  
  
### spprint
Pretty print dict with box frame.  
```python
from simple_print import spprint

spprint({"hello": "world", "lorem": "ipsum"})
spprint({"hello": "world", "lorem": "ipsum"}, i=20)  # with indent
  
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
