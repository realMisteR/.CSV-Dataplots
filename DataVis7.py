import matplotlib.pyplot as plt
import pandas as pd


# Load CSV data into a pandas dataframe
data = pd.read_csv(r"C:\Users\realm\OneDrive\Desktop\Python Projects\SPY.csv")

# Create subplots with shared X-axis and custom subplot heights
fig, ax = plt.subplots(3, 1, figsize=(10,8), sharex=True, gridspec_kw={'height_ratios': [2, 1.3, 0.3]})



# Convert Date column to datetime format
data['Date'] = pd.to_datetime(data['Date'])

# Extract month and year from Date column
month_year = data['Date'].dt.strftime('%Y-%m')

# Find the first occurrence of each month
first_day_index = [0]
prev_month = month_year[0]
for i, date in enumerate(data['Date'][1:]):
    if month_year[i+1] != prev_month:
        first_day_index.append(i+1)
        prev_month = month_year[i+1]

# Plot the price data on the first subplot (twice as tall)
ax[0].plot(data['Date'], data['Close'])
ax[0].set_ylabel('Price', color='#fb8b1e')
ax[0].tick_params(axis='y', labelcolor='#fb8b1e')

# Sort the data frame by volume and select the top 15 volume prints
top_15_volume = data.sort_values(by='Volume', ascending=False).head(15)
low_15_volume = data.sort_values(by='Volume', ascending=True).head(15)

# Plot the top 15 volume prints relative to their respective price on the first subplot
scatter1 = ax[0].scatter(top_15_volume['Date'], top_15_volume['Close'], s=top_15_volume['Volume']/100000*0.25, color='#ff433d', alpha=0.5)
scatter2 = ax[0].scatter(low_15_volume['Date'], low_15_volume['Close'], s=low_15_volume['Volume']/100000*0.25, color='#4af6c3', alpha=0.5)
ax[0].set_ylim(data['Close'].min() * 0.95, data['Close'].max() * 1.05)

# Add label for the most recent 'Close' print
most_recent_close = data['Close'].iloc[-1]
ax[0].annotate(f'{most_recent_close:.2f}', xy=(data['Date'].iloc[-1], most_recent_close), xytext=(-15, 10), textcoords='offset points', fontsize=12, color='#fb8b1e')

# Add date labels to the top 15 volume prints on subplot 1
for i, point in top_15_volume.iterrows():
    date = point['Date'].strftime('%m/%d')
    ax[0].annotate(date, xy=(point['Date'], point['Close']), xytext=(5,-15), textcoords='offset points', fontsize=8, color='#fb8b1e')


# Highlight the top 15 volume bars on subplot 2
color_list = ['orange']*len(data)
for i, point in top_15_volume.iterrows():
    index = data[data['Date']==point['Date']].index[0]
    color_list[index] = '#ff433d'
for i, point in low_15_volume.iterrows():
    index = data[data['Date']==point['Date']].index[0]
    color_list[index] = '#4af6c3'
ax[1].bar(data['Date'], data['Volume'], color=color_list, alpha=0.3)
ax[1].set_ylabel('Volume')


# Customize the plot
plt.suptitle('$SPY', color='#fb8b1e')
plt.xlabel('Date', color='#fb8b1e')
plt.gcf().patch.set_facecolor('#000000')

# Add month labels to X-axis
ax[1].set_xticks(data['Date'][first_day_index])
ax[1].set_xticklabels(data['Date'][first_day_index].dt.strftime('%b %Y'), rotation=30)


# Load CSV data for ^VIX into a pandas dataframe
vix_data = pd.read_csv(r"C:\Users\realm\OneDrive\Desktop\Python Projects\^VIX.csv")

# Convert Date column to datetime format
vix_data['Date'] = pd.to_datetime(vix_data['Date'])

# Plot the price data on the second subplot
ax[1].plot(vix_data['Date'], vix_data['Close'], color='#0068ff')
ax[1].set_ylabel('^VIX Close', color='#fb8b1e')
ax[1].set_ylim(bottom=vix_data['Close'].min()*0.95, top=vix_data['Close'].max()*1.05)

# Load CSV data for Moon into a pandas dataframe
moon_data = pd.read_csv(r"C:\Users\realm\OneDrive\Desktop\Python Projects\Moon.csv")

# Convert datetime column to datetime format
moon_data['datetime'] = pd.to_datetime(moon_data['datetime'])

# Filter the data to include only Full Moons and New Moons
moon_data = moon_data[moon_data['phase'].isin(['Full Moon', 'New Moon'])]

# Create color list for Full Moons and New Moons
colors = ['#0068ff' if phase == 'Full Moon' else '#FB8B1E' for phase in moon_data['phase']]

# Filter the data to only include data between April 2022 and April 2023
moon_data = moon_data[(moon_data['datetime'] >= '2022-04-01') & (moon_data['datetime'] <= '2023-04-30')]

# Plot the moon phases data on the third subplot
ax[2].scatter(moon_data['datetime'], moon_data['phase'])
ax[2].tick_params(axis='y', labelcolor='#fb8b1e')

# Change the background color of subplots 1, 2, and 3 to black, and change all X and Y axis labels to the color orange
fig.set_facecolor('black')
for i, axi in enumerate(ax):
    axi.tick_params(axis='x', colors='orange')
    axi.tick_params(axis='y', colors='orange')
    axi.set_xlabel('Date', color='orange')
    axi.set_ylabel(axi.get_ylabel(), color='orange')
    axi.set_facecolor('black')
    if i != 2:
        axi.grid(color='white', linestyle='--', alpha=0.5)
ax[0].set_xlabel('')
ax[1].set_xlabel('')

# Skew the date labels on the x-axis of the first subplot by 25%
ax[0].set_xticks(data['Date'][first_day_index])
ax[2].set_xticklabels(data['Date'][first_day_index].dt.strftime('%b %Y'), rotation=25, ha='right')

# Set custom y-axis tick labels and adjust the ylim for subplot 3
ax[2].set_yticks([0, 1])
ax[2].set_yticklabels(['New Moon', 'Full Moon'])
ax[2].set_ylim(-0.5, 1.5)

plt.show()