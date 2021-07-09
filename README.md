# Student loyalty and reward management System
![Badges](https://img.shields.io/badge/Powerd%20By-Django-blue.svg)
![Badges](https://img.shields.io/github/license/mashape/apistatus.svg)
![Badges](https://img.shields.io/badge/Powered%20By-brownie-blue)
![Badges](https://img.shields.io/badge/Protocol-ERC20-green)
![Badges](https://img.shields.io/badge/Database-postgresql-blue)

>Notice: Project has not been completely developed yet. It's in phase3 development and integration of web3 components to the web application

## What's this?
This is a reward management system powered by `Django`, `ERC20` and `Brownie`. To collect the custom crypto tokens, they have to contribute articles to thepage or complete the milestones or assignmentscreated by the students' respective faculty. Article posts can be based on any topic that intrigues oneself, based on the popularity of the article the author receives the tokens from the project developers and could even receive the tokens as a tip from avid readers.

## Features
- Personalized user page.
- Multi-user、multi-role permission management system.
- create Articles
- create quizzes and Assignments
- custom edits on articles, quizzes, and assignments
- deploy custom token 
- Common forum's functions:
    + Register, login/logout, reset the password, email confirm.
    + Post, reply, comment.
    + Add co-author, tag.
    + search using (#,@)

## Features(under development)
- Scalable multi-node system.
- Follow, collect, and get the dynamic news.
- Restful API.
- Common web3 functions (internal wallet):
    + fetch account details
    + share the account address
    + transfer the custom token
    + make transactions

## How to use?
1. Clone this repository into your computer.

2. create the virtual environment.
    ```bash
    virtualenv venv
    # activate the virtual env
    venv\Scripts\activate.bat # for windows
    source venv/bin/activate # for ubuntu or ios systems
    ```

3. To create and deploy custom ERC20 contract
   ```bash
    pip install brownie

    # to deploy your new custom ERC20 token change the token name and symbol in'deploy_vtoken.py'
    # and add private key of external wallet and infura project key to '.env'

    brownie run scripts/deploy_vtoken.py --network kovan
    ```
4. Get dependencies(recommend):
    ```bash
    pip install -r requirements.txt
    ```
5. Now plug the database 
    >First create the database in PostgreSQL
    
    > add the database name, user, and password in `settings.py`

6. Startup:
    ```bash
    python manage.py runserver
    ```
7. Create an administrator user:
    ```bash
    python manage.py createsuperuser
    ```

## What's more
Welcome to issue some problems that you find in this project. I appreciate your work very much!
