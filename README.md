
# Steam Games Recommender

A brief description of what this project does and who it's for

This project was created becuase I never know what game to play. Its aim is to show the list of games which are installed in the Steam library and sort them based on certain statistics, which are outlined below in Features.


## Features

- (Not implemented) Sort your games library according to:
    - Potential playtime: This is calculated using `global_average_playtime - individual_playtime` and is aimed to show which games you can potentially play more of
    - Rating
    - Individual playtime
- Cross platform
- Theme follows system theme

## Run Locally

Note: For future stable releases, executable binaries (.exe files etc.) will be distributed so that users can download and use this with only a few clicks.

### Installation

Install dependencies with pip (requires Python 3)
```
  pip install customtkinter vdf
``` 

Clone the project

```bash
  git clone https://github.com/ample-samples/steam-games-recommender.git
```

Go to the project directory and run the main file

```bash
  cd steam-games-recommender
  python main.py
```

Find your libraryfolders.vdf inside of your file manager, this is usually located at `C:\Program Files (x86)\Steam\steamapps\libraryfolders.vdf` for Windows users unless you have chosen a different installation path for Steam.

Once you have found the file, right-click on it and press "copy" to copy its path to your clipboard. You should paste this path into the entry field in the top left of the program and press save. 

Lastly, restart the application and you will see the list of your games and you're ready to use SGR, happy gaming!
