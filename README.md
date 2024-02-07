# Initialization

1. Install pip, [RASA](https://rasa.com/docs/rasa/installation/environment-set-up), [hugchat](https://pypi.org/project/hugchat/)
2. Init python venv `python3 -m venv ./venv`
3. Create a Hugging Face account and input your login data in [actions.py](./actions/actions.py)
4. Train rasa `rasa train`
5. Run rasa `rasa shell` and the action server in a new shell `rasa run actions`
6. Start chatting 🤖
