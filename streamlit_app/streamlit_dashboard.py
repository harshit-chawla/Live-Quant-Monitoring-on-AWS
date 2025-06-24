import streamlit as st
import pandas as pd
from crontab import CronTab
import subprocess
import os, sys

code_name = 'Task Scheduler'
print(code_name)
if sys.platform == 'linux':
    print(f"\033]0;{code_name}\007")
elif sys.platform == 'win32':
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(code_name)

# Set Streamlit to wide layout
st.set_page_config(layout="wide")

# Load user's crontab
cron = CronTab(user=True)

# Extract job details
data = []
for job in cron:
    if job.comment == 'Set Position':
        continue
    try:
        job_time = pd.to_datetime(f"{job.hour}:{job.minute}", format="%H:%M").time()
        data.append({
            "Time": job_time,
            "Name": job.comment,
            "Command": job.command
        })
    except Exception:
        continue

df = pd.DataFrame(data).sort_values(by="Time").reset_index(drop=True)
for idx,i in df.iterrows():
    i.Time = i.Time.replace(second = int(i.Command.split(';')[0].split(' ')[1]))

st.title("Task Scheduler")

if not df.empty:
    st.markdown("### Select Jobs to Run:")

    # Table headers
    col1, col2, col3, col4  = st.columns([0.05, 0.5, 0.8, 0.8])
    with col1:
        st.markdown("**✔️**")
    with col2:
        st.markdown("**Triggers**")
    with col3:
        st.markdown("**Name**")
    with col4:
        st.markdown("Click To Run")

    selected_jobs = []

    # Display job list
    for idx, row in df.iterrows():
        col1, col2, col3, col4  = st.columns([0.05, 0.5, 0.8, 0.8])
        with col1:
            if st.checkbox("", key=idx):
                selected_jobs.append(row)
        with col2:
            st.write(row["Time"])
        with col3:
            st.write(row["Name"])
        with col4:
             if st.button(" Run Selected Jobs", key=f"run_button_{idx}"):
                errors = []
                try:
                    command_parts = row['Command'].split('"')
                    code_path = command_parts[2].replace("\\", "")
                    code_name = command_parts[4].replace("\\", "")

                    subprocess.Popen([
                        "xfce4-terminal", "-e",
                        f"bash -c 'cd \"{code_path}\" && python3 \"{code_name}\"; exit'"
                    ])
                except Exception as e:
                    errors.append((row['Name'], str(e)))

                if errors:
                    st.error("Some jobs failed to launch:")
                    for name, err in errors:
                        st.error(f"❌ {name}: {err}")
                else:
                    st.success("✅ All selected scripts started in terminal.")
            

    if selected_jobs:
        if st.button(" Run Selected Jobs"):
            errors = []
            for row in selected_jobs:
                try:
                    command_parts = row['Command'].split('"')
                    code_path = command_parts[2].replace("\\", "")
                    code_name = command_parts[4].replace("\\", "")

                    subprocess.Popen([
                        "xfce4-terminal", "-e",
                        f"bash -c 'cd \"{code_path}\" && python3 \"{code_name}\"; exit'"
                    ])
                except Exception as e:
                    errors.append((row['Name'], str(e)))

            if errors:
                st.error("Some jobs failed to launch:")
                for name, err in errors:
                    st.error(f"❌ {name}: {err}")
            else:
                st.success("✅ All selected scripts started in terminal.")
    else:
        st.info("Please select at least one job to run.")
else:
    st.warning("No relevant cron jobs found.")
