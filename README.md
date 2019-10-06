# Prime - Tarkov bot
This is a personal project, ~~probably~~ writen in bad python as I learn the language.
This bot is written is Discord.py (rewrite)

## Resources
(Discord.py - Rewrite)[https://discordpy.readthedocs.io/en/rewrite/api.html]

## Required

You will need Python 3 - `brew install python3`

1. Go to your project’s working directory:
```
$ cd your-bot-source
$ python3 -m venv bot-env
```

2. Activate the virtual environment:
```
$ source bot-env/bin/activate
```
On Windows you activate it with:
```
$ bot-env\Scripts\activate.bat
```
3. Use pip like usual:
```
$ pip install -r requirements.txt
```

## Setup

```
{
  "owner" : ###,
  "description" : "DESC",
  "key" : "###",
  "assignable_roles" : ["Role1", "Role2"]
}
```
