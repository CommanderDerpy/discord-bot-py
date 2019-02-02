# Prime - Tarkov bot
This is a personal project, ~~probably~~ writen in bad python as I learn the language.
This bot is written is Discord.py (rewrite)

## Resources
(Discord.py - Rewrite)[https://discordpy.readthedocs.io/en/rewrite/api.html]

## Required

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
$ python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice] bs4
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
