## rtscli - Realtime Stock Ticker CLI
<a target="_blank" href="https://opensource.org/licenses/MIT" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a> <a target="_blank" href="http://makeapullrequest.com" title="PRs Welcome"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>

- A stock ticker that runs in console

- It grabs info from several APIs and displays it in a nice UI

- It's pretty simple but if you wanna read through a blog post instead: https://aranair.github.io/posts/2017/06/28/building-a-python-cli-stock-ticker-with-urwid/

## Flow Diagram

```
[Start]
   |
   v
[Initialize variables]
   |
   v
[Enter main loop]
   |
   v
[Attempt Alpha Vantage API]
   |
   +---> [Success] --> [Process data]
   |
   +---> [Failure] --> [Switch to Polygon API]
                          |
                          v
                       [Attempt Polygon API]
                          |
                          +---> [Success] --> [Process data]
                          |
                          +---> [Failure] --> [Log error]
   |
   v
[Update UI]
   |
   v
[Wait for refresh interval]
   |
   v
[Repeat main loop]
```

**NOTE!!**
This uses https://www.alphavantage.co because Google Finance does not seem to work reliably anymore (IPs get blocked and it just plain out doesn't work), and also the Polygon API is a bit more reliable.

You can get a free API key with a limited number of queries per second and so this has been tweaked to just refresh every 60s now. Put the api-key into `alphavantage-creds.txt` or 'polygon-creds.txt' and it should work.

## Screenshot

![Demo](https://github.com/aranair/rtscli/blob/master/rtscli-demo.png?raw=true "Demo")

## Dependencies

Currently this is dependent on

- Python2.7
- pip
- Bunch of other python packages

## Install via Pip
There is a pip package available for this, but it is outdated.
```
pip install rtscli
```

## Running it

```bash
$ cp tickers.txt.sample tickers.txt
$ python rtscli.py
```

## Tickers.txt Sample

Format: Name, Ticker(Alphavantage format), cost price, shares held

```
GLD,GLD,139,1
```

## Downloading and building manually

```
$ git clone git@github.com:aranair/rtscli.git
$ pip install -e .
$ rtscli
```

## License

MIT
