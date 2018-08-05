
# Jaguar
A chat application

![Jaguar](https://img00.deviantart.net/0a9d/i/2010/343/9/6/jaguar_by_alannahily-d34ju3t.jpg)

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

messaging:
  default_messenger: restfulpy.messaging.SmtpProvider

smtp:
  host: mail.carrene.com
  port: 587
  username: nc@carrene.com
  password: <smtp-password>
  local_hostname: carrene.com
   
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


