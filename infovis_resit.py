#!/usr/bin/python3

import numpy as np
from bokeh.plotting import figure, curdoc
from bokeh.layouts import gridplot, widgetbox,row
from bokeh.models import LassoSelectTool, ColorBar, BasicTicker, LinearColorMapper, Select
from bokeh.models.sources import ColumnDataSource
from bokeh.palettes import viridis, d3

# read from the file that contains the generic audio features tsne map
audio_features_tsne_file = open("audio_features_tsne.csv","r")
audio_features_tsne_lines = audio_features_tsne_file.readlines()
audio_features_tsne_file.close()

# initialize lists that will hold the 2D coordinates
x = []
y = []

# get the coordinates of each item
for i in range(0,len(audio_features_tsne_lines)):
    line = audio_features_tsne_lines[i].split("\n")
    coords = line[0].split(",")
    x.append(coords[0])
    y.append(coords[1])

# convert coordinates' lists into arrays
X = np.asarray(x,dtype=np.float32)
Y = np.asarray(y,dtype=np.float32)

# read from file that contains the t-SNE map of the chord frequencies of each song
chord_frequencies_tsne_file = open("chord_frequencies_tsne.csv","r")
chord_frequencies_tsne_lines = chord_frequencies_tsne_file.readlines()
chord_frequencies_tsne_file.close()

# initialize 2D coordinates' lists
x1 = []
y1 = []

# read coordinates for each song
for i in range(0,len(chord_frequencies_tsne_lines)):
    line = chord_frequencies_tsne_lines[i].split("\n")
    coords = line[0].split(",")
    x1.append(coords[0])
    y1.append(coords[1])

# convert coordinates' lists into arrays
X1 = np.asarray(x1,dtype=np.float32)
Y1 = np.asarray(y1,dtype=np.float32)

# read from file containing the chord names
chords_file = open('chord_names.txt','r')
chords_lines = chords_file.readlines()
chords_file.close()

# initialize list of chord names
chords = []

# read chord names
for i in range(len(chords_lines)):
    line = chords_lines[i].split('\n')
    chords.append(line[0])

# read form file containing song names
songs_file = open('song_names.txt','r')
songs_lines = songs_file.readlines()
songs_file.close()

# initialize list of song names
songs = []

# read song names
for i in range(len(songs_lines)):
    line = songs_lines[i].split('\n')
    songs.append(line[0])

# read from file containing the chord frequency table for each song
chord_frequencies_file = open('chord_frequency_table.csv','r')
chord_frequencies_lines = chord_frequencies_file.readlines()
chord_frequencies_file.close()

# initialize lists containing chord frequencies and song id
chord_frequencies = []
y2 = []
x2 = []

# read frequencies for each song and store song id for each frequency
for i in range(len(chord_frequencies_lines)):
    line = chord_frequencies_lines[i].split('\n')
    frequencies = line[0].split(',') 
    for j in range(len(frequencies)):
        chord_frequencies.append(int(frequencies[j]))
        y2.append(i)
        x2.append(chords[j])

# convert chord names, chord frequencies and song ids' lists into arrays
X2 = np.asarray(chords)
Y2 = np.asarray(y2)
Y3 = np.asarray(chord_frequencies)
X3 = np.asarray(x2)


# read from file containing the genre of each song
genres_file = open('song_genres.csv','r')
genres_lines = genres_file.readlines()
genres_file.close()

# initialize genre lists, one for the scatterplot and one for the heatmap
scatter_genres = []
heatmap_genres = [] 

# read each genre and append to lists the required number of times
for i in range(len(genres_lines)):
    line = genres_lines[i].split('\n')
    scatter_genres.append(int(line[0]))
    for j in range(45):
        heatmap_genres.append(int(line[0]))

# read from the file containing the generic audio features
audio_features_file = open('generic_audio_features.csv')
audio_features_lines = audio_features_file.readlines()
audio_features_file.close()

# create a list for each generic audio feature
danceability = []
energy = []
key= []
loudness = []
mode = []
speechiness = []
acousticness = []
instrumentalness =[] 
liveness = []
valence= []
tempo = []
duration =[]
time_signature = []

