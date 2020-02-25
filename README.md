
![Grim Reaper No Background](https://github.com/blackgeneration/Proxychilli/blob/master/images/proxychilli.png)

# Proxychilli v1.15
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
python proxychilli.py
```

### You can it in scripts

```
from proxychilli import ProxyChilli

obj = ProxyChilli(10)
action = obj.get_proxies()
proxylist = action.get_proxy_list()
```

### Headless mode aka Silent Mode

This mode doesnt show whats happening under the hood. Its enabled by default.

```
from proxychilli import ProxyChilli

obj = ProxyChilli(10, headless=True)
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


"We teh future"
