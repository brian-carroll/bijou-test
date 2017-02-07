Installation
------------
This project is written in Python 3.4 and depends on Scrapy.

Scrapy can be a bit tricky to install, and varies by OS.

To install on Ubuntu 14.04:
```
sudo apt-get install python3-lxml zlib1g-dev libxml2-dev libxslt-dev python-dev libssl-dev libffi-dev

virtualenv -p /usr/bin/python3 venv

venv/bin/pip install -r requirements.txt
```

Or just run the `install.sh` script provided.

If you have a different OS, you may need to look at the
[Scrapy installation instructions](https://doc.scrapy.org/en/latest/intro/install.html) and modify accordingly.
