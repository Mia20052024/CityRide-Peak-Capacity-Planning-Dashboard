from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="CityRide Peak Capacity Planning Dashboard",
    page_icon="🚲",
    layout="wide",
)

NAVY = "#0F172A"
CYAN = "#22D3EE"
GREEN = "#34D399"
ORANGE = "#F59E0B"
PANEL = "#172033"
BORDER = "#27364D"

SEASON_MAP = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
WEATHER_MAP = {
    1: "Clear",
    2: "Mist / Cloudy",
    3: "Light Rain / Snow",
    4: "Heavy Rain / Snow",
}
DAY_TYPE_MAP = {1: "Working day", 0: "Weekend / Holiday"}
YEAR_MAP = {0: "2011", 1: "2012"}
DATA_PATH = Path(__file__).parent / "hour.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """Load the Kaggle hourly bike-sharing snapshot and readable labels."""
    data = pd.read_csv(path, parse_dates=["dteday"])
    data["season_label"] = data["season"].map(SEASON_MAP)
    data["weather_label"] = data["weathersit"].map(WEATHER_MAP)
    data["day_type_label"] = data["workingday"].map(DAY_TYPE_MAP)
    data["year_label"] = data["yr"].map(YEAR_MAP)
    return data


def reset_filters() -> None:
    for key in ("years", "seasons", "day_types", "weather"):
        st.session_state.pop(key, None)


def setup_chart(ax: plt.Axes) -> None:
    ax.set_facecolor(PANEL)
    ax.tick_params(colors="#CBD5E1", labelsize=10)
    for spine in ax.spines.values():
        spine.set_color(BORDER)
    ax.grid(axis="y", color="#334155", alpha=0.55, linewidth=0.8)
    ax.set_axisbelow(True)


st.markdown(
    f"""
    <style>
    .stApp {{ background: {NAVY}; color: #E2E8F0; }}
    [data-testid="stSidebar"] {{ background: #111C30; border-right: 1px solid {BORDER}; }}
    [data-testid="stSidebar"] * {{ color: #E2E8F0; }}
    .block-container {{ max-width: 1440px; padding-top: 2.2rem; padding-bottom: 2rem; }}
    h1, h2, h3 {{ color: #F8FAFC !important; letter-spacing: -0.02em; }}
    div[data-testid="stMetric"] {{ background: {PANEL}; border: 1px solid {BORDER}; border-radius: 14px; padding: 1rem 1.15rem; }}
    div[data-testid="stMetricLabel"] {{ color: #94A3B8; }}
    div[data-testid="stMetricValue"] {{ color: #F8FAFC; }}
    .eyebrow {{ color: {CYAN}; font-size: .78rem; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; }}
    .subtle {{ color: #94A3B8; font-size: .95rem; }}
    .recommendation {{ background: linear-gradient(110deg, #172033, #123042); border: 1px solid #26516A; border-left: 4px solid {GREEN}; border-radius: 14px; padding: 1.2rem 1.4rem; color: #E2E8F0; }}
    .recommendation h3 {{ margin: 0 0 .45rem 0; font-size: 1.05rem; }}
    .recommendation p {{ margin: 0; line-height: 1.55; }}
    </style>
    """,
    unsafe_allow_html=True,
)

if not DATA_PATH.exists():
    st.error("The required data file was not found at hour.csv.")
    st.stop()

df = load_data(str(DATA_PATH))

st.markdown('<div class="eyebrow">Operations command center</div>', unsafe_allow_html=True)
st.title("CityRide Peak Capacity Planning Dashboard")
st.markdown("For shared-bike operations managers: plan vehicle rebalancing and maintenance before demand peaks.")
st.markdown('<span class="subtle">Data: 2011–2012 Kaggle historical snapshot | Intended production refresh: hourly<br>Focus: when demand peaks, not station-level placement.</span>', unsafe_allow_html=True)

with st.sidebar:
    st.header("Planning filters")
    st.caption("Narrow the historical conditions used in every view.")
    if st.button("Reset filters", use_container_width=True):
        reset_filters()
        st.rerun()
    selected_years = st.multiselect("Year", list(YEAR_MAP.values()), default=list(YEAR_MAP.values()), key="years")
    selected_seasons = st.multiselect("Season", list(SEASON_MAP.values()), default=list(SEASON_MAP.values()), key="seasons")
    selected_day_types = st.multiselect("Day type", list(DAY_TYPE_MAP.values()), default=list(DAY_TYPE_MAP.values()), key="day_types")
    selected_weather = st.multiselect("Weather", list(WEATHER_MAP.values()), default=list(WEATHER_MAP.values()), key="weather")

filtered = df[df["year_label"].isin(selected_years) & df["season_label"].isin(selected_seasons) & df["day_type_label"].isin(selected_day_types) & df["weather_label"].isin(selected_weather)].copy()
if filtered.empty:
    st.info("No records match these filters. Please select at least one option in each filter.")
    st.stop()

hourly_average = filtered.groupby("hr")["cnt"].mean().reindex(range(24))
peak_hour = int(hourly_average.idxmax())
peak_avg = float(hourly_average.max())
all_hour_average = float(filtered["cnt"].mean())
intensity = ((peak_avg / all_hour_average) - 1) * 100 if all_hour_average else 0

kpi_1, kpi_2, kpi_3 = st.columns(3)
kpi_1.metric("Total rides", f"{filtered['cnt'].sum():,}")
kpi_2.metric("Peak demand hour", f"{peak_hour:02d}:00")
kpi_3.metric("Peak intensity", f"+{intensity:.0f}%")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Hourly demand profile")
st.caption("Average total rides by hour under the selected conditions.")
fig, ax = plt.subplots(figsize=(13, 5.6))
fig.patch.set_facecolor(NAVY)
setup_chart(ax)
line_colors = {"Working day": CYAN, "Weekend / Holiday": GREEN}
for day_type in selected_day_types:
    profile = filtered.loc[filtered["day_type_label"] == day_type].groupby("hr")["cnt"].mean().reindex(range(24))
    if profile.dropna().empty:
        continue
    color = line_colors[day_type]
    ax.plot(profile.index, profile.values, color=color, linewidth=2.8, marker="o", markersize=3.8, label=day_type)
    line_peak = int(profile.idxmax())
    line_peak_value = float(profile.max())
    ax.scatter(line_peak, line_peak_value, s=90, color=ORANGE, edgecolor="#F8FAFC", linewidth=0.8, zorder=4)
    ax.annotate(f"{line_peak:02d}:00", (line_peak, line_peak_value), xytext=(7, 12), textcoords="offset points", color="#F8FAFC", fontsize=10, fontweight="bold")
ax.set_xlim(-0.4, 23.4)
ax.set_xticks(range(24))
ax.set_xlabel("Hour of day", color="#CBD5E1", labelpad=10)
ax.set_ylabel("Average total rides", color="#CBD5E1", labelpad=10)
ax.legend(frameon=False, labelcolor="#E2E8F0", loc="upper left")
fig.tight_layout()
st.pyplot(fig, width="stretch")
plt.close(fig)

st.subheader("Demand by weather condition")
st.caption("Average total rides; bar colors provide visual separation only, not a risk rating.")
weather_average = filtered.groupby("weather_label")["cnt"].mean().sort_values()
fig, ax = plt.subplots(figsize=(13, 4.1))
fig.patch.set_facecolor(NAVY)
setup_chart(ax)
bar_colors = [CYAN, "#4FD1C5", GREEN, ORANGE][-len(weather_average):]
bars = ax.barh(weather_average.index, weather_average.values, color=bar_colors, height=0.58)
ax.set_xlabel("Average total rides", color="#CBD5E1", labelpad=10)
ax.set_ylabel("")
for bar, value in zip(bars, weather_average.values):
    ax.text(value, bar.get_y() + bar.get_height() / 2, f"  {value:,.0f}", va="center", color="#E2E8F0", fontsize=10)
ax.margins(x=0.12)
fig.tight_layout()
st.pyplot(fig, width="stretch")
plt.close(fig)

audience_note = ""
if selected_day_types == ["Working day"]:
    audience_note = " The selected pattern is commute-oriented, so align vehicle availability and maintenance coverage with commuter flows."
elif selected_day_types == ["Weekend / Holiday"]:
    audience_note = " The selected pattern is leisure-oriented, so align vehicle availability and maintenance coverage with recreational travel patterns."
weather_note = ""
if selected_weather and selected_weather != ["Clear"]:
    weather_note = " Because non-clear weather is included, adjust capacity using the corresponding historical demand rather than assuming clear-weather volumes."
st.markdown(f'''<div class="recommendation"><h3>Operational recommendation</h3><p>Demand is highest at <strong>{peak_hour:02d}:00</strong> for the selected conditions. Complete vehicle rebalancing 60–90 minutes before this peak, and shift maintenance work outside the peak window to protect availability.{audience_note}{weather_note}</p></div>''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Limitations: This historical dataset does not include station locations, live vehicle availability, maintenance status, or current demand. It supports time-based capacity planning, not station-level dispatching.")
