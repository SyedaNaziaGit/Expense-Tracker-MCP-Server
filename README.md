# Expense-Tracker-MCP-Server

Setting MCP server
MCP
https://github.com/abhiemj/manim-mcp-server

cmd:

pip install manim
pip install mcp

cd desktop
git clone https://github.com/abhiemj/manim-mcp-server.git
cd manim-mcp-server


to configure the manim mcp server
go to claude-  settings - developer ->edit config > locate ->claude_sedktop_config.json -> paste this below code

inside config file give the path of python file"
cmd: which python3 
you get path add in configs: command key
and also:
cmd: which manim
gives path for exe file
cmd :
go to clone file
cd desktop
cd manim-mcp-server
cd src
pwd
give the path frm tht file

and then restart the claude desktop after any changes or adding any mcp server by closing it
Integration with Claude
To integrate the Manim MCP server with Claude, add the following to your claude_desktop_config.json file:

{
  "mcpServers": {
     "manim-server": {
      "command": "/absolute/path/to/python",
      "args": [
        "/absolute/path/to/manim-mcp-server/src/manim_server.py"
      ],
      "env": {
        "MANIM_EXECUTABLE": "/Users/[Your_username]/anaconda3/envs/manim2/Scripts/manim.exe"
      }
    }
  }
}






-------------------
check in claude - 
prompt:

"Use the manim-server to create an animation showing the concept of vector transformation in linear algebra.

* Start with a 2D coordinate grid.
* Show two basis vectors: $\hat{i} = (1,0)$ in red and $\hat{j} = (0,1)$ in blue.
* Animate a transformation by applying a matrix $A = [[2,1],[1,1]]$ to the grid and the vectors.
* Show the grid warping and the basis vectors moving to their new transformed positions.
* Add a title above: 'Linear Algebra: Matrix Transformation Demo'."
---------------------------
connecting twitter mcp server: local
https://github.com/EnesCinr/twitter-mcp
paste the code in claude deverloper config file - add the code inside mcpServer dict
developer console
{
  "mcpServers": {
    "twitter-mcp": {
      "command": "npx",
      "args": ["-y", "@enescinar/twitter-mcp"],
      "env": {
        "API_KEY": "your_api_key_here",
        "API_SECRET_KEY": "your_api_secret_key_here",
        "ACCESS_TOKEN": "your_access_token_here",
        "ACCESS_TOKEN_SECRET": "your_access_token_secret_here"
      }
    }
  }
}
connecting remote mcp server
connecting weather mcp server
https://github.com/adhikasp/mcp-weather

to get api keys frm accuweather:
https://developer.accuweather.com/home
get apikey frm here

{
    "mcpServers": {
        "weather": {
            "command": "uvx",
            "args": ["--from", "git+https://github.com/adhikasp/mcp-weather.git", "mcp-weather"],
            "env": {
                "ACCUWEATHER_API_KEY": "your_api_key_here"
            }
        }
    }
}

=================
 to check for available mcp servers : google search :  awesome mcp servers: check this below GitHub link:
https://github.com/punkpeye/awesome-mcp-servers


-----------------------
Working with fastmcp:

pip install uv

create a dir - expense-tracker-mcp-server 
open in vs code

terminal: - initializing uv terminal in current directory

uv init .

uv add fastmcp
fastmcp version
---note: close the vs code and restart after every install if its not working---
op:

FastMCP version:                                                                                     3.4.4
MCP version:                                                                                        1.28.1
Python version:                                                                                     3.12.6
Platform:                                                                        Windows-11-10.0.26200-SP0
FastMCP root path: C:\Users\Lenovo\OneDrive\Desktop\MCP\expense-tracker-mcp-server\.venv\Lib\site-packages

writing fastmcp code

to test server if its running to debug: we get a mcp inspector tool on search engine: it is by anthropic:

uv run fastmcp dev main.py

to run server:
uv run fastmcp run main.py

connecting mcp to claude desktop:
uv run fastmcp install claude-desktop main.py 

configure the json file on claude desktop setting:
change the paths accordingly

<img width="857" height="277" alt="image" src="https://github.com/user-attachments/assets/312e336a-6e80-480a-9f86-2d9da102ff86" />





<img width="857" height="277" alt="image" src="https://github.com/user-attachments/assets/70ceb26d-d0c1-4beb-acf3-29e7f881e6b3" />
