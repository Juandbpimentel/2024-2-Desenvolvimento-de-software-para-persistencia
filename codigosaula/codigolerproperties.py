import configparser

config = configparser.ConfigParser()

config['DEFAULT'] = {
    'database':'database',
    'host':'localhost',
    'user':'root',
    'password':'ahnes'
}

with open('config.ini','w',encoding='utf-8') as file:
    config.write(file)
    
config.read('config.ini')
database = config['DEFAULT']['database']
user = config['DEFAULT'].get('user')
host = config['DEFAULT'].get('host')
password = config['DEFAULT']['password']

print(f"""
    database: {database}
    user: {user}
    host: {host}
    password: {password}
      """)