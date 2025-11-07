import os
import sys
import time
import json
import argparse
import requests
import pandas as pd

API_BASE = "https://www.vaspexpresso.pt/api/TrackAndTrace/?term="

def normalize_vasp_response(raw_data: dict, code: str, snapshot_dir="snapshots") -> dict:
    number = raw_data.get("service", {}).get("serviceBarCode", code)
    current_event = raw_data.get("currentEvent", {}) or {}
    current_state = (
        current_event.get("eventDescriptionPT")
        or current_event.get("eventDescriptionENG")
        or "Unknown"
    )
    last_update = current_event.get("eventDate")
    events = []
    for e in raw_data.get("clientEvents", []):
        events.append({
            "timestamp": e.get("eventDate"),
            "date_raw": e.get("createdDateUtc") or e.get("eventDate"),
            "state": e.get("eventDescriptionPT") or e.get("eventDescriptionENG"),
            "location": e.get("depotName"),
            "description": e.get("incidencePT") or e.get("incidenceENG")
        })
    events.sort(key=lambda x: x.get("timestamp") or "")
    json_path = save_json_snapshot(raw_data, number, snapshot_dir)
    html_path = save_html_snapshot(number, raw_data, snapshot_dir)
    return {
        "number": number,
        "status": "ok" if events else "not_found",
        "last_update": last_update,
        "current_state": current_state,
        "events": events,
        "raw_json_snapshot_path": json_path,
        "raw_html_snapshot_path": html_path
    }


def get_tracking_info(codes):
    results = []
    print("\n🚚 Starting API lookups...\n")

    for code in codes:
        # Validar código
        if not code or len(str(code)) < 5:
            print(f"⚠️  Skipping invalid code: {code}")
            continue

        url = f"{API_BASE}{code}"
        print(f"🔍 Checking {code} ...")

        try:
            resp = requests.get(url, timeout=10)

            if resp.ok:
                try:
                    normalized = normalize_vasp_response(resp.json(), code)
                    results.append(normalized)
                    print(f"📦 {code} → {normalized['current_state']}")
                except json.JSONDecodeError:
                    print(f"❌ {code} → Invalid JSON response from server.")
                except Exception as e:
                    print(f"❌ {code} → Error processing response: {e}")

            else:
                print(f"❌ {code} → HTTP {resp.status_code} (server returned error)")

        except requests.exceptions.Timeout:
            print(f"⏱️  {code} → Request timed out after 10 seconds.")
        except requests.exceptions.ConnectionError:
            print(f"🌐 {code} → Network connection error. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            print(f"⚠️  {code} → Unexpected network error: {e}")
        except Exception as e:
            print(f"💥 {code} → Unexpected error: {e}")

        # Pequeno delay para respeitar o servidor
        time.sleep(1)

    return results


def read_codes(file):
    try:
        if file.endswith(".csv"):
            df = pd.read_csv(file)
            if "codigo" in df.columns:
                codes = df["codigo"].dropna().astype(str).tolist()
            else:
                codes = df.iloc[:, 0].dropna().astype(str).tolist()
        elif file.endswith(".txt"):
            with open(file, "r", encoding="utf-8") as f:
                codes = [line.strip() for line in f if line.strip()]
        else:
            raise ValueError("Unsupported file format. Use .txt or .csv")

        # Validar códigos
        valid_codes = [c for c in codes if len(c) >= 13]
        invalid = len(codes) - len(valid_codes)
        if invalid:
            print(f"⚠️  Skipped {invalid} invalid or empty codes.")
        return valid_codes

    except FileNotFoundError:
        print(f"❌ File '{file}' not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"⚠️  File '{file}' is empty or unreadable.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error reading file '{file}': {e}")
        sys.exit(1)


def save_results(results, save_path):
    try:
        if not results:
            print("⚠️ No results to save.")
            return False

        if save_path.endswith(".json"):
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=4)
        elif save_path.endswith(".csv"):
            pd.DataFrame(results).to_csv(save_path, index=False)
        else:
            print("⚠️ Unsupported save format. Use .json or .csv")
            return False

        print(f"✅ Results successfully saved to: {save_path}")
        return True

    except PermissionError:
        print(f"❌ Permission denied when saving to '{save_path}'. Try another folder.")
    except Exception as e:
        print(f"❌ Failed to save results: {e}")

    return False


def save_json_snapshot(data, code, snapshot_dir="snapshots"):
    os.makedirs(snapshot_dir, exist_ok=True)
    path = os.path.join(snapshot_dir, f"{code}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return path


def save_html_snapshot(code, raw_data, snapshot_dir="snapshots"):
    os.makedirs(snapshot_dir, exist_ok=True)
    path = os.path.join(snapshot_dir, f"{code}.html")

    number = raw_data.get("service", {}).get("serviceBarCode", code)
    events = raw_data.get("clientEvents", [])

    html = f"""
    <html><head>
    <meta charset='utf-8'>
    <title>Tracking {number}</title>
    <style>
        body {{ font-family: Arial; margin: 20px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; }}
        th {{ background: #1e3a8a; color: white; }}
        tr:nth-child(even) {{ background: #f2f2f2; }}
    </style>
    </head><body>
    <h1>Tracking Snapshot — {number}</h1>
    <table>
        <tr><th>Date</th><th>State</th><th>Location</th><th>Description</th></tr>
    """
    for e in events:
        html += f"<tr><td>{e.get('eventDate','')}</td><td>{e.get('eventDescriptionPT','')}</td><td>{e.get('depotName','')}</td><td>{e.get('incidencePT','')}</td></tr>"
    html += "</table></body></html>"

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    parser = argparse.ArgumentParser(description="Track Vaspexpresso shipment codes.")
    parser.add_argument("-i", "--input", help="Input file with tracking codes (.txt or .csv)")
    parser.add_argument("-o", "--output", help="Output file path (.json or .csv)")
    args = parser.parse_args()

    # Input file
    input_file = args.input
    while not input_file:
        input_file = input("Enter path to input file with codes (.txt or .csv): ").strip()
        if not os.path.isfile(input_file):
            print("❌ File does not exist. Try again.")
            input_file = None

    codes = read_codes(input_file)
    print(f"📄 Loaded {len(codes)} valid codes.\n")

    if not codes:
        print("⚠️  No valid codes found. Exiting.")
        sys.exit(0)

    results = get_tracking_info(codes)

    # Output file
    output_file = args.output
    if not output_file:
        default_dir = os.path.dirname(os.path.abspath(input_file))
        output_file = input(f"Enter path to save results (.json or .csv) [default: {default_dir}/results.json]: ").strip()
        if not output_file:
            output_file = os.path.join(default_dir, "results.json")

    saved = save_results(results, output_file)
    if not saved:
        print("⚠️ Results were not saved due to previous errors.")

    print("\n🏁 Done! All codes processed successfully.")


if __name__ == "__main__":
    main()
