# tteokbokki-map-server
Tteokbokki Map API Server

---

- [how to setup](#how-to-setup)
  - [1. install python environment](#1-install-python-environment)
  - [2. clone and install requirements](#2-clone-and-install-requirements)
  - [3. set env](#3-set-env)
- [additional setup for crawler](#additional-setup-for-crawler)
  - [1. Download chromedriver](#1-download-chromedriver)
  - [2. Set API Key](#2-set-api-key)

---
# How to setup

#### 1. install python environment
There are multiple ways to get python environments.
1. pyenv
2. venv
3. pipenv

#### 2. clone and install requirements
```bash
git clone https://github.com/siner308/ttbkk-server
cd ttbkk-server
pip install -r requirements.txt
```

#### 3. set env
1. Copy `env.sample.py` to `env.py`
    ```bash
    cp env.sample.py env.py
    ```
2. Set env
    - Fill environments in your `env.py`

# Additional setup for crawler

#### 1. Download chromedriver
1. [Download](https://chromedriver.chromium.org/) chromedriver that suit with your os and chrome version.
2. Locate chromedriver to your project root.
   - For example: `./ttbkk-server/chromedriver`
3. Fix your `env.py`
    ```python
    # env.py
    CHROMEDRIVER_PATH = './chromedriver'
    ```
   
#### 2. Set API Key
1. Set [Google API Key](https://mapsplatform.google.com/)
2. Set [Kakao API Key](https://apis.map.kakao.com/web/guide/)
3. Fix your `env.py`
    ```python
    GOOGLE_MAP_KEY = ''
    KAKAO_API_KEY = ''
    ```
