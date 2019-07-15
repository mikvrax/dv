%load frequency table
frequencies = csvread('ft2.csv');
%load song genres as numbers
genres = csvread('cgenres.csv');
%figures always on full screen
figure('units','normalized','outerposition',[0 0 1 1]);
%compute t-SNE mapping 
map = fast_tsne(frequencies,2,45,30);
%plot mapping using genre values as colormap
scatter(map(:,1),map(:,2),20,genres);
%let user select data
selection = selectdata;
%do not show next figure immediately
pause(1);
%get only the genres of the selected songs
selgenres = genres(selection);
%sort them and get index
[~,sorted] = sort(selgenres);
%get frequency table for selected songs
selfreq = frequencies(selection,:);
%get song names
fil = fopen('songs7.csv');
cel = textscan(fil,'%s','Delimiter','\n');
selsongs = {};
for i=1:size(cel{1,1},1)
selsongs{i,1} = cel{1,1}{i,1};
end
%get chord names
fil2 = fopen('chords.csv');
chords = textscan(fil2,'%s','Delimiter','\n');
%have selected frequencies, genres and songs according to the sorting of
%genres
sortedselfreq = selfreq(sorted,:);
sortedselgenres = selgenres(sorted);
sortedselsongs = {};
for i=1:size(sorted,1)
sortedselsongs{i,1} = selsongs{sorted(i),1};
end;
%display first heatmap
h = heatmap(chords{1,1},sortedselsongs,sortedselfreq);
%put labels and title
h.Title = 'Chord Frequency Table';
h.XLabel = 'Chords';
h.YLabel = 'Songs';
%wait before second heatmap
pause(2);
%get frequencies per genre
for i=1:length(unique(genres))
vec{i} = frequencies(find(genres == i),:);
end
%compute sum of frequencies per genre and normalize it
for i=1:length(unique(genres))
vec2{i} =  sum(vec{i})/length(vec{i});
vec2{i}  = (vec2{i} - min(vec2{i}))/(max(vec2{i}) -min(vec2{i}));
end
%turn to correct form for display using heatmap
norm = vertcat(vec2{:});
norm = norm';
for i=1:45
norm(i,:)=(norm(i,:)- min(norm(i,:)))/(max(norm(i,:)) - min(norm(i,:)));
end
%get genres' names
fil3 = fopen('genrenames.txt');
genrenames = textscan(fil3,'%s','Delimiter','\n');
figure('units','normalized','outerposition',[0 0 1 1]);
%second heatmap
h2 = heatmap(genrenames{1,1},chords{1,1},norm);
h2.Title = 'Chord usage per genre';
h2.XLabel = 'Genre';
h2.YLabel = 'Chords';
