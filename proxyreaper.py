"""
TODO
- Search proxies by type e.g elite, anonyumous
- search proxies by country
"""

from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import sys
import re
import time
import random
import threading
import ipaddress

from bs4 import BeautifulSoup as b4



class ProxyReaper:
    
    def __init__(self, proxy_count=None, headless=False):
        self.proxy_list = []
        self.chrome_options = webdriver.ChromeOptions()       
        chromedriver_path = self.get_chromedriver_path()
        
        if headless == True:
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
        """
        @summary - mines proxy data from given html code
        @html_doc - the source to mine from
        @returns - gets proxies and appends it to self.proxy_list 
        """
        
        f = b4(html_doc, 'html.parser')
        tds = f.find_all('td')
        count = 0
        
        while count < len(tds):
            try:
                print(ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}', tds[count] ))
                # ip = ipaddress.ip_address(tds[count])
                
                sys.exit()               
            except ValueError:
                pass
            else:
                valid_ip = "{0}:{1}".format(tds[count].string, tds[count+1].string)
                self.proxy_list.append(valid_ip)
                
        
            count += 1
            
    def suck_proxies2(self):
        ips_list = self.browser.execute_script("""
                                                         
                                                         ips_list = []
                                                         tds = document.getElementsByTagName('td')
                                                         function ValidateIPaddress(ipaddress) 
                                                            {
                                                            if (/^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/.test(ipaddress))
                                                            {
                                                                return true
                                                            }
                                                            
                                                            return false
                                                            }
                                                        
                                                        for (var i = 0; i < tds.length; i++){
                                                            
                                                            if (ValidateIPaddress(tds[i].innerText)){
                                                                ips_list.push(tds[i].innerText+":"+tds[i+1].innerText)
                                                            }
                                                        }
                                                        
                                                        return ips_list
                                                        
                                                         """)
                    
        self.proxy_list += ips_list
               
     
    def gather_proxy(self, proxy_type="elite"):
        """
        @summary - gathers proxies fro gatherproxy.com website
        @returns - nothing but proxies
        """
        print("[+] [GetherProxy.com]Getting proxies....")
        
        if proxy_type == "elite":
            self.browser.get("http://www.gatherproxy.com/proxylist/anonymity/?t=Elite")
        elif proxy_type == "transparent":
            self.browser.get("http://www.gatherproxy.com/proxylist/anonymity/?t=Transparent")
            
            
        
        try:
            commands = """
            show_full_list = document.getElementsByTagName('input')[0]
            if (show_full_list.value == "Show Full List"){
                show_full_list.click()
            }    
            """
            self.browser.execute_script(commands)
            time.sleep(2)
        except JavascriptException:
            return False
        else:
            maximum_page = int(self.browser.execute_script("return document.getElementsByClassName('inactive').length")) + 1
            current_page = 1
            while True:
                
                # Suck proxies from here
                try:       
                    self.suck_proxies2() 
                    
                    if self.proxy_count != None:                 
                        if len(self.proxy_list) >= self.proxy_count:
                            print("[+] Done!")
                            break
                except JavascriptException:
                    print("[-142-] JS Error")
                    break
                
                
                if current_page == (maximum_page-1):
                    break
                else:
                    try:
                        current_page += 1
                        commands = "return document.getElementsByClassName('inactive')[%d].click()" % current_page
                        self.browser.execute_script(commands)
                        time.sleep(2)
                    except JavascriptException:
                        break
            
            if len(self.proxy_list) > 0:
                return True
            else:
                return False


    def free_proxy_list(self):
        print("[+] [https://free-proxy-list.net] Getting proxies...")
        try:
            self.browser.get("https://free-proxy-list.net")
            time.sleep(5)
            
            while True:
                
                self.suck_proxies2()
                
                # Check if the next button is disabled
                next_disabled = self.browser.execute_script(
                    """
                    shhs = document.getElementById("proxylisttable_next").classList;
                    return shhs.contains("disabled");    
                    """
                )
                
                if next_disabled == True:
                    break
                else:
                    # Go to next table and suck em proxies 
                    self.browser.execute_script(
                    """
                    document.getElementById("proxylisttable_next").click()    
                    """
                )
                    time.sleep(1)
                    
                    
            
            if len(self.proxy_list) > 0:
            
                return True
        except:
            return False
    
        
        
    def get_proxies(self):
        gproxy_status = self.gather_proxy()
        
        if (gproxy_status):
            print("[*] [gatherproxy.com] Operation complete...")
        else:
            print("[-] [gatherproxy.com] Operation failes. Going to next site...")
            fproxy_status = self.free_proxy_list
            
            if fproxy_status:
                print("[*] [free-proxy-list.net] Operation complete...")
            else:
                print("[*] [free-proxy-list.net] Operation failed. Exiting....")
                
        
        self.browser.quit()
            
        
    def get_proxy_list(self):
        if self.proxy_count != None:
            return self.proxy_list[:10]
        return self.proxy_list
        


if __name__ == '__main__':
    d = ProxyReaper(headless=True)
    d.get_proxies()
    print(d.get_proxy_list())   
