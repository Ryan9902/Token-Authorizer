import tls_client
import time
from src.ui import Log
from src.constants import xproperties , useragent , redirect , client_secret , client_id , token_file , optium
import os 
from concurrent.futures import ThreadPoolExecutor , as_completed
from src.util import get_addr
import random
from threading import Thread ,  Lock , Timer
import ctypes
import sys





os.system('cls' if os.name == 'nt' else 'clear')

total = len(open(token_file).readlines())
failed , success = 0 , 0
start_time = time.time()
authing = True
Log.Info(f"Starting | Tokens: {len(open(token_file).readlines())}")
Log.Debug(f"Client ID: {client_id} | Client Secret: {client_secret} | Redirect: {redirect}")

#canary.discord.com , discord.com , ptb.discord.com <- these are the domains that discord uses for oauth2 so you can use any of them
# Made by Switch <3

class Title:
    def __init__(self):
        self.lock = Lock()
        self.update_title()

    def update_title(self):
            try:
                title = f'Switch G | Success: {success} | Failed: {failed} | Elapsed: {round(time.time() - start_time, 2)}s'
                if sys.platform not in ('linux', 'darwin'):
                    ctypes.windll.kernel32.SetConsoleTitleW(title)
            except:
                pass
            
            if success + failed == total:
                return
            
            if authing:
                Timer(0.1, self.update_title).start()
            else:
                return
            




