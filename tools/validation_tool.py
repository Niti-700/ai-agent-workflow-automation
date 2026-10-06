def validate_required_columns(df, required_columns):
    """
    Check whether all required columns exist in the dataframe.
    """

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    return missing_columns


def find_missing_values(df, required_columns):
    """
    Find rows where required fields are missing.
    """

    missing_rows = df[df[required_columns].isnull().any(axis=1)]

    return missing_rows