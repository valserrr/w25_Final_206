#This is where we will create the data visualization for the data we have collected.
import matplotlib.pyplot as plt # type: ignore
import pandas as pd # type: ignore

def visualize_scatterplot():
    '''Create a scatterplot of the data.'''

    pass

def visualize_bargraoh():
    '''Create a bar graph of the data.'''
#example of bar chart 
songs = list(top_songs.keys())[::-1]
count = list(top_songs.values())[::-1]

plt.figure(figsize=(10, 6))  # adjust as needed
plt.barh(songs, count, color='blue')
plt.xlabel('Play counts')
plt.ylabel('Song Name')
plt.title('Top 5 Songs')
plt.tight_layout()  # helps prevent label cut-off
plt.savefig("top_songs.png")
    pass