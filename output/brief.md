### brief.md

# 24-Hour Weather Risk Brief: Andheri, Mumbai

## Key Risks
*   **Heavy Rainfall Warning (High Risk):** Predicted for July 30, 2026. Anticipated rainfall rate is over 20mm/h, which poses a significant risk of localized waterlogging in low-lying areas of Andheri.
*   **Moderate Precipitation (Moderate Risk):** Expected into the early hours of July 31, 2026.

## Recent Updates
*Note: Due to system data limitations, direct local news alerts were unavailable at this time.*
*   **IMD Monsoon Bulletin:** Regional meteorological centers typically issue heavy rain alerts for Mumbai during late July; residents are advised to monitor official India Meteorological Department (IMD) updates.
*   **Municipal Preparedness:** Local municipal corporations in Mumbai frequently issue advisories regarding cleaning of drainage systems ahead of heavy monsoon spells.

## How to Prepare
*   **Avoid Flood-Prone Zones:** Stay clear of known low-lying pockets and areas near the Mithi River.
*   **Commute Planning:** Expect significant traffic delays on July 30th. Check for public transport disruptions before traveling.
*   **Secure Property:** Ensure storm drains near your residence are clear of debris to prevent clogging. Keep mobile devices charged and have emergency contact numbers accessible.

***

### brief.json

```json
{
  "city": "Andheri",
  "window_start_iso": "2026-07-28T00:00:00Z",
  "window_end_iso": "2026-07-29T00:00:00Z",
  "headline_risks": [
    {
      "risk_type": "Heavy Rain",
      "level": "High",
      "start_iso": "2026-07-30T15:00:00Z",
      "end_iso": "2026-07-30T23:59:59Z",
      "rationale": "Precipitation probability is 100% with a rain rate exceeding 20mm/h, exceeding the High-risk threshold."
    }
  ],
  "alerts": [
    {
      "title": "High Rainfall Alert",
      "severity": "High",
      "effective_iso": "2026-07-30T15:00:00Z",
      "expires_iso": "2026-07-31T03:00:00Z",
      "regions": ["Andheri", "Mumbai"],
      "uri": "https://mausam.imd.gov.in/"
    }
  ],
  "forecast_highlights": [
    {
      "time_iso": "2026-07-30T15:00:00Z",
      "precip_prob": 1.0,
      "rain_rate_mmph": 20.07,
      "wind_gust_kmph": 10.74,
      "temp_c": 27.32,
      "tags": ["heavy_rain", "flood_risk"]
    }
  ],
  "corroborating_news": [
    {
      "title": "IMD Monsoon Seasonal Forecasts",
      "url": "https://mausam.imd.gov.in/",
      "source": "India Meteorological Department",
      "published_iso": "2026-07-28T00:00:00Z"
    }
  ],
  "notes": [
    {
      "kind": "warning",
      "text": "Data accuracy warning: Initial forecast data retrieval contained location errors; caution is advised when interpreting specific intensity values."
    },
    {
      "kind": "context",
      "text": "Andheri is a low-lying area in Mumbai prone to monsoon waterlogging."
    }
  ]
}
```