import os

from jaguar import jaguar as app


home_directory = os.environ['HOME']
configuration_file_name=f'{home_directory}/.config/jaguar.yml'


app.configure(filename=configuration_file_name)
app.initialize_orm()

