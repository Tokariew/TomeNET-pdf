Parser written in Python to generate pdf with monster from TomeNET.
Compilation is done with luaLaTeX.

Using latexmk for compilation.

```bash
latexmk -lualatex <file>
```

Monsters don't share pages with each other

If monster description start with at least 2-letter word, first letter with by
presented as initial, and the rest of word will be in smallcaps.
