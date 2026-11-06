# Day 1 - API Data Analysis | Pesa Pulse

Fetches and analyzes customer data from `https://jsonplaceholder.typicode.com/users` using Python structures, pandas, and matplotlib. The goal is to answer "where are our customers?" for Pesa Pulse's marketing team.

## What it does

The script runs from a `main()` function and fetches the data once.

1. **Fetch:** `get_customers()` calls the API with `timeout=10` and checks the status code. If the request fails, it prints a clear error message and returns an empty list, and the script stops with a message instead of a traceback.
2. **Explore:** `explore()` walks the first customer record recursively and prints every key with its Python type, indented by depth, so the nested objects are visible.
3. **Flatten:** `extract_attributes()` turns each nested record into one flat dictionary with 12 attributes: `id, name, username, email, email_domain, phone, city, zipcode, latitude, longitude, company, website`. Latitude and longitude are converted to floats.
4. **Analyze:**
   * `unique_cities()` uses a set, and the count is compared with the number of customers.
   * `city_counts()` counts customers per city with a loop and a dict (no `Counter`).
   * `email_domain_counts()` counts customers per email top-level domain with a dict comprehension.
5. **Validate:** asserts that the hand-written counts equal `pandas.value_counts()` and `groupby()`.
6. **Export and visualize:** saves two CSVs and two charts to `output/`.

## Nested attributes

Each customer record contains two nested objects:

* `address`: contains `street`, `suite`, `city`, `zipcode` and a further nested object `geo`
* `company`: contains `name`, `catchPhrase` and `bs`

The deepest values are the coordinates, reached one level at a time:

```python
customer["address"]["geo"]["lat"]
```

That is three levels down: customer, then `address`, then `geo`, then `lat` or `lng`. The API returns them as strings, so `extract_attributes` converts them to floats.

## Key findings

* **City:** there are 10 customers in 10 different cities, so every city appears exactly once. City is a poor segment for this sample, because a campaign per city would reach one customer each. The export is sorted by count (highest first), then city A to Z.
* **Email domain:** more informative. Counting by top-level domain, `.biz` is the most common with 3 customers, and `.ca`, `.info`, `.io`, `.me`, `.net`, `.org` and `.tv` have 1 each.

## Which chart is more useful?

The email domain chart (`email_domain_distribution.png`) is more useful. The city chart has ten bars of the same height, so it shows nothing that one sentence couldn't say. The domain chart has one clearly taller bar (`.biz`), so it shows a real difference between customers.

## Outputs

* `output/customers.csv`: flat customer attributes, without the pandas index
* `output/city_counts.csv`: `city, customer_count`
* `output/customer_distribution.png`: customers by city
* `output/email_domain_distribution.png`: customers by email top-level domain

## Project structure

```
├── analysis.py
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   ├── customer_distribution.png
│   └── email_domain_distribution.png
├── requirements.txt
└── README.md
```

## Run

```
pip install -r requirements.txt
python analysis.py
```

`requirements.txt` lists `requests`, `pandas` and `matplotlib`. An internet connection is needed to reach the API.

## Assumptions

* The API is a free mock service, so the data is sample data and not real customers.
* The `email_domain` column holds the full domain (for example `april.biz`). The domain counts use only the last part (`biz`), because all ten full domains are different and counting them would show nothing useful.
* Domains are lowercased before counting.
* Every record has the same structure. A record with a missing key would raise a `KeyError`.
* `explore()` handles dictionaries, and lists that contain dictionaries.
