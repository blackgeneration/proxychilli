
![Grim Reaper No Background](https://github.com/blackgeneration/Proxyreaper/blob/master/0942fa87835fdb2cc3c6c2db9300750c-removebg-preview.png)

# Proxyreaper v1.15
A proxy scrapping tool

### Dependencies

- beautifulsoup4
- ipaddress
- selenium

### How to install 

```
pip -r requirements.txt
```

```
python proxyreaper.py
```

### You can it in scripts

```
from proxyreaper import ProxyReaper

obj = ProxyReaper(10)
action = obj.get_proxies()
proxylist = action.get_proxy_list()
```

### Headless mode aka Silent Mode

This mode doesnt show what happening under the hood. Its enabled by default.

```
from proxyreaper import ProxyReaper

obj = ProxyReaper(10, headless=True)
action = obj.get_proxies()
proxylist = action.get_proxy_list()
```


From here.......i will leave you to it.

### To do

- [ ] Add 2 more sites to the list
- [ ] House cleaning
- [ ] Gather proxies by type
- [ ] Gather proxies by time posted
- [ ] Gather proxies by country
- [ ] Gather proxies by https/http
- [ ] Store and reuse later

# DONT ABUSE MY TOOL
