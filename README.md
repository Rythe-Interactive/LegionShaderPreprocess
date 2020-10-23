Modular Preprocessor for Legion Shaders

```
Preprocess Legion Engine Shaders into pure glsl

Usage:
 python main.py <file> [-D defines ...] [-I includes ...] [options]

Options:
  -D ...                        additional defines (use = to assign a value)
  -I ...                        additional include directories
  -f --format=(1file,nfiles)    output format [default: nfiles]
  -o --output=(file,stdout)     output location [default: file]
```

TODO:
- [ ] output file format 1file needs to be implemented
- [ ] output location stdout needs to be implemented
- [ ] shader corlib needs to be fleshed out (maybe a task of legion-rendering instead?)
