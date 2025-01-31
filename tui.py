#rich imports
from rich import print #as rprint
from rich.console import Console
from rich.layout import Layout
from rich.table import Table
from rich.panel import Panel
from rich.live import Live
from time import sleep

#bs4 imports
from bs4 import BeautifulSoup
import requests
import re #regular expression

#scraper
url = "https://hackaday.com/"

result = requests.get(url)
site = BeautifulSoup(result.text, "html.parser")

#class for blog
class Post:
    def __init__(self, title, author, link, date):
        self.title = title
        self.author = author
        self.link = link
        self.date = date

    def display(self):
        print(f"\"{self.title}\" \n by {self.author} \n {self.link} \n {self.date}")

titles=[]
links=[]
dates=[]
authors=[]

for tag in site.find_all("div", {"class":"entry-intro"}):
    # find...
    # title
    for title in tag.find_all("h2"):
        if title.string != None:
            #print(title.string)
            titles.append(title.string)
    # link
            for link in tag.find_all("a"):
                #print(link["href"])
                links.append(link["href"])
                break
    # post date
            for date in tag.find_all("span", {"class":"post-date"}):
                if date.string != None:
                    #print(date.string)
                    dates.append(date.string)
    # author
            for author in tag.find_all("a", {"rel":"author"}):
                #print(author.string)
                authors.append(author.string)

# create console object for tui
console = Console()

# layout structure
def create_layout():
    layout = Layout()
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=2),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="table")
    )
    return layout

# header
def render_header():
    return Panel(":wrench: [bold yellow]hackaday blog posts[/] :robot:", style="cyan")

# table 
def render_table():
    table = Table(title="recent posts")
    table.add_column("title", justify="center", style="cyan", no_wrap=True)
    table.add_column("author", justify="center", style="magenta")
    table.add_column("link", justify="center", style="green")
    table.add_column("date", justify="center", style="red")
    #table.add_column("image", justify="center", style="green")

    count = 0
    for i in titles:
        my_post = Post(titles[count], authors[count], links[count], dates[count])
        table.add_row(f"\"{my_post.title}\"", my_post.author, my_post.link, my_post.date)
        count += 1
    return table

# right section
def render_right():
    return Panel("[bold magenta] right panel /]\n\n idk what to put here", style="cyan")

# footer
def render_footer():
    return Panel(":bone: :dog: [bold purple] deadnintendog waz here [/] :paw_prints: :sparkles:", style="red")

# create / display tui
def main():
    layout = create_layout()
    layout["header"].update(render_header())
    layout["table"].update(render_table())
    #layout["right"].update(render_right()) #idk what i would want here
    layout["footer"].update(render_footer())

    # refresh / update
    with Live(layout, refresh_per_second=4, screen=True):
        for _ in range(15):
            sleep(1)
            
if __name__ == "__main__":
    main()
