import json


def create_overrides_json(folder_path, results):
    overrides_data = {}

    for key, value in results.items():
        if key == "letter":
            continue

        try:
            parsed = json.loads(value)
            if isinstance(parsed, dict) and key in parsed:
                overrides_data[key] = parsed[key]
            else:
                overrides_data[key] = parsed
        except json.JSONDecodeError:
            print(f"Warning: {key} is not valid JSON, storing as string")
            overrides_data[key] = value

    output_path = folder_path / "overrides.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(overrides_data, f, ensure_ascii=False, indent=2)

    print(f"Overrides JSON created: {output_path}")
