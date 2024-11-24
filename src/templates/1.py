import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Create data with multiple payment methods for each season
data = {
    'Season': ['Winter', 'Winter', 'Spring', 'Spring', 'Summer', 'Summer', 'Fall', 'Fall'],
    'Sales Value ($)': [102.13, 110.67, 184.14, 120.56, 348.92, 310.45, 281.57, 295.68],
    'Payment Method': ['Bank Transfer', 'Cash', 'PayPal', 'Credit Card', 'Credit Card', 'Bank Transfer', 'Cash', 'PayPal'],
    'Average Sales Value ($)': [106.40, 106.40, 152.35, 152.35, 329.69, 329.69, 288.63, 288.63]
}

df = pd.DataFrame(data)

# Adjusting the plot to increase visibility
plt.figure(figsize=(14, 8))
plt.style.use('dark_background')


# Create a grouped bar chart
sns.barplot(x='Season', y='Sales Value ($)', hue='Payment Method', data=df, palette='plasma')

# Adjusting text styling, positioning, and colors for better visibility
plt.title('Sales Value by Season and Payment Method', fontsize=20, color='red', fontweight='bold')
plt.xlabel('Season', fontsize=16, color='orange', fontweight='bold')
plt.ylabel('Sales Value ($)', fontsize=16, color='orange', fontweight='bold')


# Adding an annotation indicating a  recession period in the 'Winter' season
plt.annotate('Recession Period', xy=(0, 170), xytext=(0.2, 200), textcoords='data',
             arrowprops=dict(arrowstyle="->", color='white', lw=2), color='white', fontsize=14)

# Adding a trend line for the average sales value using the provided column
seasons = df['Season'].unique()
avg_sales = [df[df['Season'] == season]['Average Sales Value ($)'].iloc[0] for season in seasons]
plt.plot(seasons, avg_sales, color='lime', linestyle='--', linewidth=2, label='Average Trend Line')

# Display the legend for the trend line
plt.legend(loc='upper left', fontsize=12, frameon=True, facecolor='darkgray', edgecolor='white', bbox_to_anchor=(1.05, 1))

plt.tight_layout()
plt.show()
