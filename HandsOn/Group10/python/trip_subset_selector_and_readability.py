import numpy as np
import pandas as pd
from unicodedata import *

sample_ratio = 0.4

csv_dir = "path/to/csv/"

df_freeplaces = pd.read_csv(csv_dir + "df_free_places-with-links.csv")
df_stations = pd.read_csv(csv_dir + "df_stations-with-links.csv")

df_trips = pd.read_csv(csv_dir + "updated_dataset_trips.csv")

idx_samples = np.random.choice(df_trips.index.values, round(df_trips.shape[0] * sample_ratio), replace=False)
df_trips = df_trips.loc[idx_samples]

df_districts1 = df_freeplaces[['district', 'madrid_district_URI_from_wikidata']].drop_duplicates(keep='first')
df_districts2 = df_stations[['district', 'madrid_district_URI_from_wikidata']].drop_duplicates(keep='first')
df_merged_districts = pd.concat([df_districts1, df_districts2], ignore_index=True)
df_merged_districts = df_merged_districts.drop_duplicates(keep='first').dropna()




def custom_readability_transform(word):
    return word.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u').replace('ñ',
                                                                                                                  "n").replace(
        '\'', "-").replace('Á', "A").replace('Í', "I").replace('Ó', "O").replace('É', "E").replace('Ú', "U")


def trips_readable_creator(row):
    link_date = row['unlock_date'].replace(':', '-').replace(' ', '_')
    identifier = f"{row['id_Bike']}_at_{link_date}"
    return custom_readability_transform(identifier)


def lock_map(row):
    mappings = df_stations[df_stations['id_station'] == row['id_place_lock']]
    if len(mappings) == 0:
        mappings = df_freeplaces[df_freeplaces['id_free_place'] == row['id_place_lock']]
        return mappings['readable_id'].iloc[0]
    else:
        new_id = mappings['readable_id'].iloc[0]
        return new_id


def unlock_map(row):
    mappings = df_stations[df_stations['id_station'] == row['id_place_unlock']]
    if len(mappings) == 0:
        mappings = df_freeplaces[df_freeplaces['id_free_place'] == row['id_place_unlock']]
        return mappings['readable_id'].iloc[0]
    else:
        new_id = mappings['readable_id'].iloc[0]
        return new_id


def freeplace_readable_creator(row):
    identifier = f"{row['latitude']}_x_{row['longitude']}_at_{row['address'].title().replace(' ', '')}"
    return custom_readability_transform(identifier)


def stations_readable_creator(row):
    link_name = row['station_name'].title().replace(" ", "")
    return custom_readability_transform(link_name)


df_trips['readable_id'] = df_trips.apply(trips_readable_creator, axis=1)
df_stations['readable_id'] = df_stations.apply(stations_readable_creator, axis=1)
df_freeplaces['readable_id'] = df_freeplaces.apply(freeplace_readable_creator, axis=1)
df_merged_districts['readable_id'] = df_merged_districts.apply(lambda x: custom_readability_transform(x['district']), axis=1)
df_trips['id_place_lock'] = df_trips.apply(lock_map, axis=1)
df_trips['id_place_unlock'] = df_trips.apply(unlock_map, axis=1)

df_merged_districts.to_csv(csv_dir + "districts.csv", index=False)
df_freeplaces.to_csv(csv_dir + "readable_free_places.csv", index=False)
df_stations.to_csv(csv_dir + "readable_stations.csv", index=False)
df_trips.to_csv(csv_dir + "readable_trips.csv", index=False)
