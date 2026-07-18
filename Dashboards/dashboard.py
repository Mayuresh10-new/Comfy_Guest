import pandas as pd
import streamlit as st
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

import mqtt_handler

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Hotel Automation Dashboard",
    page_icon="🏨",
    layout="wide"
)

# ---------------------------------------------------
# Custom Styling
# ---------------------------------------------------

st.markdown(
    """
    <style>
    /* Overall background */
    .stApp {
        background: linear-gradient(180deg, #0f1117 0%, #171a23 100%);
    }

    /* Hide default streamlit chrome */
    #MainMenu, footer, header {visibility: hidden;}

    /* Reclaim the space Streamlit reserves for its hidden header */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Title block */
    .dashboard-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.25rem 1.75rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #1e2130 0%, #2a2f45 100%);
        border: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.5rem;
    }
    .dashboard-header h1 {
        font-size: 1.8rem;
        margin: 0;
        color: #f5f5f7;
        font-weight: 700;
    }
    .dashboard-header p {
        margin: 0.15rem 0 0 0;
        color: #9aa0b4;
        font-size: 0.9rem;
    }

    /* Status pill */
    .status-pill {
        padding: 0.4rem 1rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
    }
    .status-online {
        background: rgba(46, 204, 113, 0.15);
        color: #2ecc71;
        border: 1px solid rgba(46, 204, 113, 0.35);
    }
    .status-offline {
        background: rgba(231, 76, 60, 0.15);
        color: #e74c3c;
        border: 1px solid rgba(231, 76, 60, 0.35);
    }

    /* Sensor cards */
    .sensor-card {
        background: linear-gradient(160deg, #1c2030 0%, #23283a 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.1rem 1.2rem;
        height: 100%;
        margin-bottom: 1.1rem;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    .sensor-card:hover {
        transform: translateY(-2px);
        border-color: rgba(120,140,255,0.35);
    }
    .sensor-icon {
        font-size: 1.6rem;
        margin-bottom: 0.4rem;
    }
    .sensor-label {
        color: #9aa0b4;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 0.2rem;
    }
    .sensor-value {
        color: #f5f5f7;
        font-size: 1.6rem;
        font-weight: 700;
    }

    .footer-note {
        color: #6b7086;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 2rem;
    }

    /* Manual override panel */
    .override-panel {
        background: linear-gradient(160deg, #1c2030 0%, #23283a 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        margin-bottom: 1.5rem;
    }
    .mode-badge {
        padding: 0.3rem 0.9rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.8rem;
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
    }
    .mode-manual {
        background: rgba(241, 196, 15, 0.15);
        color: #f1c40f;
        border: 1px solid rgba(241, 196, 15, 0.35);
    }
    .mode-auto {
        background: rgba(52, 152, 219, 0.15);
        color: #3498db;
        border: 1px solid rgba(52, 152, 219, 0.35);
    }

    /* Actuator status cards */
    .actuator-card {
        background: linear-gradient(160deg, #1c2030 0%, #23283a 100%);
        border: 1px solid rgba(255,255,255,0.06);
        border-radius: 14px;
        padding: 1rem 1.1rem;
        height: 100%;
        margin-bottom: 1.1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .actuator-icon {
        font-size: 1.5rem;
    }
    .actuator-label {
        color: #9aa0b4;
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.03em;
        margin-bottom: 0.15rem;
    }
    .actuator-state {
        font-size: 1rem;
        font-weight: 700;
    }
    .actuator-on {
        color: #2ecc71;
    }
    .actuator-off {
        color: #6b7086;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Start MQTT only once
# ---------------------------------------------------

if "mqtt_started" not in st.session_state:
    mqtt_handler.start()
    st.session_state.mqtt_started = True

# ---------------------------------------------------
# Refresh every 2 seconds
# ---------------------------------------------------

st_autorefresh(interval=2000, key="mqtt_refresh")

# ---------------------------------------------------
# Header with live status pill
# ---------------------------------------------------

is_connected = mqtt_handler.connected
status_class = "status-online" if is_connected else "status-offline"
status_dot = "🟢" if is_connected else "🔴"
status_text = "Connected to HiveMQ" if is_connected else "Not Connected"

st.markdown(
    f"""
    <div class="dashboard-header">
        <div>
            <h1>🏨 Hotel Automation Dashboard</h1>
            <p>Live sensor feed from Raspberry Pi + GrovePi</p>
        </div>
        <div class="status-pill {status_class}">{status_dot} {status_text}</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# Manual Override Panel
# ---------------------------------------------------

current_manual_mode = bool(mqtt_handler.latest_data.get("manual_mode", False))

ACTUATOR_CONTROLS = [
    ("relay", "Air Purifier", "🌬️"),
    ("room_led", "Air Conditioner", "❄️"),
    ("status_led", "Blinders", "🪟"),
    ("new_led", "Heater", "🔥"),
    ("circle", "Light", "💡"),
    ("circle_plus", "Fan", "🌀"),
]

mode_class = "mode-manual" if current_manual_mode else "mode-auto"
mode_text = "MANUAL MODE" if current_manual_mode else "AUTO (AI Planner)"
mode_icon = "🟡" if current_manual_mode else "🔵"

st.subheader("Manual Override")

top_col1, top_col2 = st.columns([3, 1])

with top_col1:
    st.markdown(
        f'<span class="mode-badge {mode_class}">{mode_icon} {mode_text}</span>',
        unsafe_allow_html=True
    )

with top_col2:
    st.caption("Mirrors the physical button on GrovePi port D3.")

st.write("")

# Seed everything from the Pi the first time the app loads, then keep
# it synced on every rerun so ALL open dashboards (different laptops,
# tabs, etc.) reflect the real state — not just whatever it was when
# each one first loaded. The one exception: right after THIS session
# clicks any toggle, we skip syncing for a single rerun so the click
# doesn't visibly snap back before the Pi's MQTT round-trip confirms it.
override_just_changed = st.session_state.get("override_just_changed", False)

if "manual_mode_toggle" not in st.session_state:
    st.session_state.manual_mode_toggle = current_manual_mode

    for key, _, _ in ACTUATOR_CONTROLS:
        st.session_state[f"manual_{key}_toggle"] = bool(
            mqtt_handler.latest_actuator_status.get(key, False)
        )

elif override_just_changed:
    st.session_state.override_just_changed = False

else:
    st.session_state.manual_mode_toggle = current_manual_mode

    for key, _, _ in ACTUATOR_CONTROLS:
        st.session_state[f"manual_{key}_toggle"] = bool(
            mqtt_handler.latest_actuator_status.get(key, False)
        )


def _publish_override():
    st.session_state.override_just_changed = True

    actuator_states = {
        key: st.session_state[f"manual_{key}_toggle"]
        for key, _, _ in ACTUATOR_CONTROLS
    }
    mqtt_handler.publish_manual_override(
        st.session_state.manual_mode_toggle,
        actuator_states
    )
    st.toast(
        f"Manual override sent — mode {'ON' if st.session_state.manual_mode_toggle else 'OFF'}"
    )


st.toggle(
    "Manual Mode",
    key="manual_mode_toggle",
    on_change=_publish_override,
    help="ON = take control away from the AI planner. OFF = return to AUTO."
)

st.write("")

toggle_cols = st.columns(len(ACTUATOR_CONTROLS))

for col, (key, label, icon) in zip(toggle_cols, ACTUATOR_CONTROLS):
    with col:
        st.toggle(
            f"{icon} {label}",
            key=f"manual_{key}_toggle",
            disabled=not st.session_state.manual_mode_toggle,
            on_change=_publish_override
        )

st.divider()

# ---------------------------------------------------
# Actuator Status Overlay
# ---------------------------------------------------

ACTUATOR_DISPLAY = [
    ("relay", "Air Purifier", "🌬️"),
    ("room_led", "Air Conditioner", "❄️"),
    ("status_led", "Blinders", "🪟"),
    ("new_led", "Heater", "🔥"),
    ("circle", "Light", "💡"),
    ("circle_plus", "Fan", "🌀"),
]

if mqtt_handler.latest_actuator_status:

    st.subheader("Actuator Status")

    status = mqtt_handler.latest_actuator_status

    cols = st.columns(len(ACTUATOR_DISPLAY))

    for col, (key, label, icon) in zip(cols, ACTUATOR_DISPLAY):
        is_on = bool(status.get(key, False))
        state_class = "actuator-on" if is_on else "actuator-off"
        state_text = "ON" if is_on else "OFF"

        with col:
            st.markdown(
                f"""
                <div class="actuator-card">
                    <div class="actuator-icon">{icon}</div>
                    <div>
                        <div class="actuator-label">{label}</div>
                        <div class="actuator-state {state_class}">{state_text}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")

else:
    st.caption("⏳ Waiting for actuator status...")

# ---------------------------------------------------
# Sensor icon mapping
# ---------------------------------------------------

ICON_MAP = {
    "temperature": "🌡️",
    "humidity": "💧",
    "light": "💡",
    "motion": "🚶",
    "door": "🚪",
    "gas": "🟡",
    "sound": "🔊",
    "distance": "📏",
    "button": "🔘",
    "led": "🔆",
    "buzzer": "🔔",
    "fan": "🌀",
}


def get_icon(sensor_name: str) -> str:
    name = sensor_name.lower()
    for key, icon in ICON_MAP.items():
        if key in name:
            return icon
    return "📟"


# ---------------------------------------------------
# Fields to hide from the dashboard
# ---------------------------------------------------

HIDDEN_FIELDS = {
    "outside_pressure",
    "aqi",
    "wind_speed",
    "manual_relay",
    "manual_mode",
}


def is_hidden(sensor_key: str) -> bool:
    return sensor_key.strip().lower() in HIDDEN_FIELDS


# ---------------------------------------------------
# Live Sensor Data
# ---------------------------------------------------

if mqtt_handler.latest_data:

    st.subheader("Live Sensor Data")

    items = [
        (key, value) for key, value in mqtt_handler.latest_data.items()
        if not is_hidden(key)
    ]
    cols_per_row = 4
    rows = [items[i:i + cols_per_row] for i in range(0, len(items), cols_per_row)]

    for row in rows:
        cols = st.columns(cols_per_row)
        for col, (key, value) in zip(cols, row):
            label = key.replace("_", " ").title()
            icon = get_icon(key)
            with col:
                st.markdown(
                    f"""
                    <div class="sensor-card">
                        <div class="sensor-icon">{icon}</div>
                        <div class="sensor-label">{label}</div>
                        <div class="sensor-value">{value}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.markdown(
        f"<div class='footer-note'>Last update received from Raspberry Pi · {datetime.now().strftime('%H:%M:%S')}</div>",
        unsafe_allow_html=True
    )

    with st.expander("View raw data table"):
        df = pd.DataFrame(
            [
                {"Sensor": key.replace("_", " ").title(), "Value": str(value)}
                for key, value in mqtt_handler.latest_data.items()
                if not is_hidden(key)
            ]
        )
        st.dataframe(df, width="stretch", hide_index=True)

else:
    st.info("⏳ Waiting for MQTT data...")