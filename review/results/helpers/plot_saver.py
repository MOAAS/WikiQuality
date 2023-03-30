def show_and_save(plt, file, size):
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.gcf().set_size_inches(size[0], size[1])
    plt.savefig(file, dpi=100, bbox_inches='tight', pad_inches=0.1)
    plt.show()
