import urwid
import requests
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
try:
    # For Python3.0 and later
    from html.parser import HTMLParser
except ImportError:
    # Fall back to Python 2's HTMLparser
    from HTMLparser import HTMLparser
from simplejson import loads
from time import sleep


def parse_lines(lines):
    for l in lines:
        ticker = l.strip().split(",")
        yield ticker

# Read files and get symbols

with open("tickers.txt") as file:
    tickers = list(parse_lines(file.readlines()))


with open("alphavantage-creds.txt") as file:
    apikey = list(parse_lines(file.readlines()))[0]
    

with open("polygon-creds.txt") as file:
    polygon_apikey = list(parse_lines(file.readlines()))[0]


# Set up color scheme
palette = [
    ('titlebar', 'dark red', ''),
    ('refresh button', 'dark green,bold', ''),
    ('quit button', 'dark red', ''),
    ('getting quote', 'dark blue', ''),
    ('headers', 'white,bold', ''),
    ('change ', 'dark green', ''),
    ('change negative', 'dark red', ''),
    ('error', 'light red', ''),
    ]

header_text = urwid.Text(u' Stock Quotes')
header = urwid.AttrMap(header_text, 'titlebar')

# Create the menu
menu = urwid.Text([
    u'Press (', ('refresh button', u'R'), u') to manually refresh. ',
    u'Press (', ('quit button', u'Q'), u') to quit.'
])

# Create the quotes box
quote_text = urwid.Text(u'Press (R) to get your first quote!')
quote_filler = urwid.Filler(quote_text, valign='top', top=1, bottom=1)
v_padding = urwid.Padding(quote_filler, left=1, right=1)
quote_box = urwid.LineBox(v_padding)

# Assemble the widgets
layout = urwid.Frame(header=header, body=quote_box, footer=menu)

def pos_neg_change(change):
    if not change:
        return "0"
    else:
        return ("+{}".format(change) if change >= 0 else str(change))

def get_color(change):
    color = 'change '
    if change < 0:
        color += 'negative'
    return color

def append_text(l, s, tabsize=10, color='white'):
    l.append((color, s.expandtabs(tabsize)))

def calculate_gain(price_in, current_price, shares):
    gain_per_share = float(current_price) - float(price_in)
    gain_percent = round(gain_per_share / float(price_in) * 100, 3)

    return gain_per_share * int(shares), gain_percent

#Get Stock Data Update
def get_update():
    results = []
    use_polygon = False  # Initialize use_polygon at the beginning of the function
    
    try:
        for t in tickers:
            ticker_sym = t[1]
            if not use_polygon:
                # Alpha Vantage API call
                url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker_sym}&apikey={apikey}"
                response = urlopen(url)
                res = loads(response.read())
                if "Global Quote" in res and res["Global Quote"]:
                    results.append(res["Global Quote"])
                else:
                    print(f"Unexpected response from Alpha Vantage for {ticker_sym}: {res}")
                    use_polygon = True  # Switch to polygon.io if Alpha Vantage fails
            
            if use_polygon:
                # Polygon.io API call
                url = f"https://api.polygon.io/v2/aggs/ticker/{ticker_sym}/prev?apiKey={polygon_apikey}"
                response = requests.get(url)
                res = response.json()
                if "results" in res and res["results"]:
                    polygon_data = res["results"][0]
                    results.append({
                        "01. symbol": ticker_sym,
                        "05. price": str(polygon_data["c"]),
                        "09. change": str(polygon_data["c"] - polygon_data["o"]),
                        "10. change percent": f"{((polygon_data['c'] - polygon_data['o']) / polygon_data['o'] * 100):.2f}%"
                    })
                else:
                    print(f"Unexpected response from Polygon.io for {ticker_sym}: {res}")

        if not results:
            return [('error', "No valid results obtained. Please check your tickers and try again.")]

        updates = [
            ('headers', u'Stock \t '.expandtabs(25)),
            ('headers', u'Last Price \t Change '.expandtabs(5)),
            ('headers', u'\t % Change '.expandtabs(5)),
            ('headers', u'\t Gain '.expandtabs(3)),
            ('headers', u'\t % Gain \n'.expandtabs(5))]

        total_portfolio_change = 0.0

        for i, r in enumerate(results):
            pass  # Add your logic here

        updates.append(('', '\n\n\nNet Portfolio Gain: '))
        updates.append((get_color(total_portfolio_change), pos_neg_change(total_portfolio_change)))

        return updates

    except Exception as err:
        print(f"Error in get_update: {err}")
        return [('error', f"Error fetching data: {err}. Please try again later.")]

# Handle key presses
def handle_input(key):
    if key == 'R' or key == 'r':
        refresh(main_loop, '')

    if key == 'Q' or key == 'q':
        raise urwid.ExitMainLoop()

#Refresh
def refresh(_loop, _data):
    main_loop.draw_screen()
    update_data = get_update()
    if isinstance(update_data, list) and update_data:
        quote_box.base_widget.set_text(update_data)
    else:
        quote_box.base_widget.set_text([('error', "Unable to fetch updates. Please try again later.")])
    main_loop.set_alarm_in(60, refresh)


main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)

def cli():
    main_loop.set_alarm_in(0, refresh)
    main_loop.run()
cli()