# use a dictionary to quickly access the correct audio feature list through its index 
features_dict = { 0 : danceability, 1 : energy, 2 : key, 3 : loudness, 4 : mode, 5 : speechiness, 6 : acousticness, 7 : instrumentalness, 8 : liveness, 9 : valence, 10 : tempo, 11 : duration, 12 : time_signature}

# read generic audio features for each song
for i in range(len(audio_features_lines)):
    line = audio_features_lines[i].split('\n')
    features = line[0].split(',')
    for j in range(len(features)):
        features_dict[j].append(float(features[j]))

# maximum value of each feature found in the dataset
maxs = { 'key' : 11, 'mode' : 2, 'time_signature' : 5, 'genre' : 12, 'danceability' : 0.978, 'energy' : 0.999, 'loudness' : -0.201, 'speechiness' : 0.947, 'acousticness' : 0.996, 'instrumentalness' : 0.985, 'liveness' : 0.989, 'valence' : 0.995, 'tempo' : 217.648, 'duration' : 1643427.0, 'genre' : 12}

# minimum value of each feature found in the dataset
mins = { 'danceability' : 0.0, 'energy' : 2.03e-05, 'key' : 0.0, 'loudness' : -43.911, 'mode' : 0.0, 'speechiness' : 0.0, 'acousticness' : 0.0, 'instrumentalness' : 0.0, 'liveness' : 0.0199, 'valence' : 0.0, 'tempo' : 0.0, 'duration' : 10027.0, 'time_signature' : 0.0, 'genre' : 1}

# number of different values present in the dataset for each feature
ticks = { 'danceability' : 779, 'energy' : 940, 'key' : 12, 'loudness' : 4010, 'mode' : 2, 'speechiness' : 910, 'acousticness' : 2402, 'instrumentalness' : 2339, 'liveness' : 1129, 'valence' : 1102, 'tempo' : 4428, 'duration' : 4481, 'time_signature' : 5, 'genre' : 12}

# read from the file containing the normalized generic audio features
normalized_audio_features_file = open('audio_features_normalized.csv','r')
normalized_audio_features_lines = normalized_audio_features_file.readlines()
normalized_audio_features_file.close()

# create list of user options
columns = ['danceability','energy','key','loudness','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration','time_signature']

# initialize lists for vertical and horizontal position and value of each normalized generic audio feature
x4 = []
y4 = []
values = []

# populate these lists
for i in range(len(normalized_audio_features_lines)):
    line = normalized_audio_features_lines[i].split('\n')
    feats = line[0].split(',')
    for j in range(len(feats)):
        y4.append(i)
        x4.append(columns[j])
        values.append(feats[j])

# convert into arrays
Y4 = np.asarray(y4)
X4 = np.asarray(x4)
Values = np.asarray(values,dtype=np.float32)

