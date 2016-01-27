MultiSearcher
---

The MultiSearcher is an open source scan which uses some engines
to find web sites with the use of keywords and phrases

### Dependencies
* Python 2.7+
* requests
* BeautifulSoup

Installation
----

Preferably, you can download MultiSearcher by cloning the [Git](https://github.com/proclnas/multisearcher) repository:

    git clone https://github.com/proclnas/multisearcher.git 
	cd multisearcher
	pip install -r requirements.txt

Usage
----

Basic usage:

	python multisearcher.py -f word_file -o output -t threads
	
The words in the word_file are separated by a end_line:
	
	work /wp-content/
	products index.php?option=
	...

Or full help:

    python multisearcher.py -h
    
Demo
----
[![Youtube Video](http://i.imgur.com/1CRVxu1.jpg)](https://www.youtube.com/watch?v=NaLIHsaBxDM)

### License
```
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
