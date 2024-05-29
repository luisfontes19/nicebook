# What's Up With Markdown
## _GitHub Flavored Markdown Cheat Sheet_

This is intended as a quick reference and showcase. For more complete info, see [John Gruber's original spec](http://daringfireball.net/projects/markdown/) and the [Github-flavored Markdown info page](http://github.github.com/github-flavored-markdown/). This cheatsheet is modified from Joshua Pekera'a cheat sheet for "Markdown Here", but this page is just GitHub Flavored Markdown

#### Table of Contents
[Headers](#headers)
[Emphasis](#emphasis)
[Lists](#lists)
[Links](#links)
[Images](#images)
[Code and Syntax Highlighting](#code-and-syntax-highlighting)
[Tables](#tables)
[Blockquotes](#blockquotes)
[Inline HTML](#inline-html)
[Horizontal Rule](#horizontal-rule)
[Line Breaks](#line-breaks)

## Headers

```markdown
For H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------

Or the more common

# H1
## H2
### H3
#### H4
##### H5
###### H6
```

For H1 and H2, an underline-ish style:

Alt-H1
======

Alt-H2
------

Or the more common

# H1
## H2
### H3
#### H4
##### H5
###### H6

---
## Emphasis

```markdown
Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses one tilde ~Scratch This~ or two tildes. ~~Scratch this.~~
```

Emphasis, aka italics, with *asterisks* or _underscores_.

Strong emphasis, aka bold, with **asterisks** or __underscores__.

Combined emphasis with **asterisks and _underscores_**.

Strikethrough uses one tilde ~Scratch This~ or two tildes. ~~Scratch this.~~

Note: In the GitHub text editor, only two tildes shows the inline preview, but
either one or two tildes show the same on output.

---
## Lists
<!--
```markdown
1. First ordered list item
2. Another item
    * Unordered sub-list, lead with 4 spaces
1. Actual numbers don't matter, just that it's a number
    1. Ordered sub-list, lead with 4 spaces
        1. More sub, lead with 4 spaces
            3. Notice how the numbers can get janky
            1. Notice how the numbers can get janky
        2. previous sub
    2. previous sub
4. And another item.


1. Main level
    1. second level
        1. third level
            - fourth level
        2. third level
    2. Second level
7. main level



Unordered list:

- This is a list
    - This is a sub list, lead with 4 spaces
        - and a further sublist, lead with 4 spaces
            - and still more subing
    - back down a few
    1. add in some ordered stuff
    3. more ordered stuff
        2. sub ordered stuff
            1. Hi There
- Back to the future

   Some text that should be aligned with the above item.

* Unordered list can use asterisks
- Or minuses
+ Or pluses
```

1. First ordered list item
2. Another item
    * Unordered sub-list, lead with 4 spaces
1. Actual numbers don't matter, just that it's a number
    1. Ordered sub-list, lead with 4 spaces
        1. More sub, lead with 4 spaces
            3. Notice how the numbers can get janky
        7. previous sub
    2. previous sub
4. And another item.


1. Main level
    1. second level
        1. third level
            - fourth level
        2. third level
    2. Second level
7. main level


Unordered list:

- This is a list
    - This is a sub list, lead with 4 spaces
        - and a further sublist, lead with 4 spaces
            - and still more subing
    - back down a few
    1. add in some ordered stuff
    3. more ordered stuff
        2. sub ordered stuff
            1. Hi There
- Back to the future

* Unordered list can use asterisks
- Or minuses
+ Or pluses -->

---
## Links

There are several ways to create links.

```markdown
[I'm an inline-style link](https://www.google.com)

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[You can use numbers][1] for reference-style link definitions

Or leave it empty and use the [link text itself][]

Some text to show that the reference links can follow later. But while we're at it, might as well point out we can use <a href="#Links" class="dismissed">html links</a> too—this is useful if you need to add a class for use with pages/Jeckyl/whatever.

[arbitrary case-insensitive reference text]: https://git.myndex.com
[1]: http://www.myndex.com/APCA/
[link text itself]: http://www.myndex.com/CVD/
```

[I'm an inline-style link](https://www.google.com)

[I'm a reference-style link][Arbitrary case-insensitive reference text]

[You can use numbers][1] for reference-style link definitions

Or leave it empty and use the [link text itself][]

Some text to show that the reference links can follow later. But while we're at it, might as well point out we can use <a href="#Links" class="dismissed">html links</a> too—this is useful if you need to add a class for use with pages/Jeckyl/whatever.

[arbitrary case-insensitive reference text]: https://git.myndex.com
[1]: http://www.myndex.com/APCA/
[link text itself]: http://www.myndex.com/CVD/


## Images

```markdown
Here's a logo (hover logo to see the alt text):

Inline-style:
![don't forget to do alt text](https://avatars.githubusercontent.com/u/42009457?s=40&v=4 "Logo Title Hover Text")

Reference-style:
![don't forget to do alt text, this is a logo][logo]

And regular HTML img tags work, and allows setting the width or height, and classes for use with pages:

<img width="200" alt="Hi There! Please be descriptive with Alt Text!!" class="recess" src="https://avatars.githubusercontent.com/u/42009457?s=400&u=2dcba5c146315f82f802b8b58e92a4d6b82344b3&v=4">

[logo]: https://avatars.githubusercontent.com/u/42009457?s=40&v=4 "Logo Title Hover Text: The Sequel"

```

Here's a logo (hover to see the title text):

Inline-style:
![don't forget to do alt text](https://avatars.githubusercontent.com/u/42009457?s=40&v=4 "Logo Title Hover Text")

Reference-style:
![don't forget to do alt text, this is a logo][logo]

And regular HTML img tags work, and allows setting the width or height, and classes for use with pages:

<img width="200" alt="Hi There! Please be descriptive with Alt Text!!" class="recess" src="https://avatars.githubusercontent.com/u/42009457?s=400&u=2dcba5c146315f82f802b8b58e92a4d6b82344b3&v=4">

[logo]: https://avatars.githubusercontent.com/u/42009457?s=40&v=4 "Logo Title Hover Text: The Sequel"




## Code and Syntax Highlighting

Code blocks are part of the Markdown spec, but syntax highlighting isn't. However, many renderers -- like Github's and *Markdown Here* -- support syntax highlighting. *Markdown Here* supports highlighting for dozens of languages (and not-really-languages, like diffs and HTTP headers); to see the complete list, and how to write the language names, see the [highlight.js demo page](http://softwaremaniacs.org/media/soft/highlight/test.html).


Inline `code` has `back-ticks around` it.


Blocks of code are either fenced by lines with three back-ticks <code>```</code>, or are indented with four spaces. I recommend only using the fenced code blocks -- they're easier and only they support syntax highlighting.

```markdown

      ```javascript
      var s = "JavaScript syntax highlighting";
      alert(s);
      ```

      ```python
      s = "Python syntax highlighting"
      print s
      ```

      ```
      No language indicated.
      let what = 'will it' + B;

      // let's throw in a comment
      <b>tag</b>.
      ```
          // And code blocks that are just indented 4 spaces
          let me = out > ofHere ? 'bye' : 'never' ;
          return null;
          me = 'help I'm trapped after the return line!';

```

```javascript
var s = "JavaScript syntax highlighting";
alert(s);
```

```python
s = "Python syntax highlighting"
print s
```

```
No language indicated.
let what = 'will it' + B;

// let's throw in a comment
<b>tag</b>.
```
    // And code blocks that are just indented 4 spaces
    let me = out > ofHere ? 'bye' : 'never' ;
    return null;
    me = 'help I'm trapped after the return line!';


```
Again, to see what languages are available for highlighting, and how to write those language names, see the [highlight.js demo page](http://softwaremaniacs.org/media/soft/highlight/test.html).



## Blockquotes

```markdown
>> Blockquotes are very handy in email to emulate reply text.
>> This line is part of the same quote.
> This is one less quote level
This line gets incorporated with the quote because it's only a single newline away

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.
```

>> Blockquotes are very handy in email to emulate reply text.
>> This line is part of the same quote.
> This is one less quote level
This line gets incorporated with the quote because it's only a single newline away

Quote break.

> This is a very long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.


## Horizontal Rule

```markdown
Three or more...

Hyphens

---

Asterisks

***

Underscores
___

All become a thick horizontal line.
```

Three or more...

Hyphens

---

Asterisks

***

Underscores
___

All become a thick horizontal line.


## Line Breaks

Here are some things to try out:

```markdown
Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also begins a separate paragraph, but,
despite having a single newline, it just gets wrapped together.

This line ends with four white spaces before hitting return.
So the next line becomes a single new line
```

Here's a line for us to start with.

This line is separated from the one above by two newlines, so it will be a *separate paragraph*.

This line is also begins a separate paragraph, but,
despite having a single newline, it just gets wrapped together.

This line ends with four white spaces before hitting return.
So the next line becomes a single new line


## End For Now

Any requests for features fleshed out?
