# RFC Docset

This repository offers the [RFC documents](https://tools.ietf.org/rfc/index) as downloadable docset for tools like [Dash](https://kapeli.com/dash).

![RFC Docset](https://raw.githubusercontent.com/nlohmann/rfc-docset/master/screenshot.png)

## Features

Within [Dash](https://kapeli.com/dash), the docset has the following features:

- Offline access to more than 7900 RFC documents.
- Quicksearch for title or RFC number.
- Full-text search inside the current RFC.
- Links to other RFCs (also to sections) work within the docset.
- "Open Online Page" functionality opens RFC at <https://tools.ietf.org/html>.

## Installation

Just open file `rfc.docset` with Dash. There will be a new entry "RFC" in the documentation list. You can search for an RFC with the prefix `rfc:`.

## Update docset

The docset can be built from scratch as follows

```sh
# download RFCs
make download -j10
# recreate the docset
make rfc.docset
```

## License

<img align="right" src="http://opensource.org/trademarks/opensource/OSI-Approved-License-100x137.png">

The code to create the docset is licensed under the [MIT License](http://opensource.org/licenses/MIT):

Copyright &copy; 2016 [Niels Lohmann](http://nlohmann.me)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Further copyright notices

- This project is not affilated with [Dash](https://kapeli.com/dash), which is Copyright &copy; 2016 Kapeli.
- The RFC documents are copyright by the IETF Trust and the persons identified as the document authors. All rights reserved. The RFC documents have been downloaded from <https://tools.ietf.org/html> and edited as follows:
  - Relative links to `./rfc0000` have been changed to `rfc0000.html` to work in the context dof Dash.
