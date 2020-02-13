"""
TODO
- Search proxies by type e.g elite, anonyumous
- search proxies by country
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, JavascriptException

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import time
import random
import threading
import ipaddress

from bs4 import BeautifulSoup as b4



class ProxyReaper:
    
    def __init__(self, proxy_count=None):
        self.proxy_list = []
        self.chrome_options = webdriver.ChromeOptions()       
        chromedriver_path = self.get_chromedriver_path()
        self.chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome(chromedriver_path, chrome_options=self.chrome_options)
        self.first_run = True
        self.page_count = 1
        self.max_page_count = 10
        self.semap = threading.Semaphore(3)
        self.proxy_count = proxy_count
        
    def get_chromedriver_path(self):
             
        if sys.platform == "darwin":
            chrome_driver = "chromedriver_mac"
        elif sys.platform == "linux":
            chrome_driver = "chromedriver_linux"
        else:
            chrome_driver = "chromedriver_win"
            
        return "./chromedrivers/"+chrome_driver
    
    def suck_proxies(self, html_doc):
        print("[+] Sucking proxies....")
        f = b4(html_doc, 'html.parser')
        tds = f.find_all('td')
        count = 0
        
        while count < len(tds):
            try:
                ip = ipaddress.ip_address(tds[count].string)               
            except ValueError:
                pass
            else:
                valid_ip = "{0}:{1}".format(tds[count].string, tds[count+1].string)
                self.proxy_list.append(valid_ip)
            
            count += 1
               
     
    def gather_proxy(self, proxy_type="elite"):
        print("[+] [GetherProxy.com]Getting proxies....")
        
        if proxy_type == "elite":
            self.browser.get("http://www.gatherproxy.com/proxylist/anonymity/?t=Elite")
        elif proxy_type == "transparent":
            self.browser.get("http://www.gatherproxy.com/proxylist/anonymity/?t=Transparent")
            

        time.sleep(5)
        try:       
            output = self.browser.execute_script("return document.getElementsByTagName('table')[0].innerHTML")
            self.suck_proxies(output)
            if len(self.proxy_list) > 0:
                print("[+] Done!")
                return True
        except:
            return None


    def free_proxy_list(self):
        print("[+] [https://free-proxy-list.net] Getting proxies...")
        try:
            self.browser.get("https://free-proxy-list.net")
            time.sleep(5)
            output = self.browser.execute_script("return document.getElementsByTagName('table')[0].innerHTML")
            self.suck_proxies(output)
            
            if len(self.proxy_list) > 0:
                print("[+] Done!")
                return True
        except:
            return None
    
        
        
    def get_proxies(self):
        gather_output = self.gather_proxy()
        
        if gather_output == None:
            print("[-] [https://gatherproxy.com] FAILED")
            free_output = self.free_proxy_list()

            if free_output == None:
                print("[-] [https://free-proxy-list.net] FAILED")
            
        self.browser.quit()
        
    def get_proxy_list(self):
        if self.proxy_count != None:
            return self.proxy_list[:10]
        return self.proxy_list
        


if __name__ == '__main__':
    d = ProxyReaper(10)
    d.get_proxies()
    print(d.get_proxy_list())   
