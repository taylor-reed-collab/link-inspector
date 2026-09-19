# Link Inspector
![Tests](https://github.com/taylor-reed-collab/link-inspector/actions/workflows/tests.yml/badge.svg)

A small Python command-line tool for checking URLs, measuring response time, and extracting page titles.

## Features

- Checks multiple URLs from the command line
- Reads URLs from a text file
- Reports HTTP status codes
- Measures response time
- Extracts the HTML `<title>` when available
- Exports results to JSON or CSV
- Uses only Python's standard library

## Requirements

- Python 3.10 or newer

No third-party packages are required.

## Usage

Check one URL:

```bash
python link_inspector.py https://example.com
```

Check several URLs:

```bash
python link_inspector.py https://github.com https://python.org
```

Read URLs from a file:

```bash
python link_inspector.py --file examples/urls.txt
```

Save results as JSON:

```bash
python link_inspector.py --file examples/urls.txt --output results.json
```

Save results as CSV:

```bash
python link_inspector.py --file examples/urls.txt --output results.csv
```

Change the timeout:

```bash
python link_inspector.py https://example.com --timeout 5
```
### Example workflow

You can inspect a list of URLs and save the results for later use:

```bash
python link_inspector.py --file examples/urls.txt --output results.json
## Example output
The generated JSON file can then be used by another script or automation workflow.
```text
[OK        ] 200      143.2 ms  https://example.com
             title: Example Domain
```

## Running tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
link-inspector/
├── link_inspector.py
├── README.md
├── examples/
│   └── urls.txt
└── tests/
    └── test_link_inspector.py
```

## License

MIT
