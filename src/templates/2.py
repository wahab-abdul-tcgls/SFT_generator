import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create the DataFrame
data = {
    'Player': [
        'Player A', 'Player A', 'Player A',
        'Player B', 'Player B', 'Player B',
        'Player C', 'Player C', 'Player C',
        'Player D', 'Player D', 'Player D',
        'Player E', 'Player E', 'Player E'
    ],
    'Match Type': [
        'Test', 'ODI', 'T20',
        'Test', 'ODI', 'T20',
        'Test', 'ODI', 'T20',
        'Test', 'ODI', 'T20',
        'Test', 'ODI', 'T20'
    ],
    'Runs': [
        450, 500, 350,
        670, 800, 450,
        890, 950, 60,
        420, 470, 320,
        560, 610, 410
    ],
    'Strike Rate': [
        45.0, 90.0, 130.0,
        50.0, 95.0, 140.0,
        55.0, 100.0, 150.0,
        40.0, 85.0, 120.0,
        48.0, 92.0, 135.0
    ]
}

df = pd.DataFrame(data)

# Set up the 3D plot
fig = plt.figure(figsize=(15, 10))
ax = fig.add_subplot(111, projection='3d')

# Set background
fig.patch.set_facecolor('#1a1a1a')
ax.set_facecolor('#1a1a1a')

# Axis positions
players = df['Player'].unique()
match_types = df['Match Type'].unique()
x_pos = np.arange(len(players))  # Player positions
y_pos = np.arange(len(match_types))  # Match type positions

# Bar dimensions
bar_width = 0.3
depth = 0.4
z_pos = np.zeros(len(players) * len(match_types))

# Colors for match types
colors = plt.cm.plasma(np.linspace(0.3, 0.9, len(match_types)))

# Plot runs and strike rates as grouped bars
for i, match_type in enumerate(match_types):
    mask = df['Match Type'] == match_type
    run_values = df[mask]['Runs'].values
    strike_rate_values = df[mask]['Strike Rate'].values

    # Adjust x positions for each match type
    x_positions = np.arange(len(players)) + i * (bar_width * 2)

    # Runs bar
    ax.bar3d(
        x_positions, y_pos[i], z_pos[:len(players)],
        bar_width, depth, run_values,
        color=colors[i], alpha=0.8, label=f'{match_type} Runs'
    )

    # Strike Rate bar
    ax.bar3d(
        x_positions + bar_width, y_pos[i], z_pos[:len(players)],
        bar_width, depth, strike_rate_values,
        color=colors[i], alpha=0.5, label=f'{match_type} Strike Rate'
    )

# Labels and formatting
ax.set_xlabel('Players', labelpad=20, color='white')
ax.set_ylabel('Match Types', labelpad=20, color='white')
ax.set_zlabel('Performance Metrics', labelpad=10, color='white')
ax.set_title('Player Performance Comparison: Runs vs Strike Rate', color='white', pad=30)

# Custom tick labels
ax.set_xticks(np.arange(len(players)) + bar_width)
ax.set_xticklabels(players, rotation=45, ha='right', color='white')
ax.set_yticks(y_pos)
ax.set_yticklabels(match_types, color='white')
ax.tick_params(axis='z', colors='white')

# Add watermark
fig.text(0.5, 0.5, 'Cricket Analysis 2024', fontsize=40, color='grey', alpha=0.2, ha='center', va='center', rotation=30)

plt.legend(loc='upper left', fontsize=12, frameon=True, facecolor='black', edgecolor='white', bbox_to_anchor=(1.05, 1))
plt.tight_layout()
plt.show()