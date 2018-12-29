
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

##### NOTE: You need to have RabbitMQ installed on your machine. you can install it from [RabbitMQ guide](https://www.rabbitmq.com/install-debian.html).

### Install Project (edit mode)

#### Working copy

```bash

cd /path/to/workspace
git clone git@github.com:Carrene/jaguar.git
cd jaguar
pip install -e .

```
 
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

```bash

jaguar db create --drop --mockup

```

And or

```bash

jaguar db create --drop --basedata 

```

#### Drop old database: **TAKE CARE ABOUT USING THAT**

```bash

jaguar [-c path/to/config.yml] db --drop

```

#### Create database

```bash

jaguar [-c path/to/config.yml] db --create

```

Or, you can add `--drop` to drop the previously created database: **TAKE CARE ABOUT USING THAT**

```bash

jaguar [-c path/to/config.yml] db create --drop

```

### Testing the websocket server

To start the websocket server run the following command:

```bash

jaguar websocket start

```

To enqueue the message, run the following command:

```bash

./scripts/rabbitmq_enqueue_async.py <session_id> [payload]

```

The *session_id* is a required parameter which must be the same as *session_id* in the token payload.

The *payload*  is a optional parameter which has a default value. You can observe the default value by running: `jaguar -h`.

As a client you can recieve the message enqueued by the `wscat` cli app. Like:

```bash

wscat -c localhost:8085?token=<token>

```

