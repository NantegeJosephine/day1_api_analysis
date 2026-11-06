
# Day 1 - API Data Analysis | Pesa Pulse

Fetches and analyzes customer data from `https://jsonplaceholder.typicode.com/users` using Python structures, pandas, and matplotlib.

### What It Does
1. **Fetch:** Gets customer data from API with error handling (`timeout=10`)
2. **Explore:** Recursively inspects nested structure to find paths like `address.city`, `address.geo.lat`, `company.name`
3. **Flatten:** Extracts 12 attributes per customer: `customer_id, name, username, email, email_domain, phone, city, zipcode, latitude, longitude, company, website`
4. **Analyze:**
   - Unique cities and marketing insight
   - `city_counts` - customers per city (loop/dict, no Counter)
   - `email_domain_counts` - customers per email TLD
5. **Validate:** Asserts hand-written counts == `pandas.value_counts()` == `groupby()`
6. **Export & Visualize:** Saves CSVs and charts to `/output`

### Key Findings
- **City:** All 10 customers are in different cities, so city is a poor segment for this sample. Export is sorted by count DESC, then city A-Z.
- **Email Domain:** More useful here - groups customers into repeated categories (e.g. `.biz, .org, .net`) that city cannot show.

### Outputs
- `output/customers.csv` - flat customer attributes
- `output/city_counts.csv` - city, customer_count
- `output/customer_distribution.png` - customers by city
- `output/email_domain_distribution.png` - customers by email domain

### Run
```bash
pip install requests pandas matplotlib
python analysis.py
