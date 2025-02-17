import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import numpy as np
from scipy.stats import norm

# Download GBP/USD data for the past year
data = yf.download(tickers="GBPJPY=X", period="1mo", interval="1h")['Close']

# Calculate Z-Score
rolling_mean = data.rolling(20).mean()
rolling_std = data.rolling(20).std()
z_score = (data - rolling_mean) / rolling_std

# Signal strength function
def signal_strength(z):
    if z > 2.5:
        return "Strong Sell"
    elif 1.96 < z <= 2.5:
        return "Sell"
    elif -2.5 < z <= -1.96:
        return "Buy"
    elif z <= -2.5:
        return "Strong Buy"
    else:
        return "Hold"

# Pattern analysis function
def detect_pattern(z):
    if z > 1.96:
        return "Clustered"
    elif z < -1.96:
        return "Dispersed"
    else:
        return "Random"

# Calculate P-Value
def calculate_p_value(z):
    return 2 * (1 - norm.cdf(abs(z)))

# Calculate probability for the signal
def calculate_probability(z):
    return 1 - (0.5 * np.exp(-z ** 2 / 2))

# Get the last Z-Score value
last_z = z_score.iloc[-1]  # Last value in the series
last_z_value = last_z[-1]  # Extracting the individual last value

signal = signal_strength(last_z_value)  # Use the individual value
pattern = detect_pattern(last_z_value)  # Use the individual value
p_value = calculate_p_value(last_z_value)  # Use the individual value
probability = calculate_probability(last_z_value)  # Use the individual value

# Display results
print(f"Z-Score: {last_z_value:.2f}")
print(f"Signal: {signal}")
print(f"Pattern: {pattern}")
print(f"P-Value: {p_value:.4f}")
print(f"Probability of Signal: {probability:.2%}")

# Plot Z-Score with thresholds and patterns
plt.figure(figsize=(20, 10))
plt.plot(z_score, label="Z-Score", color="blue")
plt.axhline(1.96, color="red", linestyle="--", label="Clustered Threshold")
plt.axhline(-1.96, color="green", linestyle="--", label="Dispersed Threshold")
plt.axhline(2.5, color="red", linestyle="--", label="Clustered Threshold")
plt.axhline(-2.5, color="green", linestyle="--", label="Dispersed Threshold")
plt.axhline(0, color="black", linestyle="-", label="Neutral")
plt.title("Z-Score Analysis with Pattern Detection")
plt.xlabel("Date")
plt.ylabel("Z-Score")
plt.legend()

# Highlight the last data point
plt.scatter(z_score.index[-1], last_z_value, color="purple", label=f"Last Z-Score: {last_z_value:.2f}")
plt.legend()
plt.show()