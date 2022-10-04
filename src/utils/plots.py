import pandas as pd
import os 
import numpy as np
import requests
import plotly.graph_objs as go

fred_apikey = os.environ.get('FRED_API_KEY')

# TODO add buffett indicator plot

# Add alphavantage real time data
# http://mattdturner.com/wordpress/2018/08/create-a-buffett-indicator-plot-in-python/
def get_observations(series_id='GDP', observation_start="2000-01-01")-> pd.DataFrame:
  """
  Returns Pandas Dataframe containing gdp data
  """
  # Url of interest is 
  fred_url = "https://api.stlouisfed.org/fred/series/observations"
  payload = {
    'series_id': series_id,
    "observation_start": observation_start,
    "file_type": "json",
    "api_key": fred_apikey
  }
  r = requests.get(fred_url, params=payload)
  response = r.json()
  observations = pd.DataFrame(response["observations"])
  # drop columns that are not of interest
  observations = observations.drop(['realtime_start', 'realtime_end'], axis=1)
  observations = observations.replace('.', np.nan)
  # convert value column to number
  observations["value"] = pd.to_numeric(observations["value"])
  observations['date'] = observations['date'].astype('datetime64[ns]') 
  observations = observations.rename(columns={'value': series_id})
  # drop duplicates based on date
  observations = observations.drop_duplicates(subset ="date", keep = False)
  return observations

def make_buffett_indicator(start_time='2000-01-01'):
  gdp = get_observations("GDP", start_time)
  wilshire = get_observations("WILL5000PR", start_time)
  # concats based on date
  combined = pd.merge(gdp, wilshire, on='date', how='outer')
  combined = combined.set_index('date')
  combined = combined.sort_index()
  # resort the index
  combined = combined.fillna(method='ffill')
  # Calculate Buffett indicator
  combined['Buffett_Indicator'] = combined.WILL5000PR / combined.GDP * 100
  # Get the starting and ending date
  min_date = combined.index.to_pydatetime()[0]
  max_date = combined.index.to_pydatetime()[-1]
  num_dates = len(combined.index.to_pydatetime())
  quarter_date = combined.index.to_pydatetime()[int(num_dates/4)]
  three_quarter_date = combined.index.to_pydatetime()[int(3*num_dates/4)]
  # horizontal line
  shapes=[
    go.layout.Shape(
      type="line",
      x0=min_date,
      y0=100,
      x1=max_date,
      y1=100,
      line=dict(
          color="red",
          width=4,
          dash="dashdot",
      )
    ),
    go.layout.Shape(
      # Line Horizontal
      type="line",
      x0=min_date,
      y0=80,
      x1=max_date,
      y1=80,
      line=dict(
          color="green",
          width=4,
          dash="dashdot",
      )
    ),
  ]
  layout = go.Layout(shapes=shapes, xaxis = dict(
      range=(min_date, max_date),
      tickformat='%Y-%m-%d',
      title='Buffett Indicator'
    )
  )
  fig = go.Figure(layout=layout)
  fig.add_trace(go.Scatter(
      x=combined.index.to_pydatetime(),
      y=combined.Buffett_Indicator,
      name="Buffett Indicator"
  ))

  # Create scatter trace of text labels
  fig.add_trace(go.Scatter(
      x=[ quarter_date, three_quarter_date],
      y=[ 70, 110],
      text=["Undervalued",
            "Overvalued"],
      name="Labels",
      mode="text",
  ))

  # return dcc.Graph(
  #     id='buffett',
  #     figure=fig
  # )
  return fig


