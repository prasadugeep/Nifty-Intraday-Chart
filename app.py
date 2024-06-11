from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objs as go

app = Flask(__name__)

# Read data from CSV file

df = pd.read_csv('../Project 1/export_dataframe.csv', parse_dates=['datetime'])
df.set_index('datetime', inplace=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visualize', methods=['POST'])
def visualize():
    selected_date = request.form['date']
    timeframe = request.form['timeframe']

    # Filter data based on selected date
    filtered_data = df[selected_date:selected_date]

    # Resample data based on selected timeframe
    if timeframe == '1min':
        resampled_data = filtered_data
    else:
        resampled_data = filtered_data.resample(timeframe).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})

    # Create candlestick chart
    fig = go.Figure(data=[go.Candlestick(x=resampled_data.index,
                    open=resampled_data['open'],
                    high=resampled_data['high'],
                    low=resampled_data['low'],
                    close=resampled_data['close'])])

    # Update layout for interactive features and add annotations
    fig.update_layout(
        title=f'Nifty Index {timeframe} Candlestick Chart - Date: {selected_date}',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
        annotations=[
            dict(
                x=1,
                y=1.03,
                xref='paper',
                yref='paper',
                text=f'Timeframe: {timeframe}',
                showarrow=False,
                bgcolor='rgba(255, 255, 255, 0.5)',
                bordercolor='rgba(255, 255, 255, 0.5)'
            )
        ]
    )

    return fig.to_json()

@app.route('/result')
def result():
    return render_template('result.html')

if __name__ == '__main__':
    app.run(debug=True)
