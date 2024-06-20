# Simple print
Collection of console debug utilities.  
Userful for local development.

```no-highlight
https://github.com/Sobolev5/simple-print
```

## Install
To install run:
```no-highlight
pip install simple-print
```

### sprint 🚀 print variables with names

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
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/common.png)   

Fn params:
> `c` color [grey, red, green, yellow, blue, magenta, cyan, white]  
> `b` background [on_grey, on_red, on_green, on_yellow, on_blue, on_magenta, on_cyan]  
> `a` attribute  [bold, dark, underline, blink, reverse, concealed]  
> `p` path [with path to file]  
> `i` indent [indent 1..40]  
> `s` string [return as string] 
> `r` return [print and return as string] 
> `f` force print [ignore SIMPLE_PRINT_ENABLED=False for docker production logs for example]  
> `stream` output stream  [stdout, stderr, null]. stdout by default. null means no print.


#### Example with indent
```python

def test_indent():
    fruits = ["lemon", "orange", "banana"]
    sprint(fruits, c="green")  
    for fruit in fruits:
        sprint(fruit, c="yellow", i=4)

```  
![](https://github.com/Sobolev5/simple-print/blob/master/screenshots/indent.png)


### SprintErr 🚀 minified error traceback
Show last 20 error_tb lines (useful for large error tb):  
```python
from simple_print import SprintErr

with SprintErr(l=20):
   some_broken_code / 0
   
```

### spprint 🚀 pretty print with indent
Show last 20 error_tb lines (useful for large error tb):  
```python
from simple_print import sprrint

spprint({"hello": c"world", "lorem": "ipsum"}, i=20)

                        {
                           'hello': 'world', 
                           'lorem': 'ipsum'
                        }
```


### ArtEnum 🚀 collection of ascii Art
```sh
from simple_print import ArtEnum

print(ArtEnum.PACMAN_1)

   ,##.                   ,==.
 ,#    #.                 \ o ',
#        #     _     _     \    \
#        #    (_)   (_)    /    ; 
 `#    #'                 /   .'  
   `##'                   "=="

```
  

### Env
Stop printing on production:  
```sh
export SIMPLE_PRINT_ENABLED=False

```

  
### Test 
```sh
tox

```
