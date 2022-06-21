# SafeLock-CSV

This tool takes the csv created in SafeLock Stellar One console from Stellar Enforce scan tool to make the whitelist.

You must install the python requirements first, this tool was made to work with Python 3.9.

## Installation

Use the package manager pip to install the requirements

```bash
pip install -f requirements.txt
```

Requirements.txt
~~~~
numpy==1.22.4
pandas==1.4.2
python-dateutil==2.8.2
pytz==2022.1
six==1.16.0
~~~~~

Two folders must be created in the root of this tool:
- approve-list-csv
- approve-list-done

The CSV created in Stellar Enforce must be in the *approve-list-csv* folder.

The processed CSV files will be in the *approved-list-done*

## Usage

```bash
python main.py
````

## Contributing
Pull requests are welcome. For major changes, please open a issue first to discuss what you would like to change.

Please make sure to update the README as appropiate.

## License
## License
[MIT](https://choosealicense.com/licenses/mit/)