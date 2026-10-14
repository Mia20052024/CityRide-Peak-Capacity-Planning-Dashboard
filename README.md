# CityRide Peak Capacity Planning Dashboard

> Screenshot placeholder: add a captured dashboard image here after running the app locally.

CityRide is a small Streamlit dashboard for shared-bike operations managers. It highlights when historical demand peaks under selected year, season, day-type, and weather conditions so teams can schedule rebalancing and maintenance before demand rises.

## Data

Source: [Kaggle Bike Sharing Dataset](https://www.kaggle.com/datasets/marklvl/bike-sharing-dataset). The dashboard uses `hour.csv`, an hourly historical snapshot covering 2011-01-01 through 2012-12-31. Each row represents one hour of aggregate bike-rental activity, with calendar, weather, and rider-count fields. It is historical—not live operational data—and `cnt` is used directly as the total ride count.

## User, decision, and action

The target user is a shared-bike operations manager. The dashboard supports decisions about when to position more vehicles and adjust maintenance capacity. If a manager finds that peak demand rises for a particular day type and weather condition, they should rebalance more vehicles and adjust maintenance shifts before the peak begins, reducing both unavailable bikes and idle vehicles.

An interactive dashboard is preferable to a one-time report or weekly email because managers can immediately compare the conditions relevant to the next operating day. The filters make the decision view reusable for a weekday commute, a holiday, or a weather-specific planning check.

## What is shown

- Three KPIs: total rides indicates the filtered scale; peak demand hour identifies the planning deadline; peak intensity shows how much that hour exceeds the filtered all-hour average.
- Two charts: the hourly demand profile is the primary view for timing rebalancing; demand by weather condition compares average demand under the selected weather categories.
- Filters: year, season, day type, and weather keep every KPI, chart, and recommendation tied to the same operating context.

Two things are deliberately omitted:

- A raw hourly data table, because it slows down rapid capacity decisions.
- Distribution charts for every weather variable, because they are useful for exploratory analysis but do not directly support daily dispatch action.

## Limitations and refresh strategy

This dataset has no station locations, live vehicle availability, maintenance status, or current demand. It therefore supports time-based capacity planning, not station-level dispatching. Historical averages can also mislead users when current events, service changes, or unusual weather make today different from 2011–2012.

In production, refresh the data every hour. Managers should review it each morning and conduct additional checks before holidays and severe weather. When expected demand for a time period is more than 20% above the average for comparable conditions, schedule additional vehicles.

## Run locally

From this folder:

```bash
uv run streamlit run app.py
```
