# tteokbokki-map-server
Tteokbokki Map API Server

---

- [For ttbkk-web Contributors](#for-ttbkk-web-contributors)
- [How to setup](#how-to-setup)
  - [1. Install python environment](#1-install-python-environment)
  - [2. Clone and install requirements](#2-clone-and-install-requirements)
  - [3. Set env](#3-set-env)
  - [4. Launch for server](#4-launch-for-server)
- [Additional setup for crawler](#additional-setup-for-crawler)
  - [1. Download chromedriver](#1-download-chromedriver)
  - [2. Set API Key](#2-set-api-key)
  - [3. Launch for crawler](#3-launch-for-crawler)

---
# For ttbkk-web contributors
Here is always usable develop stage ttbkk-server for [ttbkk-web](https://github.com/siner308/ttbkk-web) contributor.

You **don't need to run this server** for your client development.<br>
Just fill text like below in your .env file in ttbkk-web project.

```text
REACT_APP_API_HOST=https://dev-api.ttbkk.com
```

# How to setup

#### 1. Install python environment
There are multiple ways to get python environments.
1. pyenv
2. venv
3. pipenv

#### 2. Clone and install requirements
```bash
git clone https://github.com/siner308/ttbkk-server
cd ttbkk-server
pip install -r requirements.txt
```

#### 3. Set env
1. Copy `env.sample.py` to `env.py`
    ```bash
    cp env.sample.py env.py
    ```
2. Set env
    - Fill environments in your `env.py`

#### 4. Launch for server
> Before launch, you need to setup mysql database.

```bash
python3 manage.py migrate
python3 manage.py runserver 0.0.0.0:8000
```

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

#### 3. Launch for crawler
0. Setup database
    > Before launch, you need to setup mysql database.

1. Select targets you want to scrap.
    ```python
    # src.crawlers.main.py:

    def run():
        crawlers = get_crawlers([
            # FranchiseType.SINJEON,
            # FranchiseType.GAMTAN,
            # FranchiseType.YUPDDUK,
            # FranchiseType.BAEDDUCK,
            # FranchiseType.MYUNGRANG,
            # FranchiseType.YOUNGDABANG,
            # FranchiseType.SINCHAM,
            # FranchiseType.SINBUL,
            # FranchiseType.EUNGDDUK,
            # FranchiseType.JAWSFOOD,
            # FranchiseType.TTEOKCHAM,
            # FranchiseType.SAMCHEOP,
            # FranchiseType.DALDDUK,
            # FranchiseType.DOOKKI
            FranchiseType.KANG
        ])
        for crawler in crawlers:
            crawler.run()
    ```

2. Move into django shell
    ```bash
    # in bash
    python3 manage.py migrate
    python3 manage.py shell
    ```

3. Run script
    ```python3
    # in python shell
    >>> from src.crawlers.main import run
    >>> run()
    ```