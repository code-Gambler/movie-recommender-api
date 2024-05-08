import os
from ydata_profiling import ProfileReport
import pandas as pd

def report_generation(files, names, output):
    """Generates data profiling reports for multiple CSV files.

    This function iterates through a list of file paths, corresponding list of report names,
    and a list of output paths. For each file, it reads the CSV data into a pandas DataFrame,
    creates a data profiling report using the ydata_profiling library, and saves the report
    to the specified output path.

    Args:
        files: A list of file paths for the CSV files to generate reports for.
        names: A list of names to use as titles for the generated reports.
        output: A list of file paths for the output reports (Markdown or HTML).
    """
    for i in range(3):
        df = pd.read_csv(files[i])
        # Generate the data profiling report
        report = ProfileReport(df, title=names[i])
        report.to_file(output[i])

def generate_report():
    """Generates data profiling reports for the movie recommendation dataset.

    This function defines file paths for the ratings, movies, and links CSV files,
    corresponding names for the reports, and output paths for the generated reports (HTML).
    It then calls the `report_generation` function to create reports for each file.
    """
    files = ["recommend-logic/data-set/data/ratings.csv", "recommend-logic/data-set/data/movies.csv", "recommend-logic/data-set/data/links.csv"]
    files_output = ["recommend-logic/data-set/reports/ratings.md", "recommend-logic/data-set/reports/movies.html", "recommend-logic/data-set/reports/links.html"]
    names = ["Ratings", "Movies", "Links"]
    report_generation(files, names, files_output)