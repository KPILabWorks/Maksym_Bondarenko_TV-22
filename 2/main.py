import pandas as pd
import json

# Load the JSON file
file_path = "openaq.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)
df = pd.json_normalize(data)

# Filter columns and set index
df = df[["country_name_en","city", "location", "measurements_parameter", "measurements_value", "measurements_lastupdated"]]
df["measurements_lastupdated"] = pd.to_datetime(df["measurements_lastupdated"], utc=True)
df.set_index(["country_name_en", "measurements_parameter"], inplace=True)
df.to_csv("results/Dataset.csv")

# Queries using xs
country_data = df.xs("India", level="country_name_en")
country_data.to_csv("results/India.csv")
print("Stored query result")

polutant_data = df.xs("CO", level="measurements_parameter")
polutant_data.to_csv("results/CO.csv")
print("Stored query result")

composite_data = df.xs(("India", "CO"), level=("country_name_en", "measurements_parameter"))
composite_data.to_csv("results/India_CO.csv")
print("Stored query result")
