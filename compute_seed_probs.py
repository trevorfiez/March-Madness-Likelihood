import csv
import plotly

import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline

def is_int(s):
	try:
		int(s)
		return True
	except ValueError:
		return False
	
def plot_matchup_num(counts):
	trace = go.Heatmap(z=counts, x=range(1,17), y=range(1, 17),colorscale="Greens", text=counts)
	
	data = [trace]
	
	layout = go.Layout(title='NCAA Seed Match-Up Counts',
						 width = 700, height = 700,
					    autosize = True,
						)
	fig = go.Figure(data=data, layout=layout)
	
	
	offline.plot(fig, image='png', image_filename='/scratch/tfiez/junk/March-Madness-Likelihood/game_counts', image_width=700, image_height=700)

def plot_win_prob(counts):
	trace = go.Heatmap(z=counts, x=range(1,17), y=range(1, 17), text=counts)
	
	data = [trace]
	
	layout = go.Layout(title='Raw Win Probability',
						 width = 700, height = 700,
					    autosize = True,
						xaxis=dict(title='Losing Seed'),
						yaxis=dict(title='Winning Seed'))
	fig = go.Figure(data=data, layout=layout)
	
	
	offline.plot(fig, image='png', image_filename='unnorm_win', image_width=700, image_height=700)

def load_games():
	games = []
	with open('ncaa_tourney_results.csv', 'r') as csvfile:
		tourney = csv.reader(csvfile)
		adding_games = False
		for row in tourney:
			if (row[0] == '1979'):
				adding_games = True
			
			if (not adding_games):
				continue
			
			#print(row[3])
			if (not is_int(row[3]) and not is_int(row[4])):
				continue
			
			if (is_int(row[3])):
				games.append([int(row[3]), int(row[5]), int(row[6]), int(row[8])])
			else:
				games.append([int(row[4]), int(row[6]), int(row[7]), int(row[9])])
			#if (row[6] == '16'):
			#print(row)
			
	return games
			
	
def compute_seed_win_percentages(games, normalization=None, scale=16):
	win_counts = []
	for i in xrange(16):
		win_counts.append([])
		for j in xrange(16):
			#win_bias = j
			if (normalization is None):
				win_counts[-1].append([0, 0])
			elif (normalization == "Bad"):
				win_counts[-1].append([j, i + j])
			elif (normalization == "Good"):
				win_val = 16 - i
				total_val = 32 - i - j
				
				win_counts[-1].append([16 - i, 32 - i - j])
			elif (normalization == "Other Good"):
				num = (i - j) / 2.0
				#if (i > j):
				win_bias = scale * ((8.0 - num) / 16.0)
				win_counts[-1].append([win_bias, float(scale)])
				#else:
				#win_counts[-1].append([8 + num, 16])

	#return win_counts
	for game in games:
		winner_index = game[0] - 1
		loser_index = game[2] - 1
		
		win_counts[winner_index][loser_index][0] += 1
		win_counts[winner_index][loser_index][1] += 1
		win_counts[loser_index][winner_index][1] += 1
		
	return win_counts

def diff_in_expected_wins(unnorm, norm):
	
	diff = 0.0
	for i in range(len(unnorm)):
		for j in range(len(unnorm[i])):
			expected_wins = unnorm[i][j][1] * (float(norm[i][j][0])/ float(norm[i][j][1]))
			diff += abs(expected_wins - unnorm[i][j][0])
			
	return diff
	
def main():
	games = load_games()
	'''
	for game in games:
		print(game)
	'''
	#for scale in range(1,30):
	probs = compute_seed_win_percentages(games, normalization='Other Good', scale=16.0)
	'''
	for i in xrange(8):
		for j in xrange(8):
			print(str(i + 1) + " win vs. " + str(j + 1))
			print(probs[i][j])
	'''	
	game_counts = []
	unnormalized_win = []
	for row in probs:
		game_counts.append([])
		unnormalized_win.append([])
		for entry in row:
			game_counts[-1].append(entry[1])
			
			if (entry[1] == 0):
				unnormalized_win[-1].append(0.5)
			else:
				unnormalized_win[-1].append(float(entry[0])/ float(entry[1]))
			
	unnorm_counts = compute_seed_win_percentages(games)
	#print(probs[0][15])
	#plot_matchup_num(game_counts)
	#plot_win_prob(unnormalized_win)
	
	with open('seed_win_probs.csv', 'w') as f:
		writer = csv.writer(f)
		writer.writerows(unnormalized_win)
	
	#diff = diff_in_expected_wins(unnorm_counts, probs)
	#print("Diff " + str(scale))
	#print(diff)


if __name__ == "__main__":
	main()