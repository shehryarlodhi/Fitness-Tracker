from unicodedata import category
from matplotlib.patches import Shadow
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle('../../data/interim/01_data_processed.pkl')

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df["set"]==1]
plt.plot(set_df["acc_z"].reset_index(drop=True))
# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------
for label in df["label"].unique():
    subset = df[df["label"]==label]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_x"].reset_index(drop=True),label=label) 
    plt.legend()
    plt.plot()
# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"]=(20,5)
mpl.rcParams["figure.dpi"]=100


# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------
category_df = df.query("label=='squat'").query("participant=='D'").reset_index()
fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------
paricipant_df = df.query("label=='bench'").sort_values("participant").reset_index()
fig, ax = plt.subplots()
paricipant_df.groupby(["participant"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------
label = "squat"
participant = "A"
all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
fig, ax = plt.subplots()
all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()
# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
    for participant in participants:
        all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()

        if len(all_axis_df)>0:
            fig, ax = plt.subplots()
            all_axis_df[["acc_x","acc_y","acc_z"]].plot(ax=ax)
            ax.set_ylabel("acc_y")
            ax.set_xlabel("samples")
            plt.title(f"{label}({participant})".title())
            plt.legend()
# ---------------
# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
label = "row"
participant = "A"
combined_plot_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index(drop=True)

fig,ax = plt.subplots(nrows=2,sharex=True,figsize= (20,10))
combined_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
combined_plot_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax[1])

ax[0].legend(loc="upper center", bbox_to_anchor = (0.5,1.15),ncol=3, fancybox=True,Shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor = (0.5,1.15),ncol=3, fancybox=True,Shadow=True)
ax[1].set_xlabel("samples")
# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
labels = df["label"].unique()
participants = df["participant"].unique()

for label in labels:
    for participant in participants:
        combined_plot_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()

        if len(combined_plot_df)>0:
            fig,ax = plt.subplots(nrows=2,sharex=True,figsize= (20,10))
            combined_plot_df[["acc_x","acc_y","acc_z"]].plot(ax=ax[0])
            combined_plot_df[["gyr_x","gyr_y","gyr_z"]].plot(ax=ax[1])

            ax[0].legend(loc="upper center", bbox_to_anchor = (0.5,1.15),ncol=3, fancybox=True, shadow=True)
            ax[1].legend(loc="upper center", bbox_to_anchor = (0.5,1.15),ncol=3, fancybox=True,shadow=True)
            ax[1].set_xlabel("samples")
            plt.savefig(f"../../reports/figures/{label} ({participant}).png")
            plt.show()