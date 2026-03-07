# Inside viz_factory/src/bar_logic.py
def draw_bar(df, config):
    # 'height' is guaranteed to be here because of the ConfigManager merge!
    fig = px.bar(df, x=config['target_col'], height=config['height'])
    return fig