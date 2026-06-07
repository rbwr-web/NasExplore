#----------------------------------------------------------------------------------------------------------------
# NasExplore
# Currently this program only gets the "photo of the day", but in this will be a full CLI thing in the future.
# See README.md for more details on the project and its goals.
#-----------------------------------------------------------------------------------------------------------------
# I think this looks cool (dont you?)
# _
# |
# |
#\|/
Startup = r"""
__/\\\\\_____/\\\______________________________/\\\\\\\\\\\\\\\______________________________/\\\\\\_______________________________________________        
 _\/\\\\\\___\/\\\_____________________________\/\\\///////////______________________________\////\\\_______________________________________________       
  _\/\\\/\\\__\/\\\_____________________________\/\\\_____________________________/\\\\\\\\\_____\/\\\_______________________________________________      
   _\/\\\//\\\_\/\\\__/\\\\\\\\\_____/\\\\\\\\\\_\/\\\\\\\\\\\______/\\\____/\\\__/\\\/////\\\____\/\\\________/\\\\\_____/\\/\\\\\\\______/\\\\\\\\__     
    _\/\\\\//\\\\/\\\_\////////\\\___\/\\\//////__\/\\\///////______\///\\\/\\\/__\/\\\\\\\\\\_____\/\\\______/\\\///\\\__\/\\\/////\\\___/\\\/////\\\_    
     _\/\\\_\//\\\/\\\___/\\\\\\\\\\__\/\\\\\\\\\\_\/\\\_______________\///\\\/____\/\\\//////______\/\\\_____/\\\__\//\\\_\/\\\___\///___/\\\\\\\\\\\__   
      _\/\\\__\//\\\\\\__/\\\/////\\\__\////////\\\_\/\\\________________/\\\/\\\___\/\\\____________\/\\\____\//\\\__/\\\__\/\\\_________\//\\///////___  
       _\/\\\___\//\\\\\_\//\\\\\\\\/\\__/\\\\\\\\\\_\/\\\\\\\\\\\\\\\__/\\\/\///\\\_\/\\\__________/\\\\\\\\\__\///\\\\\/___\/\\\__________\//\\\\\\\\\\_ 
        _\///_____\/////___\////////\//__\//////////__\///////////////__\///____\///__\///__________\/////////_____\/////_____\///____________\//////////__
"""
# Library Imports
import os
import sys
import time
import requests
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn

# Initialize the rich console
console = Console()

if sys.platform == "win32":
    os.system("chcp 65001 > nul")  # Forces UTF-8 encoding
    os.system("cls")               # Clears and resets terminal sizing

def fetch_nasa_data():
    # Public demo key for NASA API's
    url = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    load_bar = BarColumn(bar_width=40, style="black", complete_style="bright_green", finished_style="green3")
    with Progress(
        TextColumn("[bright_green]{task.description}"),
        load_bar,
        TextColumn("[green3]{task.percentage:>6.2f}%"),
        transient=True
    ) as progress:
        # Get connection
        api_task = progress.add_task("Connecting to NASA API's...", total=100)
        time.sleep(0.6)
        progress.update(api_task, advance=30)
        
        # Make API request and handle potential connection issues
        progress.update(api_task, description="Downloading data...")
        try:
            response = requests.get(url, timeout=60) # Quite long to handle the public demo being slow (like my brain in the morning)
            progress.update(api_task, advance=40)
            time.sleep(0.4)
            if response.status_code == 503: # Checks for MOST errors I have found in this section
                return {"error": "Nasa API Service Unavailable!"}
            if response.status_code == 429:
                return {"error": "NASA API Rate Limit Exceeded!"}
            if response.status_code == 200:
                progress.update(api_task, description="Processing data...", advance=30)
                time.sleep(0.3)
                return response.json()
            else:
                return {"error": f"NASA API Returned Code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"error": f"Connection failed: {str(e)}"}

def main():
    # Clear terminal screen and print a cool styled banner header
    console.clear()
    console.print(
    Panel.fit(
        "[bold dark_green]" + Startup + "[/bold dark_green]",
        border_style="green",
        subtitle="[green3]Version 1.0[/green3][green]-------[/green][green3]Type 'Help' for commands[/green3]",
        subtitle_align="left"
    ),
    soft_wrap=True,
    no_wrap=True
    )

    console.print("\n")

    # Trigger the loading bar and get data
    data = fetch_nasa_data()

    # Error Handling
    if "error" in data:
        console.print(Panel(f"[bold red]ERROR:[/bold red] [green3]{data['error']}[/green3]", border_style="red"))
        input("\nPress Enter to exit...")
        return

    # Extract Data
    title = data.get("title", "Unknown Cosmic Phenomenon")
    date = data.get("date", "Unknown Date")
    explanation = data.get("explanation", "No details provided.")
    hd_url = data.get("hdurl", "N/A")

    # Deal the goods (that sounds sus)
    console.print(f"[bold italic bright_green]PHOTO OF THE DAY[/bold italic bright_green]\n")
    console.print(f"[bold green3]Today we have: {title}[/bold green3]")
    console.print(f"[dim italic white]Captured on: {date}[/dim italic white]\n")
    
    
    console.print(Panel(explanation, title="[green3]Scientific Explanation[/green3]", border_style="green"))
    console.print("\n")
    
    # Clickable link to the image
    console.print(f" [bold underline green3]View High-Res Image:[/bold underline green3] {hd_url}")
    console.print("\n")
    input("\nPress Enter to exit...")
if __name__ == "__main__":
    main()
