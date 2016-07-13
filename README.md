# srt-Tool
Tool to manipulate .srt subtitle files

```
python srt-Tool.py <file path> <action> <"rate" or "seconds"/second file path> <ratio or seconds>
```
Actions supported:

* shift, requires value in seconds
* frate, requires value of ratio (old rate)/(new rate)
* script, no value argument
* match_new, requires second file path
