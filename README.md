# Prime - Tarkov bot
This is a personal project, ~~probably~~ writen in bad python as I learn the language.
This bot is written is Discord.py (rewrite)

## Resources
[Discord.py](https://discordpy.readthedocs.io/en/latest/api.html#)

## Required

You will need Python 3 - `brew install python3`

## Setup
1. After cloning the project, go to your project’s working directory:
```
$ cd prime
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
4. Set up credential file
```
data.json
```
5. Use makefile to run bot.
```
make build
```


## data.json example

```
{
  "owner" : ###,
  "description" : "DESC",
  "key" : "###",
  "assignable_roles" : ["Role1", "Role2"]
}
```
