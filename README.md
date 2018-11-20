
# Jaguar
A chat application

![Jaguar](https://img00.deviantart.net/0a9d/i/2010/343/9/6/jaguar_by_alannahily-d34ju3t.jpg)

## Branches

### master

[![Build Status](https://travis-ci.com/Carrene/jaguar.svg?token=JgyQwxgapUeYpgeJwWxz&branch=master)](https://travis-ci.com/Carrene/jaguar)
[![Coverage Status](https://coveralls.io/repos/github/Carrene/jaguar/badge.svg?branch=master&t=JBn3pI)](https://coveralls.io/github/Carrene/jaguar?branch=master)

Setting up development Environment on Linux
----------------------------------

### Install Project (edit mode)

#### Working copy
    
    $ cd /path/to/workspace
    $ git clone git@github.com:Carrene/jaguar.git
    $ cd jaguar
    $ pip install -e .
 
### Setup Database

#### Configuration

```yaml

db:
  url: postgresql://postgres:postgres@localhost/jaguar_dev
  test_url: postgresql://postgres:postgres@localhost/jaguar_test
  administrative_url: postgresql://postgres:postgres@localhost/postgres

oauth:
  secret: A1dFVpz4w/qyym+HeXKWYmm6Ocj4X5ZNv1JQ7kgHBEk=\n
  application_id: 1
  url: http://localhost:8080

storage:
  local_directory: %(root_path)s/data/assets
  base_url: http://localhost:8080/assets
  
 ```

#### Remove old abd create a new database **TAKE CARE ABOUT USING THAT**

    $ jaguar db create --drop --mockup

And or

    $ jaguar db create --drop --basedata 

#### Drop old database: **TAKE CARE ABOUT USING THAT**

    $ jaguar [-c path/to/config.yml] db --drop

#### Create database

    $ jaguar [-c path/to/config.yml] db --create

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

    $ jaguar [-c path/to/config.yml] db create --drop

