import matplotlib.pyplot as plt

def generate_search_plot(search_dict):
    x_values, y_values, scores = [], [], []

    for setting_id, data in search_dict.items():
        x_values.append(data["knobs"][0])
        y_values.append(data["knobs"][1])
        scores.append(data["scores"])  

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