### Frappe Field Sales

Custom field sales app: Sales Visit, Mutation Log, Daily Sales Summary, Vehicle Log, get_aussendienst_items, Lead/Item custom fields, company-based access.

**API:** The mobile app calls `get_aussendienst_items` (with optional `numericIdFilter`). This is implemented as a whitelisted method in this app. You can remove any existing Server Script that provided `get_aussendienst_items`; use this app method instead.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app frappe_field_sales
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/frappe_field_sales
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
