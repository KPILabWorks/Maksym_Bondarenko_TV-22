import pandas as pd
import json
import inquirer

# Load the JSON file
file_path = "openaq.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)
df = pd.json_normalize(data)

# Filter columns and set index
df = df[["country_name_en","city", "location", "measurements_parameter", "measurements_value", "measurements_lastupdated"]]
df["measurements_lastupdated"] = pd.to_datetime(df["measurements_lastupdated"], utc=True)

# Extract indexed field values
pollutants = df["measurements_parameter"].unique().tolist()
countries = df["country_name_en"].unique().tolist()

# Set indexes
df.set_index(["country_name_en", "measurements_parameter"], inplace=True)
df.to_csv("results/Dataset.csv")

# Prompt user
while True:
    questions = [
        inquirer.List(
            "pollutant",
            message="Select a pollutant to search by",
            choices=['Skip', 'Exit', *pollutants],
        ),
        inquirer.List(
            "country",
            message="Select a country to search by",
            choices=['Skip', 'Exit', *countries],
        )
    ]
    answers = inquirer.prompt(questions)
    selected_pollutant = answers["pollutant"]
    selected_country = answers["country"]

    if selected_pollutant == 'Exit' or selected_country == 'Exit': exit(0)

    # Search
    if selected_country != 'Skip' and selected_pollutant != 'Skip':
        result = df.xs((selected_country, selected_pollutant), level=("country_name_en","measurements_parameter"))
    elif selected_pollutant != 'Skip':
        result = df.xs(selected_pollutant, level="measurements_parameter")
    elif selected_country != 'Skip':
        result = df.xs(selected_country, level="country_name_en")
    else: continue

    result.to_csv("results/search_result.csv")
    print("Search results stored to results folder")
