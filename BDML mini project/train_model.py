import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def generate_stock_data(filepath='stock_data.csv', num_days=500):
    """Generate realistic historical time series stock price data if not present."""
    if os.path.exists(filepath):
        print(f"[*] Found existing dataset at '{filepath}'")
        return pd.read_csv(filepath)

    print(f"[*] Generating realistic time series stock dataset ({num_days} trading days)...")
    np.random.seed(42)
    start_date = pd.to_datetime('2023-01-01')
    dates = pd.bdate_range(start=start_date, periods=num_days)

    initial_price = 1500.0  # Initial stock price in INR
    daily_returns = np.random.normal(0.0005, 0.018, num_days)
    close_prices = [initial_price]
    for r in daily_returns[1:]:
        close_prices.append(close_prices[-1] * (1 + r))

    close_prices = np.array(close_prices)

    # Generate correlated Open, High, Low, Volume based on Close
    open_prices = close_prices * (1 + np.random.normal(0, 0.006, num_days))
    high_prices = np.maximum(open_prices, close_prices) * (1 + np.abs(np.random.normal(0.004, 0.005, num_days)))
    low_prices = np.minimum(open_prices, close_prices) * (1 - np.abs(np.random.normal(0.004, 0.005, num_days)))
    volumes = np.random.randint(100000, 2500000, size=num_days)

    df = pd.DataFrame({
        'Date': dates.strftime('%Y-%m-%d'),
        'Open': np.round(open_prices, 2),
        'High': np.round(high_prices, 2),
        'Low': np.round(low_prices, 2),
        'Close': np.round(close_prices, 2),
        'Volume': volumes
    })

    df.to_csv(filepath, index=False)
    print(f"[OK] Saved stock dataset to '{filepath}'")
    return df

def train_and_evaluate():
    print("=" * 60)
    print("EXP 9: TIME SERIES-BASED STOCK PRICE FORECASTING")
    print("WITH LINEAR REGRESSION")
    print("=" * 60)

    # 1. Data Collection
    csv_file = 'stock_data.csv'
    df = generate_stock_data(csv_file)
    print("\n--- 1. First 5 Rows of Historical Stock Data ---")
    print(df.head())

    # 2. Data Preprocessing
    print("\n--- 2. Data Preprocessing ---")
    df['Date'] = pd.to_datetime(df['Date'])
    initial_len = len(df)
    df.dropna(inplace=True)
    df.sort_values(by='Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    print(f"Total rows after cleaning missing values: {len(df)} (removed {initial_len - len(df)})")
    print(f"Date range: {df['Date'].min().strftime('%Y-%m-%d')} to {df['Date'].max().strftime('%Y-%m-%d')}")

    # 3. Feature Selection
    features = ['Open', 'High', 'Low', 'Volume']
    target = 'Close'
    X = df[features]
    y = df[target]
    print(f"\n--- 3. Selected Features: {features} | Target: '{target}' ---")

    # 4. Train-Test Split (Chronological 80%-20% for Time Series)
    train_size = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]
    test_dates = df['Date'].iloc[train_size:]

    print(f"\n--- 4. Train-Test Split ---")
    print(f"Training set size: {X_train.shape[0]} samples (80%)")
    print(f"Testing set size:  {X_test.shape[0]} samples (20%)")

    # 5. Model Training
    print(f"\n--- 5. Training Linear Regression Model ---")
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("Model Coefficients:")
    for feature_name, coef in zip(features, model.coef_):
        print(f"  {feature_name}: {coef:.6f}")
    print(f"Intercept: {model.intercept_:.6f}")

    # 6. Prediction
    y_pred = model.predict(X_test)

    # 7. Evaluation
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("\n--- 6. Evaluation Metrics ---")
    print(f"Mean Squared Error (MSE):       {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE):  {rmse:.4f}")
    print(f"R² Score:                        {r2:.4f} ({r2 * 100:.2f}%)")

    # Sample Predictions
    comparison_df = pd.DataFrame({
        'Date': test_dates.dt.strftime('%Y-%m-%d').values,
        'Actual Close': y_test.values,
        'Predicted Close': np.round(y_pred, 2),
        'Difference': np.round(y_test.values - y_pred, 2)
    })
    print("\n--- Sample Test Predictions (First 5 Rows) ---")
    print(comparison_df.head())

    # 8. Visualization with Professional Dark Fintech Theme
    os.makedirs('static/image', exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0b0f19')
    ax.set_facecolor('#111827')
    
    ax.plot(test_dates.values, y_test.values, label='Actual Close Price', color='#06b6d4', linewidth=2.5)
    ax.plot(test_dates.values, y_pred, label='Predicted Close (Linear Regression)', color='#f43f5e', linestyle='--', linewidth=2.5)
    
    ax.set_title('Stock Price Forecasting: Actual vs Predicted Trends', fontsize=14, fontweight='bold', color='#f8fafc', pad=15)
    ax.set_xlabel('Trading Date', fontsize=12, color='#94a3b8', labelpad=10)
    ax.set_ylabel('Stock Price (INR)', fontsize=12, color='#94a3b8', labelpad=10)
    
    ax.tick_params(colors='#94a3b8', labelsize=10)
    for spine in ax.spines.values():
        spine.set_color('#334155')
        
    ax.grid(True, linestyle=':', alpha=0.3, color='#64748b')
    leg = ax.legend(loc='upper left', fontsize=11, facecolor='#0f172a', edgecolor='#334155')
    for text in leg.get_texts():
        text.set_color('#f8fafc')
        
    plt.tight_layout()

    chart_path = 'actual_vs_predicted.png'
    static_chart_path = os.path.join('static', 'image', 'stock_chart.png')
    plt.savefig(chart_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.savefig(static_chart_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close()
    print(f"\n--- 7. Visualization saved to '{chart_path}' and '{static_chart_path}' ---")

    # Save trained model
    model_filename = 'model.pkl'
    joblib.dump(model, model_filename)
    print(f"--- 8. Trained model exported successfully to '{model_filename}' ---")
    print("\n[OK] Training and evaluation complete!")

    return mse, rmse, r2

if __name__ == '__main__':
    train_and_evaluate()
