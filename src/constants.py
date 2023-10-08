import json


#hardcoded values here which i didnt bother to make dynamic because i dont care

xproperties = 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC43NiIsIm9zX3ZlcnNpb24iOiIxMC4wLjIyNjIxIiwib3NfYXJjaCI6Ing2NCIsImFwcF9hcmNoIjoiaWEzMiIsInN5c3RlbV9sb2NhbGUiOiJlbi1VUyIsImJyb3dzZXJfdXNlcl9hZ2VudCI6Ik1vemlsbGEvNS4wIChXaW5kb3dzIE5UIDEwLjA7IFdPVzY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBkaXNjb3JkLzEuMC43NiBDaHJvbWUvMTA4LjAuNTM1OS4yMTUgRWxlY3Ryb24vMjIuMy4yNCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMjIuMy4yNCIsImNsaWVudF9idWlsZF9udW1iZXIiOjIyODc4MSwibmF0aXZlX2J1aWxkX251bWJlciI6Mzc0MTEsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
useragent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.76 Chrome/108.0.5359.215 Electron/22.3.24 Safari/537.36'

config = json.load(open('config.json'))
redirect = config['redirect']
client_secret = config['client_secret']
client_id = config['client_id']

token_file = 'tokens.txt'
debug = True

#optium = ['discord.com','canary.discord.com','ptb.discord.com']
optium = ['discord.com','canary.discord.com','ptb.discord.com']

if redirect == '' or client_secret == '' or client_id == '':
    raise Exception('Please fill out the config.json file with your client id, client secret, and redirect uri - Switch')


if len(open(token_file).readlines()) == 0:
    raise Exception('Please add some tokens to tokens.txt - Switch')