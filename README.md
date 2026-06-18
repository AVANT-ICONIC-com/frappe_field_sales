### Frappe Field Sales

**EXPERIMENTAL:** Not all doctypes are implemented yet for practical use, and practical testing has been limited. Automated tests will be expanded in future versions.

Custom field sales app for Frappe Framework: Sales Visit, Mutation Log, Daily Sales Summary, Vehicle Log, get_aussendienst_items, Lead/Item custom fields, company-based access.

**API:** A mobile app can call `get_aussendienst_items` (with optional `numericIdFilter`). This is implemented as a whitelisted method in this app.

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
