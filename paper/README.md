# Paper build status

`main.tex` is an unlocked development manuscript. It follows the project
section order and uses a two-column `article` layout with an `abbrv` numeric
bibliography.

The current environment has no detected `pdflatex`, `xelatex` or `bibtex`, so
no compiled PDF is claimed. In a TeX-enabled environment, run from `paper/`:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Compilation and visual inspection are separate acceptance gates. Do not treat
the source-only draft as a rendered or submission-ready paper.
