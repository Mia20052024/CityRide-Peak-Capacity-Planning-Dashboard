# CityRide Peak Capacity Planning Dashboard | Team 4

CityRide is a Streamlit dashboard for shared-bike operations managers. It shows when historical demand peaks under selected year, season, day type, and weather conditions, helping teams schedule vehicle rebalancing and maintenance before demand rises.

> Screenshot placeholder: add a screenshot of the deployed dashboard here before submitting.

## Data

Source: [Kaggle Bike Sharing Dataset](https://www.kaggle.com/datasets/marklvl/bike-sharing-dataset)

The dashboard uses `hour.csv`, an hourly historical snapshot covering January 1, 2011 through December 31, 2012. Each row represents one hour of aggregate Capital Bikeshare rental activity in Washington, D.C., with calendar, weather, and rider-count fields.

This is real historical data from the Capital Bikeshare system, not synthetic data. It is not live operational data. The dashboard uses `cnt` directly as the total ride count.

## User, Decision, and Action

The target user is a shared-bike operations manager.

The dashboard supports decisions about when to position more vehicles and adjust maintenance capacity. If a manager finds that peak demand rises for a particular day type and weather condition, they should rebalance more vehicles and adjust maintenance shifts before the peak begins. This reduces unavailable bikes during high-demand periods and avoids unnecessary vehicle movement when demand is low.

Without this dashboard, the operations manager would need to manually combine hourly trip records, weather forecasts, and past demand patterns in spreadsheets. This process is slower and makes it easier to miss a coming peak. Missing a peak can lead to unavailable bikes, dissatisfied customers, and inefficient staff or vehicle allocation.

An interactive dashboard is better than a one-time report or weekly email because the manager needs to repeatedly compare the conditions relevant to the next operating day. The filters make the view reusable for a weekday commute, a holiday, a specific season, or a weather-related planning check.

## What Is Shown

The dashboard has three headline KPIs:

- **Total rides:** shows the overall volume of demand under the selected conditions.
- **Peak demand hour:** identifies the hour when operations should be prepared.
- **Peak intensity:** shows how much the peak hour exceeds the filtered all-hour average.

The dashboard has two supporting charts:

- **Hourly demand profile:** the primary chart, showing the average total ride count by hour. It helps managers identify when to complete vehicle rebalancing.
- **Demand by weather condition:** compares average ride demand under selected weather categories and explains why demand changes.

The dashboard has four filters:

- Year
- Season
- Day type: Working day or Weekend/Holiday
- Weather condition

These filters ensure that every KPI, chart, and recommendation refers to the same operating context.

## What Is Not Shown

Two things are intentionally excluded:

- **Raw hourly data table:** it contains too much detail for a manager making a fast capacity decision.
- **Distribution charts for every weather variable:** they are useful during exploratory data analysis, but they do not directly support daily vehicle-dispatch decisions.

## Dashboard Order

The page is ordered from most important to least important:

1. Headline KPIs answer: “When is the demand peak, and how large is it?”
2. The hourly demand chart explains when demand rises during the day.
3. The weather chart explains how weather conditions affect demand.
4. The operational recommendation turns the selected results into a suggested action.

## Limitations and Potentially Misleading Data

This dataset is a historical snapshot from 2011–2012. It does not include station locations, live vehicle availability, maintenance status, current demand, service changes, special events, or current weather forecasts.

Therefore, the dashboard supports time-based capacity planning, but it cannot decide exactly which station should receive vehicles. Historical averages may also mislead users when unusual weather or current events make today different from the historical period.

The dashboard displays the data period clearly so users understand that this is a Kaggle historical snapshot rather than live operations data.

## Refresh and Review Strategy

In a real production environment, operational data should refresh every hour because bike availability and ride demand can change throughout the day.

The operations manager should review the dashboard every morning and conduct additional checks before holidays and severe weather. The data refresh frequency and review frequency are different: data can update hourly, while the manager may only need to make formal planning decisions once per day.

If expected demand for a time period is more than 20% above the average demand for comparable conditions, the manager should schedule additional vehicles and consider adjusting maintenance shifts before the peak begins.

Stale data can lead to vehicle shortages during busy periods or unnecessary rebalancing when demand is lower than expected.

## Run Locally

From this project folder, run:

```bash
uv run streamlit run app.py
