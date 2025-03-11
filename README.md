# PubMed Paper Fetcher

## Project Overview

This project is designed to fetch research papers from PubMed based on a given query and identify papers with industry affiliations. The results are saved in a CSV file.

## Code Organization

The project structure is as follows:

```
poetry.lock
pyproject.toml
README.md
src/
    pubmed_paper_fetcher_cli/
        __init__.py
        cli.py
        fetch.py
tests/
    __init__.py
```

- `pyproject.toml`: Contains project metadata and dependencies.
- `src/pubmed_paper_fetcher_cli/`: Contains the main scripts to fetch and process PubMed papers.
- `tests/__init__.py`: Placeholder for unit tests.

## Installation

To install the dependencies, you need to have [Poetry](https://python-poetry.org/) installed. Then, run the following command in the project directory:

```sh
poetry install
```

This will install all the required dependencies specified in the `pyproject.toml` file.

## Usage

To execute the program, use the following command:

```sh
poetry run python src/pubmed_paper_fetcher_cli/cli.py <query> [-f <filename>] [-d]
```

- `<query>`: The search query for PubMed.
- `-f <filename>`: (Optional) The filename to save the results. If not provided, the results will be printed to the console.
- `-d`: (Optional) Enable debug output.

Example:

```sh
poetry run python src/pubmed_paper_fetcher_cli/cli.py "cancer research" -f results.csv -d
```

## Tools and Libraries

The following tools and libraries were used to build this program:

- [Requests](https://docs.python-requests.org/en/latest/): For making HTTP requests to the PubMed API.
- [Pandas](https://pandas.pydata.org/): For handling and saving data in CSV format.
- [lxml](https://lxml.de/): For parsing XML responses from the PubMed API.
- [Poetry](https://python-poetry.org/): For dependency management and packaging.

## License

This project is licensed under the MIT License.
