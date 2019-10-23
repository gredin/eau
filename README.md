This project aims at scraping French water quality website (_orobnat.sante.gouv.fr_), parsing water quality data and plotting nice graphs.

## Prerequisites

N.B. In addition to `pip` requirements, command-line application `orca` must be installed and available in PATH. Please refer to instructions at [github.com/plotly/orca](https://github.com/plotly/orca).

Install `pip` requirements:

    virtualenv -p /usr/bin/python3 env
    source env/bin/activate
    pip install -r requirements.txt

## Run

Customize scraping parameters (department, city, number of pages...) in `1_scrape.py`.

Run `1_scrape.py`, `2_parse.py` and `3_plot.py` sequentially.

Enjoy `plots/*.png`.