# callback function for changing the colormap and colorbar of the scatterplots when the user chooses a generic audio feature
def update(attr, old, new):
    global p,p1
    # maximum, minimum values and number of different values for the chosen feature
    maxf = maxs[choice.value]
    minf = mins[choice.value]
    tickf = ticks[choice.value]

    # differentiate between features with discrete and continuous values when changing the color map and color_bar of each scatterplot
    if ((choice.value == 'key') or (choice.value == 'mode') or (choice.value == 'time_signature') or (choice.value == 'genre')):
        color_mapper = LinearColorMapper(palette=d3['Category20b'][int(maxf-minf+1)], high=maxf, low=minf)
        color_bar3 = ColorBar(color_mapper=LinearColorMapper(palette=d3['Category20b'][int(maxf-minf+1)], high=maxf, low=minf), ticker=BasicTicker(desired_num_ticks=int(maxf-minf+1)), label_standoff=6, border_line_color=None, location=(0,0))
        color_bar2 = ColorBar(color_mapper=LinearColorMapper(palette=d3['Category20b'][int(maxf-minf+1)], high=maxf, low=minf), ticker=BasicTicker(desired_num_ticks=int(maxf-minf+1)), label_standoff=6, border_line_color=None, location=(0,0))
    else:
        color_mapper = LinearColorMapper(palette=viridis(256), high=maxf, low=minf)
        color_bar3 = ColorBar(color_mapper=LinearColorMapper(palette=viridis(256), high=maxf, low=minf), ticker=BasicTicker(desired_num_ticks=25), label_standoff=3, border_line_color=None, location=(0,0))
        color_bar2 = ColorBar(color_mapper=LinearColorMapper(palette=viridis(256), high=maxf, low=minf), ticker=BasicTicker(desired_num_ticks=25), label_standoff=1, border_line_color=None, location=(0,0))
    
    # create new figure where the first scatterplot will be  depicted
    p = figure(tools=TOOLS, plot_width=1600, plot_height=900, title="Generic audio feature representation of songs")
    # disable uninformative mouse actions
    p.select(LassoSelectTool).select_every_mousemove=False
    # create scatterplot with color map and color bar
    renderer = p.scatter('x', 'y', line_color=None, source=source, color={'field' : choice.value, 'transform' : color_mapper})
    p.add_layout(color_bar3,'right')
    
    # same procedure for the second scatterplot
    p1 = figure(tools=TOOLS, plot_width=1600, plot_height=900, title="Chord frequencies representation of songs")
    p1.select(LassoSelectTool).select_every_mousemove=False
    renderer2 = p1.scatter('x1', 'y1', line_color=None, source=source, color={'field' : choice.value, 'transform' : color_mapper})
    p1.add_layout(color_bar2, 'right')
    # replace previous plots in the layout
    p7 = gridplot([[p,p4], [p1,p2]])
    layout.children[1] = p7


# add select button
choice = Select(title='Color map by audio feature', value='audio', options=['genre'] + columns)
# add callback
choice.on_change('value', update)
# add widget box
controls = widgetbox([choice], width=200)

# declare all tools that will be available in the figures
TOOLS="hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select,"

# create color map for genre
color_mapper = LinearColorMapper(palette=d3['Category20b'][12], high=12)

# create default figure
p = figure(tools=TOOLS, plot_width=1600, plot_height=900, title="Generic audio feature representation of songs")
p.select(LassoSelectTool).select_every_mousemove=False

# create shared data source between scatterplots, enables linked highlighting
source = ColumnDataSource(data=dict(x=X, y=Y, x1=X1, y1=Y1,genre=scatter_genres, danceability=danceability, energy=energy, key=key, loudness=loudness, mode=mode, speechiness=speechiness, acousticness=acousticness, instrumentalness=instrumentalness, liveness=liveness, valence=valence, tempo=tempo, duration=duration, time_signature=time_signature))

# create first scatterplot
renderer = p.scatter('x', 'y', line_color=None, source=source, color={'field' : 'genre', 'transform' : color_mapper})

# create its color bar
color_bar = ColorBar(color_mapper=LinearColorMapper(palette=d3['Category20b'][12], high=12,low=1), ticker=BasicTicker(desired_num_ticks=12), label_standoff=6, border_line_color=None, location=(0,0))
p.add_layout(color_bar, 'right')

# same procedure for the second scatterplot
p1 = figure(tools=TOOLS, plot_width=1600, plot_height=900, title="Chord frequencies representation of songs")
p1.select(LassoSelectTool).select_every_mousemove=False
renderer2 = p1.scatter('x1', 'y1', line_color=None, source=source, color={'field' : 'genre', 'transform' : color_mapper})
color_bar2 = ColorBar(color_mapper=LinearColorMapper(palette=d3['Category20b'][12], high=12, low=1), ticker=BasicTicker(desired_num_ticks=12), label_standoff=6, border_line_color=None, location=(0,0))
p1.add_layout(color_bar2, 'right')

