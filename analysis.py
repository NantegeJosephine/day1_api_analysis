"""Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path("output")

# CSV column names. If expected_output.md uses different names, change them here only.
CUSTOMER_COLUMNS = [
    "id", "name", "username", "email", "email_domain", "phone",
    "city", "zipcode", "latitude", "longitude", "company", "website",
]
CITY_COUNT_COLUMNS = ["city", "customer_count"]


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching customers: {error}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    for key, value in record.items():
        print(f"{'  ' * indent}{key}: {type(value).__name__}")
        if isinstance(value, dict):
            explore(value, indent + 1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    explore(item, indent + 1)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    return [
        {
            "id": c["id"],
            "name": c["name"],
            "username": c["username"],
            "email": c["email"],
            "email_domain": c["email"].split("@")[-1].lower(),   # full domain, e.g. april.biz
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),
            "longitude": float(c["address"]["geo"]["lng"]),
            "company": c["company"]["name"],
            "website": c["website"],
        }
        for c in customers
    ]


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {c["address"]["city"] for c in customers}


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop (no Counter, no pandas)."""
    counts = {}
    for c in customers:
        city = c["address"]["city"]
        counts[city] = counts.get(city, 0) + 1
    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv') with a dict comprehension."""
    tlds = [c["email"].split("@")[-1].lower().split(".")[-1] for c in customers]
    return {tld: tlds.count(tld) for tld in set(tlds)}


def print_sorted(counts: dict[str, int], title: str) -> None:
    """Print counts from most to least common, ties listed alphabetically."""
    print(title)
    for name, n in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {name}: {n}")


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(rows, columns=CUSTOMER_COLUMNS)


def plot_distribution(counts: dict[str, int], path: Path,
                      title: str = "Distribution", xlabel: str = "Customers") -> None:
    """Save a horizontal bar chart of counts, most common first."""
    if not counts:
        print(f"No data available for chart: {path}")
        return

    items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    labels = [name for name, _ in items]
    values = [n for _, n in items]

    fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(labels))))
    ax.barh(labels, values, color="steelblue")
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(range(0, max(values) + 1))
    for i, v in enumerate(values):
        ax.text(v + 0.05, i, str(v), va="center")

    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    customers = get_customers()              # fetched once
    if not customers:
        print("No data, stopping.")
        return

    explore(customers[0])

    rows = extract_attributes(customers)

    cities = unique_cities(customers)
    print(f"\nCustomers retrieved : {len(customers)}")
    print(f"Unique cities       : {len(cities)}")
    if len(cities) == len(customers):
        print("Marketing insight   : Every customer is in a different city, "
              "so city is a poor segment for this sample.")
    else:
        print("Marketing insight   : Repeated cities may be useful for geographic segmentation.")

    by_city = city_counts(customers)
    by_tld = email_domain_counts(customers)
    print_sorted(by_city, "\nCustomers by city")
    print_sorted(by_tld, "\nCustomers by email top-level domain")

    df = to_dataframe(rows)
    print("\nDataFrame shape:", df.shape)
    print("DataFrame dtypes:\n", df.dtypes)

    # Confirm pandas agrees with the hand-written counts
    pd_cities = df["city"].value_counts().to_dict()
    pd_groupby = df.groupby("city").size().to_dict()
    pd_tlds = df["email_domain"].str.split(".").str[-1].value_counts().to_dict()
    print("city_counts matches value_counts:", by_city == pd_cities)
    print("city_counts matches groupby:     ", by_city == pd_groupby)
    print("email_domain_counts matches:     ", by_tld == pd_tlds)
    assert by_city == pd_cities == pd_groupby
    assert by_tld == pd_tlds

    # Export to CSV, without the pandas index
    OUTPUT_DIR.mkdir(exist_ok=True)
    df.to_csv(OUTPUT_DIR / "customers.csv", index=False)

    city_df = pd.DataFrame(
        sorted(by_city.items(), key=lambda kv: (-kv[1], kv[0])),
        columns=CITY_COUNT_COLUMNS,
    )
    city_df.to_csv(OUTPUT_DIR / "city_counts.csv", index=False)
    print(f"Wrote {len(df)} rows to customers.csv and {len(city_df)} rows to city_counts.csv")

    # Charts
    plot_distribution(by_city, OUTPUT_DIR / "customer_distribution.png", "Customers by city")
    plot_distribution(by_tld, OUTPUT_DIR / "email_domain_distribution.png",
                      "Customers by email top-level domain")
    print("Charts saved to the output folder.")


if __name__ == "__main__":
    main()