import pandas as pd
import json


def process_data(message: str) -> dict:
    """
    Processes the input data and performs time series analysis.

    Parameters
    ----------
    message : str
        Raw message body as a JSON string.

    Returns
    -------
    dict
        Processed data with analysis results.
    """
    try:
        data = json.loads(message)
        df = pd.DataFrame(data["prices"])

        # Example analysis: Simple moving average
        df["SMA"] = df["price"].rolling(window=5).mean()
        return {
            "symbol": data["symbol"],
            "analysis": df.to_dict(orient="records")
        }
    except Exception as e:
        return {"error": str(e)}
