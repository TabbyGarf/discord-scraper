from colorama import Fore
import json
import os
import discord
from datetime import datetime

from discord.ext import (
    commands,
    tasks
)

with open("config.json") as f:
    config = json.load(f)
    
token = config["token"]
cmd = config["command"]
command_prefix=config["prefix"]



client = discord.Client()
client = commands.Bot(
    command_prefix=config["prefix"],
    self_bot=True
)
client.remove_command('help')


os.system('cls')

print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Discord Chat Scraper made by {Fore.WHITE}LnX{Fore.LIGHTBLACK_EX}, fork by {Fore.YELLOW}TabbyGarf{Fore.LIGHTBLACK_EX}")
print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Licensed under {Fore.WHITE}MIT {Fore.LIGHTBLACK_EX}License")
print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}You can follow LnX on Github: {Fore.WHITE}https://github.com/lnxcz")
print(f"{Fore.WHITE}[ {Fore.CYAN}§ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}You can follow me there too:  {Fore.WHITE}https://github.com/TabbyGarf")

print(f"\n{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Bot is ready!")
print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Write {Fore.WHITE}{command_prefix}{cmd} <number of messages>{Fore.LIGHTBLACK_EX} to log messages\n")
os.system("title awaiting command")

def Init():
    if config["token"] == "token-here":
        os.system('cls')
        print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}You didnt put your token in the config.json file\n\n"+Fore.RESET)
        exit()
    else:
        token = config["token"]
        try:
            client.run(token, bot=False, reconnect=True)
            os.system(f'Discord message scraper')
        except discord.errors.LoginFailure:
            print(f"\n\n{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Token is invalid\n\n"+Fore.RESET)
            exit()


@client.command(name=cmd)
async def scrape(ctx, amount: int):
    time = datetime.now()
    ft = time.strftime("%Y%m%d-%H%M%S")
    f = open(f"scraped/{ctx.message.channel}-{ft}.txt","w+", encoding="UTF-8")
    count = 1
    total = amount
    print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Scraping {Fore.WHITE}{amount}{Fore.LIGHTBLACK_EX} messages to {Fore.WHITE}scraped/{ctx.message.channel}-{ft}.txt{Fore.LIGHTBLACK_EX}!")
    async for message in ctx.message.channel.history(limit=amount):
        attachments = [attachment.url for attachment in message.attachments if message.attachments]
        try:
            if attachments:
                realatt = attachments[0]
                f.write(f"({message.created_at}) {message.author}: {message.content} ({realatt})\n")
                print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Scraped {count} out of {total} message(s)")
            else:
                f.write(f"({message.created_at}) {message.author}: {message.content}\n")
                print(f"{Fore.WHITE}[ {Fore.GREEN}+ {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Scraped {count} out of {total} message(s)")
        except Exception as e:
            print(f"{Fore.WHITE}[ {Fore.RED}- {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Cannot scrape message from {Fore.WHITE}{message.author}")
            print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX} {Fore.WHITE}{e}")
            total = total - 1
        os.system("title [{}/{}] scraping {}".format(count,total,ctx.message.channel))
        count = count + 1
    print(f"{Fore.WHITE}[ {Fore.YELLOW}? {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Succesfully scraped {Fore.WHITE}{total} {Fore.LIGHTBLACK_EX}messages!\n\n{Fore.WHITE}")
    os.system("title [DONE] - awaiting command".format(total))



@client.event
async def on_command_error(ctx, error):
    error_str = str(error)
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, discord.errors.Forbidden):
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}Discord error: {error}"+Fore.RESET)    
    else:
        print(f"{Fore.WHITE}[ {Fore.RED}E {Fore.WHITE}] {Fore.LIGHTBLACK_EX}{error_str}"+Fore.RESET)

Init()