class Authorize:
    def __init__(self,client_id :str , redirect:str , clientkey:str , token:str) ->None:


        self.tkn_ = token.strip()

        
        if ':' in token:
            token=token.split(':')[2]
        



        self.token = token.strip('\n')
         #discord uses these domains for oauth2 so you can use any of them
        self.domain = random.choice(optium)
        self.headers = {
                    "Authorization": self.token,
                    "Origin": "https://" + self.domain,
                    "Accept": "*/*",
                    "X-Discord-Locale": "en-US",
                    "X-Super-Properties": xproperties,
                    "User-Agent": useragent,
                    "X-Debug-Options": "bugReporterEnabled",
                    "Content-Type": "application/json"
            }
            
        
        self.client_id = client_id
        self.redirect = redirect
        self.clientkey = clientkey
        
        self.authurl = f"https://{self.domain}/api/oauth2/authorize?client_id={self.client_id}&redirect_uri={self.redirect}&response_type=code&scope=identify%20guilds.join"
        self.session  = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
            )
        self.session.headers['Accept-Encoding'] = 'deflate' #discord doesnt like gzip from tls_client for some reason so we use deflate instead
        
    



    def authorize(self)->bool:
        global failed , success 
        #ik its gross to use global in a class i could have passed it as a parameter but i was lazy
        while True:
            try:
                r = self.session.post(self.authurl, json={"authorize": "true"} , headers=self.headers)
                break
            except Exception as e:
                Log.Debug(f'Exception in Authorize.authorize() : {e} | [Retry]')
                continue
        
        if r.status_code == 500:
            Log.Info(f"Retrying to Auth <- {self.token} [500]")
            self.authorize()

        if r.status_code == 429 :
            if 'cloudflare' in r.text:
                Log.Info(f"Retrying to Auth <- {self.token} [Cloudflare] {r.status_code}")


            time.sleep(2)
            return self.authorize()
        

        if r.status_code in (200, 201, 204):
            try:
                r.json()
            except:
                
                Log.Error(f"Failed to Auth <- {self.token} [No Json] {r.status_code} {r.text}")
                with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                    f.write(self.tkn_ + "\n")
                
                failed += 1
                return
    
            location = r.json()['location']
            try:
                code = location.split("code=")[1]
            except:
                Log.Error(f"Failed to Auth <- {self.token} {r.text}")
                return


        elif r.status_code == 429 :
            try:
                r.json()
            except:
                Log.Error(f"Failed to Auth <- {self.token} [No Json] {r.status_code} {r.text}")
                with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                    f.write(self.tkn_ + "\n")

                return
            time.sleep(int(r.json()['retry_after']))
            return self.authorize()
        elif r.status_code == 401:
            Log.Error(f"Failed to Auth <- {self.token} [401][Invalid/Locked]")
            with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                f.write(self.tkn_ + "\n")
                failed += 1
            return False
        else:
            Log.Error(f"Failed to Auth <- {self.token} {r.status_code} {r.text}")
            with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                f.write(self.tkn_ + "\n")
                failed += 1
            return False


        while True:
            try:
                r = self.session.post(f"https://{self.domain}/api/v9/oauth2/token", data={'client_id': self.client_id,'client_secret': self.clientkey,'grant_type': 'authorization_code','code': code,'redirect_uri': self.redirect}, headers={'Content-Type': 'application/x-www-form-urlencoded'})
                break
            except Exception as e:
                Log.Debug(f'Exception in Authorize.authorize() : {e} | [Retry]')
                continue
        

        if r.status_code == 429: 
            if 'cloudflare' in r.text:
                Log.Error(f"Retrying to Auth <- {self.token} [Cloudflare] {r.status_code}")
            

            time.sleep(2)
            return self.authorize()
        
        if r.status_code == 500:
            Log.Info(f"Retrying to Auth <- {self.token} [500]")
            self.authorize()

        if r.status_code in (200, 201, 204):
            try:
                r.json() #ik could have checked for response header content-type but this is easier
            except:

                Log.Error(f"Failed to Auth <- {self.token} [No Json] {r.status_code} {r.text}")
                with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                    f.write(self.tkn_ + "\n")
                
                failed += 1
                return

            access_token , refresh_token = r.json()['access_token'] , r.json()['refresh_token']
        else:
            Log.Error(f"Failed to Auth <- {self.token} {r.status_code}  ")
            with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                f.write(self.tkn_ + "\n")
            failed += 1
            return False
        
        userid = get_addr(self.token)

        if not userid:

            while True:
                try:
                    r = self.session.get(f"https://{self.domain}/api/v9/users/@me", headers={"Authorization": f"Bearer {access_token}"})
                    break
                except Exception as e:
                    Log.Debug(f'Exception in Authorize.authorize() : {e} | [Retry]')
                    continue
            if r.status_code == 500:
                Log.Info(f"Retrying to Auth <- {self.token} [500]")
                self.authorize()


            if r.status_code == 429 :
                if 'cloudflare' in r.text:
                    Log.Error(f"Retrying to Auth <- {self.token} [Cloudflare] {r.status_code}")
                

                time.sleep(2)
                return self.authorize()
            

            if r.status_code in (200, 201, 204):
                try:
                    r.json()
                except:

                    Log.Error(f"Failed to Auth <- {self.token} [No Json] {r.status_code} {r.text}")
                    with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                        f.write(self.tkn_ + "\n")
                    
                    failed += 1
                    return

                userid = r.json()['id']
            else:
                Log.Error(f"Failed to Auth <- {self.token} {r.status_code}  ")
                with open('output/failed_auths.txt' , 'a',encoding='utf-8') as f:
                    f.write(self.tkn_ + "\n")
                failed += 1
                return False
            
        success += 1
        Log.Success(f"Authorized <- {self.token[:50]}xxxxxxxxx  | {userid}")
        return  userid , access_token , refresh_token
            

def submit(token, lock):
    token_main = token.strip()
    try:
        token = token.split(':')[2].strip() if ':' in token else token.strip() 
        s = Authorize(client_id , redirect , client_secret , token.strip()).authorize()
        if s is False:
            return
        with lock:
            with open('output/auths.txt', 'a', encoding='utf-8') as sax:
                sax.write(f"{s[0]}:{s[1]}:{s[2]}\n")
            with open('output/tokens_authed.txt', 'a', encoding='utf-8') as niget:
                niget.write(token_main + "\n")

            with open('output/reaction_format.txt' , 'a',encoding='utf-8') as uwu:
                uwu.write(f"{s[0]}:{s[1]}:{s[2]}:{token}\n")


    except Exception as e:
        Log.Error(f"Exception in submit() : {e}")
        return False

def main() -> None:
    with open(token_file, 'r', encoding='utf-8') as file:
        tokens = file.readlines()

    lock = Lock() 
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(submit, token, lock) for token in tokens]
        for future in as_completed(futures):
            result = future.result()


if __name__ == "__main__":
    Thread(target=Timer(0.1, Title).start()).start()
    main()
    authing = False
    Log.Info(f"Finished | Success: {success} | Failed: {failed}| Elapsed: {round(time.time() - start_time, 2)}s")
