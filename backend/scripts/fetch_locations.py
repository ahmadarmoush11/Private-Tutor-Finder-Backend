import argparse
import io
import json
import math
import sys
import urllib.request
import zipfile
from pathlib import Path

COUNTRY_CODE = "LB"
GEONAMES_URL = f"https://download.geonames.org/export/dump/{COUNTRY_CODE}.zip"
DISTRICT_BOUNDARIES_URL = (
    "https://media.githubusercontent.com/media/wmgeolab/geoBoundaries/main/"
    "releaseData/gbOpen/LBN/ADM2/geoBoundaries-LBN-ADM2_simplified.geojson"
)

BACKEND_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BACKEND_DIR / "data" / "locations"
RAW_DIR = OUTPUT_DIR / "raw"
OUTPUT_FILE = OUTPUT_DIR / "lebanon_locations.json"

PLACES_FILE = f"{COUNTRY_CODE}.zip"
DISTRICTS_FILE = "geoBoundaries-LBN-ADM2_simplified.geojson"

EXCLUDED_FEATURE_CODES = {"PPLH", "PPLQ", "PPLW", "PPLCH"}
MAX_SNAP_DISTANCE_KM = 5

DISTRICTS = {
    "Akkar": ("Akkar", "Akkar"),
    "Baalbek": ("Baalbek", "Baalbek-Hermel"),
    "Hermel": ("Hermel", "Baalbek-Hermel"),
    "Beirut": ("Beirut", "Beirut"),
    "Zahle": ("Zahle", "Bekaa"),
    "West Bekaa": ("West Bekaa", "Bekaa"),
    "Rachaya": ("Rashaya", "Bekaa"),
    "Kesrouan": ("Keserwan", "Keserwan-Jbeil"),
    "Jbail": ("Jbeil", "Keserwan-Jbeil"),
    "Aley": ("Aley", "Mount Lebanon"),
    "Baabda": ("Baabda", "Mount Lebanon"),
    "Chouf": ("Chouf", "Mount Lebanon"),
    "El Metn": ("Metn", "Mount Lebanon"),
    "Batroun": ("Batroun", "North Lebanon"),
    "Bcharre": ("Bsharri", "North Lebanon"),
    "Koura": ("Koura", "North Lebanon"),
    "Minieh-Dinnieh": ("Minieh-Danniyeh", "North Lebanon"),
    "Tripoli": ("Tripoli", "North Lebanon"),
    "Zgharta": ("Zgharta", "North Lebanon"),
    "Saida": ("Saida", "South Lebanon"),
    "Sour": ("Tyre", "South Lebanon"),
    "Jezzine": ("Jezzine", "South Lebanon"),
    "Nabatiye": ("Nabatieh", "Nabatieh"),
    "Bent Jbail": ("Bint Jbeil", "Nabatieh"),
    "Hasbaya": ("Hasbaya", "Nabatieh"),
    "Marjaayoun": ("Marjayoun", "Nabatieh"),
}


def download(url: str, file_name: str, refresh: bool) -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    target = RAW_DIR / file_name
    if target.exists() and not refresh:
        print(f"Using cached {target.relative_to(BACKEND_DIR)}")
        return target

    print(f"Downloading {url} ...")
    request = urllib.request.Request(url, headers={"User-Agent": "private-tutor-finder/1.0"})
    with urllib.request.urlopen(request, timeout=120) as response:
        target.write_bytes(response.read())
    print(f"Saved {target.relative_to(BACKEND_DIR)} ({target.stat().st_size // 1024} KB)")
    return target


def read_places(path: Path) -> list[tuple[str, float, float]]:
    places = []
    with zipfile.ZipFile(path) as archive:
        with archive.open(f"{COUNTRY_CODE}.txt") as raw:
            for line in io.TextIOWrapper(raw, encoding="utf-8"):
                columns = line.rstrip("\n").split("\t")
                if len(columns) < 8:
                    continue
                feature_class, feature_code = columns[6], columns[7]
                if feature_class != "P" or feature_code in EXCLUDED_FEATURE_CODES:
                    continue
                places.append((columns[1].strip(), float(columns[4]), float(columns[5])))
    return places


