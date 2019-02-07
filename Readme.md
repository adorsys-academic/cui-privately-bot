# CUI Privately Bot

In his thesis Marco Maisel evaluated the use of open-source-based NLU technologies as an alternative to commercial services.  Open source solutions, which operate entirely on proprietary servers, promise to be a more thoughtful approach for handling private and confidential data.  In the course of the thesis Marco Maisel implemented a chatbot based on RASA NLU and RASA Core which allows candidates to find matching job offers.


## Installation + Running of the bot
To set up the bot, clone the repo and install rasa:

```
pip install rasa_nlu
pip install rasa_core
```

Please note that some nlu training data as well as most stories for the dialogue management have been removed for data protection reasons. This data is needed for training the respective components. To get this bot working properly you need to get more data for training. Put the stories in `app/data/core` and the nlu data in `app/data/nlu`.


## Overview of the files
`app` - contains all data and config files. Changes to the cui system should be made here

`app/data/core` - contains stories for Rasa Core

`app/data/nlu` - contains training data for Rasa NLU

`app/actions` - contains all files related to the Rasa Action server with the respective dbs

`app/domain.yml` - the domain file for Rasa Core

`app/config/nlu_tensorflow.yml` - the NLU config file

`app/config/endpoints.yml` - config file to define endpoints for tracker_store, nlu and action server

`app/config/endpoints_offline.yml` - alternative endpoint config file for offline usage

`app/config/policy_config.yml` - the config file for rasa policies (keras, fallback, memoization)

`app/core_agent` - website backend for usage without docker

`app/models` - trained models for nlu and dialoguemanagement

`app/static` - chatbot frontend

`rasa_core, rasa_nlu` - repositories for rasa nlu and core. Can be updated with newer versions of the respective repos if needed

`dialogue_log` - frontend and backend for logging component. For details about the component and how to install it please visit the respective  [Readme](/dialogue_log/Readme.md)


## Training without Docker
To train the core model: 

```
python3 bot.py train-dialogue
```

To train the NLU model: 

```
python3 bot.py train-nlu
```


## Train with Docker on Mac
Train Core
```
docker run -v $(pwd):/app/project -v $(pwd)/models/dialogue:/app/models rasa/rasa_core:latest train -c project/config/policy_config.yml --domain project/domain.yml --stories project/data/core/stories.md --out models
```

Train NLU
```
docker run -v $(pwd):/app/project -v $(pwd)/models/nlu:/app/models -v $(pwd)/config:/app/config rasa/rasa_nlu:latest run python -m rasa_nlu.train -c config/config_tensorflow.yml -d project/data/nlu/nlu.json -o models --fixed_model_name current
```


## Train with Docker on Windows
Train Core
```
docker run -v ${pwd}:/app/project -v ${pwd}/models/dialogue:/app/models rasa/rasa_core:latest train -c project/config/policy_config.yml --domain project/domain.yml --stories project/data/core/stories.md --out models
```

Train NLU
```
docker run -v ${pwd}:/app/project -v ${pwd}/models/nlu:/app/models -v ${pwd}/config:/app/config rasa/rasa_nlu:latest run python -m rasa_nlu.train -c config/config_tensorflow.yml -d project/data/nlu/nlu.json -o models --fixed_model_name current
```


Build Rasa-SDK docker image with custom compontents (needed for rasa actions)
```
cd actions
docker build -t rasa_core_sdk_hr .
```


## Evaluation
To evaluate the NLU model: 

```
python3 -m rasa_nlu.evaluate --config config/config_tensorflow.yml --data data/nlu/nlu.json --mode crossvalidation
```


## Interactive Learning
To start interactive learning
```
cd actions
```

```
python3 -m rasa_core_sdk.endpoint --actions actions
```

```
python3 -m rasa_core.train interactive -c config/policy_config.yml -u models/nlu/default/current/ -o models/dialogue -d domain.yml -s data/core/stories.md --endpoints config/endpoints_offline.yml --skip_visualization
```

To run the bot on the website install rasa-addons:
```
pip install rasa-addons
```

Start the action webserver
```
cd actions
```
```
python3 -m rasa_core_sdk.endpoint --actions actions
```

Serve the website containing the chat widget:
```
cd static
```
```
python3 -m http.server 5100
```

Launch the website backend:
```
cd core_agent
python3 website.py
```

The website can be found on http://localhost:5100/index.html


## Deployment
- Train NLU
- Train Core
- Start NLU, Core, MongoDB:
```
docker-compose up
```
- Start Frontend-Component
- Start Logging-Component


## Generated .md-files can be converted to json:
```
cd data

python3 -m rasa_nlu.convert --data_file nlu.md --out_file nlu2.json --format json
```

## Used libraries:
- [Rasa NLU][rasanlu]
- [Rasa Core][rasacore]
- [Rasa Python-SDK][rasasdk]
- [Rasa Addons][rasaaddons]
- [Rasa Webchat][webchat]
- [Chatroom][chatroom]

[rasanlu]: https://github.com/RasaHQ/rasa_nlu
[rasacore]: https://github.com/RasaHQ/rasa_core
[webchat]: https://github.com/mrbot-ai/rasa-webchat
[rasaaddons]: https://github.com/mrbot-ai/rasa-addons
[chatroom]: https://github.com/scalableminds/chatroom
[rasasdk]: https://github.com/RasaHQ/rasa_core_sdk