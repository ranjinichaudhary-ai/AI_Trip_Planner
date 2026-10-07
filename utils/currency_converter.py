import requests

class CurrencyConverter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def convert(self, amount: float,from_currency: str, to_currency: str):
        """Convert the amount from one currency to another"""
        if not self.api_key:
            raise ValueError("EXCHANGE_RATE_API_KEY is not set.")

        url = f"{self.base_url}/{self.api_key}/latest/{from_currency}"
        response = requests.get(url)
        response.raise_for_status()
        try:
            data = response.json()
        except ValueError as exc:
            raise ValueError(
                f"ExchangeRate-API returned invalid JSON (HTTP {response.status_code})."
            ) from exc

        if data.get("result") != "success":
            raise ValueError(f"ExchangeRate-API request failed: {data.get('error-type', 'unknown error')}.")

        rates = data["conversion_rates"]
        if to_currency not in rates:
            raise ValueError(f"{to_currency} not found in exchange rates.")
        return amount * rates[to_currency]