# create figures, heat maps, color maps and color bars
color_mapper9 = LinearColorMapper(palette=viridis(256), high=1,low=0)
color_mapper8 = LinearColorMapper(palette=viridis(30), high=29, low=0)
p2 = figure(x_range=chords,y_range=songs,tools=TOOLS, plot_width=1600, plot_height=900, title="Chord frequencies of songs")
source2 = ColumnDataSource(data=dict(x3=X3, y3=Y2, val=Y3))
p2.rect(x='x3', y='y3', width=0.2, height=2, line_color=None, fill_color={'field' : 'val', 'transform' : color_mapper8}, source=source2)
color_bar1 = ColorBar(color_mapper=LinearColorMapper(palette=viridis(30), high=29,low=0), ticker=BasicTicker(desired_num_ticks=30), label_standoff=6, border_line_color=None, location=(0,0))
p2.add_layout(color_bar1, 'right')

source3 = ColumnDataSource(data=dict(x4=X4, y4=Y4,val=Values))
p4 = figure(y_range=songs,x_range=columns,tools=TOOLS, plot_width=1600, plot_height=900, title="Generic Audio Features of songs")
p4.rect(x='x4', y='y4', width=0.2, height=1, line_color=None, fill_color={'field' : 'val', 'transform' : color_mapper9}, source=source3)
color_bars = ColorBar(color_mapper=LinearColorMapper(palette=viridis(256), high=1, low=0), ticker=BasicTicker(desired_num_ticks=25), label_standoff=6, border_line_color=None, location=(0,0))
p4.add_layout(color_bars, 'right')

# remove horizontal and vertical lines of figures
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None
p1.ygrid.grid_line_color = None
p1.xgrid.grid_line_color = None
p2.ygrid.grid_line_color = None
p2.xgrid.grid_line_color = None
p4.ygrid.grid_line_color = None
p4.xgrid.grid_line_color = None

# create grid of figures
p3 = gridplot([[p,p4],[p1,p2]])

# create row with select widget and grid
layout = row(controls, p3)

# add layout as root of current document
curdoc().add_root(layout)

# callback for user selection in the scatterplots
def selectChords(attr,old,new):
    # if selection contains points
    if new.indices !=[]:
        # create lists for the coordinates, values and names of each of the selected song
        xs = []
        ys = []
        vs = []
        s = []
        xf = []
        yf = []
        vf = []
        for i in range(len(new.indices)):
            s.append(songs[new.indices[i]])
            for j in range(new.indices[i]*45,new.indices[i]*45+45):
                    ys.append(i)
                    xs.append(chords[j % 45])
                    vs.append(chord_frequencies[j])
            for j in range(new.indices[i]*13,new.indices[i]*13+13):
                yf.append(i)
                xf.append(columns[j % 13])
                vf.append(values[j])

        # create the new heatmaps
        p2 = figure(x_range=chords,y_range=s,tools=TOOLS, plot_width=1600, plot_height=900, title="Chord frequencies of songs")
        source4 = ColumnDataSource(data=dict( x3=xs, y3=ys, val=vs))
        p2.rect(x='x3', y='y3', width=0.2, height=2, line_color=None, fill_color={'field' : 'val', 'transform' : color_mapper8}, source=source4)
        color_bar1 = ColorBar(color_mapper=LinearColorMapper(palette=viridis(30), high=29, low=0), ticker=BasicTicker(desired_num_ticks=30), label_standoff=6, border_line_color=None, location=(0,0))
        p2.add_layout(color_bar1, 'right')
        source3 = ColumnDataSource(data=dict(x4=xf, y4=yf,val=vf))
        p4 = figure(y_range=s,x_range=columns,tools=TOOLS, plot_width=1600, plot_height=900, title="Generic Audio Features of songs")
        p4.rect(x='x4', y='y4', width=0.2, height=1, line_color=None, fill_color={'field' : 'val', 'transform' : color_mapper9}, source=source3)
        color_bars = ColorBar(color_mapper=LinearColorMapper(palette=viridis(256), high=1, low=0), ticker=BasicTicker(desired_num_ticks=25), label_standoff=6, border_line_color=None, location=(0,0))
        p4.add_layout(color_bars, 'right')
        p2.ygrid.grid_line_color = None
        p2.xgrid.grid_line_color = None
        p4.ygrid.grid_line_color = None
        p4.xgrid.grid_line_color = None
        p8 = gridplot([[p,p4], [p1,p2]])
        layout.children[1] = p8


# register selection callback
renderer.data_source.on_change('selected',selectChords)

