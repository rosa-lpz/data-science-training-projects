DATA_DIR = "/home/rlz-98/Documents/GitHub/Data-Science-Portfolio/Predictive Maintenance/MA_predictive_maintenance/data/raw/"


# List of file names and corresponding DataFrames
files_names = [
    ("PdM_telemetry.csv", "df_telemetry"),
    ("PdM_errors.csv", "df_errors"),
    ("PdM_machines.csv", "df_machines"),
    ("PdM_maint.csv", "df_maint"),
    ("PdM_failures.csv", "df_failures")
]

files = ["PdM_telemetry.csv", "PdM_errors.csv", "PdM_machines.csv", "PdM_maint.csv","PdM_failures.csv"]
df_names= ["df_telemetry","df_errors", "df_machines", "df_maint", "df_failures"] 