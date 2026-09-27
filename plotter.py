import matplotlib.pyplot as plt

def generate_search_plot(history_list):
    x_values, y_values, scores = [], [], []

    # extract the knob settings and their corresponding scores from the history list pair (knob settings, score)
    for knobs, score in history_list:
        x_values.append(knobs[0])
        y_values.append(knobs[1])
        scores.append(score)

    # create a scatter plot of the knob settings and their corresponding scores
    plt.scatter(x_values, y_values, c=scores, vmin=0, vmax=1)

    # add a color bar to indicate the score values
    plt.colorbar(label='Decode Rate')

    #add labels and title to the plot
    plt.xlabel('Knob 1 Setting')
    plt.ylabel('Knob 2 Setting')
    plt.title('Decode Rates for Settings Tried')

    # display the plot
    plt.show()