def read_districts(path: Path) -> list[tuple[str, list[list[list[float]]]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    districts = []
    for feature in data["features"]:
        name = feature["properties"]["shapeName"]
        if name not in DISTRICTS:
            raise ValueError(f"Unknown district in boundary file: {name}")
        geometry = feature["geometry"]
        polygons = (
            [geometry["coordinates"]]
            if geometry["type"] == "Polygon"
            else geometry["coordinates"]
        )
        rings = [ring for polygon in polygons for ring in polygon]
        districts.append((name, rings))
    return districts


def point_in_rings(longitude: float, latitude: float, rings: list[list[list[float]]]) -> bool:
    inside = False
    for ring in rings:
        previous_x, previous_y = ring[-1][0], ring[-1][1]
        for x, y in ((point[0], point[1]) for point in ring):
            if (y > latitude) != (previous_y > latitude):
                crossing_x = previous_x + (latitude - previous_y) * (x - previous_x) / (y - previous_y)
                if longitude < crossing_x:
                    inside = not inside
            previous_x, previous_y = x, y
    return inside


def distance_km(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    phi_1, phi_2 = math.radians(latitude_1), math.radians(latitude_2)
    delta_phi = phi_2 - phi_1
    delta_lambda = math.radians(longitude_2 - longitude_1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(a))


def find_district(latitude: float, longitude: float, districts) -> str | None:
    for name, rings in districts:
        if point_in_rings(longitude, latitude, rings):
            return name

    nearest_name, nearest_distance = None, float("inf")
    for name, rings in districts:
        for ring in rings:
            for x, y in ((point[0], point[1]) for point in ring):
                distance = distance_km(latitude, longitude, y, x)
                if distance < nearest_distance:
                    nearest_name, nearest_distance = name, distance
    if nearest_distance <= MAX_SNAP_DISTANCE_KM:
        return nearest_name
    return None


def build_locations(places, districts) -> tuple[list[dict], list[str]]:
    locations = {}
    unmatched = []
    for name, latitude, longitude in places:
        district_key = find_district(latitude, longitude, districts)
        if district_key is None:
            unmatched.append(name)
            continue
        district, governorate = DISTRICTS[district_key]
        key = (name.lower(), district.lower())
        locations.setdefault(
            key,
            {
                "name": name,
                "district": district,
                "governorate": governorate,
                "latitude": round(latitude, 5),
                "longitude": round(longitude, 5),
            },
        )

    ordered = sorted(
        locations.values(),
        key=lambda row: (row["governorate"], row["district"], row["name"]),
    )
    return ordered, unmatched


def write_json(locations: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as file:
        json.dump(locations, file, ensure_ascii=False, indent=2)
        file.write("\n")


def print_summary(locations: list[dict], unmatched: list[str]) -> None:
    print()
    print(f"Wrote {len(locations)} locations to {OUTPUT_FILE.relative_to(BACKEND_DIR)}")
    print(f"Skipped {len(unmatched)} places outside Lebanon's districts", end="")
    print(f": {', '.join(unmatched[:10])}" if unmatched else "")

    per_governorate = {}
    for row in locations:
        districts = per_governorate.setdefault(row["governorate"], {})
        districts[row["district"]] = districts.get(row["district"], 0) + 1
    for governorate, districts in sorted(per_governorate.items()):
        print(f"  {governorate} ({sum(districts.values())})")
        for district, count in sorted(districts.items()):
            print(f"    {district}: {count}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Build data/locations/lebanon_locations.json from GeoNames places and geoBoundaries districts"
    )
    parser.add_argument(
        "--refresh",
        action="store_true",
        help="download the files again even if they are already in data/locations/raw",
    )
    args = parser.parse_args()

    try:
        places_path = download(GEONAMES_URL, PLACES_FILE, args.refresh)
        districts_path = download(DISTRICT_BOUNDARIES_URL, DISTRICTS_FILE, args.refresh)
    except OSError as error:
        print(f"Download failed: {error}", file=sys.stderr)
        print(
            f"You can download these files manually into {RAW_DIR} and run the script again:\n"
            f"  {GEONAMES_URL}\n  {DISTRICT_BOUNDARIES_URL}",
            file=sys.stderr,
        )
        return 1

    locations, unmatched = build_locations(read_places(places_path), read_districts(districts_path))
    write_json(locations)
    print_summary(locations, unmatched)
    return 0


if __name__ == "__main__":
    sys.exit(main())
