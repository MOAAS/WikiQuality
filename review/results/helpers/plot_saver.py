def show_and_save(plt, file, size = None, type = ''):
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    if size is not None:
        plt.gcf().set_size_inches(size[0], size[1])

    if type == 'boxplot':
        # median lines must be black
        for line in plt.gca().get_lines():
            line.set_color('black')
    plt.savefig(file, dpi=100, bbox_inches='tight', pad_inches=0.1)
    plt.show()
