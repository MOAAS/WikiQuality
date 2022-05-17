import matplotlib.pyplot as plot

from helpers import load_model

def analyze_feature_importance(modelname):
    model, features = load_model(modelname)
    importance = model.feature_importances_

    # make dictonary of feature names and importance values
    feature_importance = dict(zip(features, importance))

    # get the top 20 and bottom 20 features
    top_20_1 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[0:10])
    top_20_2 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[11:20])
    bottom_20_1 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=False)[0:10])
    bottom_20_2 = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=False)[11:20])
    
    figure_top, axis_top = plot.subplots(2, 1,figsize=(9,6))
    figure_bot, axis_bot = plot.subplots(2, 1,figsize=(9,6))

    axis_top[0].set_title('Feature Importance: Top 20')
    axis_top[0].bar(top_20_1.keys(), top_20_1.values())
    axis_top[1].bar(top_20_2.keys(), top_20_2.values())

    #figure.tight_layout()

    axis_bot[0].set_title('Feature Importance: Bottom 20')
    axis_bot[0].bar(bottom_20_1.keys(), bottom_20_1.values())
    axis_bot[1].bar(bottom_20_2.keys(), bottom_20_2.values())

    plot.draw()
    plot.pause(1) # https://stackoverflow.com/a/22899859
    plot.waitforbuttonpress(0)
    plot.close(figure_bot)
    plot.close(figure_top)

analyze_feature_importance("CSRH6/forest_r")
