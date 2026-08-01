import copy
import json
import sys
from pathlib import Path


APP_NAMES = ("frappe_field_sales", "erpnext", "crm")


def read_bundle(generated_dir: Path, app: str) -> dict:
	with (generated_dir / "apps" / f"{app}.json").open(encoding="utf-8") as source:
		return json.load(source)


def make_deterministic(document: dict) -> dict:
	document = copy.deepcopy(document)
	document.pop("x-frappe-generated-at", None)
	return document


def merge_bundles(bundles: list[dict]) -> dict:
	combined = make_deterministic(bundles[0])
	combined["info"] = {
		"title": "Frappe Field Sales, ERPNext and Frappe CRM API",
		"version": "1.0.0",
		"summary": "Generated API surface for Frappe Field Sales and its application dependencies.",
	}
	combined["$self"] = "/openapi/frappe_field_sales_full.json"
	combined.pop("x-frappe-app", None)
	combined["x-frappe-apps"] = list(APP_NAMES)
	combined["x-frappe-generated-source"] = "alyf-de/frappe_openapi"

	paths = {}
	schemas = {}
	security_schemes = {}
	tags = set()
	for bundle in bundles:
		paths.update(bundle.get("paths", {}))
		components = bundle.get("components", {})
		schemas.update(components.get("schemas", {}))
		security_schemes.update(components.get("securitySchemes", {}))
		tags.update(tag["name"] for tag in bundle.get("tags", []) if tag.get("name"))

	combined["paths"] = dict(sorted(paths.items()))
	combined["components"] = {
		"schemas": dict(sorted(schemas.items())),
		"securitySchemes": dict(sorted(security_schemes.items())),
	}
	combined["tags"] = [{"name": tag} for tag in sorted(tags)]
	return combined


def write_document(path: Path, document: dict) -> None:
	path.parent.mkdir(parents=True, exist_ok=True)
	path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
	if len(sys.argv) != 3:
		raise SystemExit("usage: merge_openapi_specs.py GENERATED_DIR OUTPUT_DIR")
	generated_dir = Path(sys.argv[1])
	output_dir = Path(sys.argv[2])
	bundles = [read_bundle(generated_dir, app) for app in APP_NAMES]
	write_document(output_dir / "frappe_field_sales.json", make_deterministic(bundles[0]))
	write_document(output_dir / "frappe_field_sales_full.json", merge_bundles(bundles))


if __name__ == "__main__":
	main()
