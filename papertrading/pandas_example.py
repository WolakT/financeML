import yfinance as yf

# Download minute data for the last 5 days for AAPL
data = yf.download("AAPL", period="5w", interval="1m")

# Save the data to a CSV file
data.to_csv("AAPL.csv")
