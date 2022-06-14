# WikiQuality - Real-time prediction of Wikipedia articles' quality.

WikiQuality is a Chrome extension that uses Machine Learning to automatically predict the quality of Wikipedia articles. It was trained using a dataset of 36,000 English Wikipedia articles, and uses a set of 145 different features to determine the quality output. The model predicts quality with a mean error of 9%, higher on non-English articles, so these results are meant to be indicators of quality and are not to be taken as flawless ratings. Definitions of quality are based on Wikipedia's quality scale.​

This application was developed for the Master's Dissertation titled "Real-time prediction of Wikipedia articles' quality". This project was developed by Pedro Miguel Moás, with the supervision of Professor Carla Teixeira Lopes, from October 2021 to June 2022.

The extension is published in https://up201705208.wixsite.com/wikiquality, which succinctly explains the context of the application and its uses.

This repository contains all the code developed for the project, and is structured in the following manner:

docs/ - Contains relevant data produced during the stages of planning analysis of the state of the art. This data may be outdated, so please refer to the dataset published for the Systematic Literature Review article (temporarily available [here](https://drive.google.com/drive/folders/1t1ojqrEV98zmHWY1WCgmwwuaQwBVcWca?usp=sharing))

extension/ - Source code for the Chrome extension, developed using React.

graph/ - Source code for the Graph Parser written to convert the dataset provided in https://law.di.unimi.it/webdata/enwiki-2022/ into the csv file containing Wikipedia's nodes and edges.

ml/ - Source code for the development and testing of the Machine Learning model. All the code is written in python, using frameworks like sklearn and flask.


