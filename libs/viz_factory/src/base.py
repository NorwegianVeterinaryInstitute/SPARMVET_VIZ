# viz_factory/src/plot_factory.py

def render_group_plots(group_config, dataframe):
    """
    Takes a 'group' from the YAML (e.g., AMR) 
    and returns a list of Plotnine figures.
    """
    figures = []

    for plot_meta in group_config['plots']:
        fid = plot_meta['factory_id']

        if fid == "bar_logic":
            fig = create_bar_chart(dataframe, plot_meta)
        elif fid == "heatmap_logic":
            fig = create_heatmap(dataframe, plot_meta)

        figures.append(fig)

    return figures
