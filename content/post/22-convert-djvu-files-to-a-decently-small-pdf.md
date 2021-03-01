---
title: "Convert djvu files to a decently small pdf"
date: 2013-12-22T21:05:25.000Z
lastmod: 2013-12-22T21:05:25.000Z
tags: ["tips", "djvu", "conversion", "pdf"]
categories: ["Blog"]
slug: "convert-djvu-files-to-a-decently-small-pdf"
disqus_identifier: 22
---

Despite there are few decent [djvu](https://en.wikipedia.org/wiki/DjVu) readers, they are not as comfortable as the pdf readers. Moreover, it is not really possible to open djvu files in eInk ebook readers.

Additionally, if you have ever tried to convert djvu files to pdf (or ps), you should have noted that the output is either corrupted or unbelievably big.

There is an hack that could come in help. Open your `.bashrc` (or `.zshrc` if you use Zsh) and define this new [alias](https://tldp.org/LDP/abs/html/aliases.html) (i.e. add this line somewhere, say at the end of the file)

```sh
    alias djvu2pdf='LC_ALL=C ddjvu -format=pdf -mode=black -quality=85'
```
Save and reopen your terminal.

Now, running

```sh
    djvu2pdf file.djvu output.pdf
```
will create a relatively small file with decent/good quality.

Note that the `-mode=black` option improves sensibily the size of the file, but at the price of destroying some of the figures. 

If you really need the figures, you could drop the option or create a different alias, e.g.

```sh
alias djvu2pdf4pics='LC_ALL=C ddjvu -format=pdf -quality=85'
```