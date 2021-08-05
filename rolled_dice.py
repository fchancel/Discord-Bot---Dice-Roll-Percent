import discord
from dotenv import load_dotenv
import random
import os


load_dotenv(dotenv_path="config")
client = discord.Client()


def parse_rolled_percent_dice(cmd):
    cmd = cmd.split()[1:]
    try:
        int(cmd[0][1:])
    except ValueError:
        raise Exception("Idiot ! Ta commande est invalide !")
    if cmd[1] != "d" or "p" not in cmd:
        raise Exception("Idiot ! Ta commande est invalide !")
    i = 2
    number_list = []
    dice_value = int(cmd[0][1:])
    while cmd[i] != "p":
        try:
            int(cmd[i])
        except ValueError:
            raise Exception(
                "Idiot ! Ta liste de dé ne doit comporter que des nombres !")
        if int(cmd[i]) > dice_value:
            raise Exception(
                "Idiot ! Ta liste de dé ne peux pas posséder un nombre plus grand que la valeur de ton dé !")
        elif int(cmd[i]) <= 0:
            raise Exception(
                "Idiot ! Ta liste de dé ne peux pas posséder un nombre inférieur à 1 !"
            )

        number_list.append(int(cmd[i]))
        i += 1
    percent_list = cmd[i + 1:]
    total_percent = 0
    for value in percent_list:
        try:
            int(value)
        except ValueError:
            raise Exception(
                "Idiot ! Ta liste de pourcentage ne doit comporter que des nombres !")
        total_percent += int(value)
    if len(number_list) == 0:
        raise Exception("Idiot ! Ta commande est invalide !")
    elif len(number_list) != len(percent_list):
        raise Exception(
            "Idiot ! Tu dois avoir autant de valeur de dé que de valeur pourcentage")
    elif len(set(number_list)) != len(number_list):
        raise Exception(
            "Idiot ! Ta liste de dé ne doit pas comporter de doublon")
    elif total_percent > 100:
        raise Exception("Idiot ! Tu ne peux pas dépasser 100% !")


def rolled_percent_dice(cmd):
    cmd = cmd.split()[1:]
    dice_faces = int(cmd[0][1:])
    if dice_faces == 1:
        return 1
    else:
        numbers_lst = []
        percent_lst = []
        numbers_final_lst = []
        value_lst = []
        value_select = random.randint(0, 99)
        i = 2

        while cmd[i] != "p":
            numbers_lst.append(int(cmd[i]))
            i += 1
        percent_list = cmd[i + 1:]
        for i in range(len(numbers_lst)):
            j = 0
            while j != int(percent_list[i]):
                numbers_final_lst.append(numbers_lst[i])
                j += 1
        for value in range(1, dice_faces + 1):
            if value not in numbers_lst:
                value_lst.append(value)
        for i in range(len(numbers_final_lst), 100):
            numbers_final_lst.append(value_lst[i % len(value_lst)])
        random.shuffle(numbers_final_lst)
        return numbers_final_lst[value_select]


def make_response(cmd, message, result):
    cmd = cmd.split()[1:]
    dice_faces = int(cmd[0][1:])
    numbers_lst = []
    i = 2
    while cmd[i] != "p":
        numbers_lst.append(cmd[i])
        i += 1
    percent_lst = cmd[i + 1:]

    msg = f"Le résultat de 1d{dice_faces} est: **{result}\n** *Pourcentage demandé :*\n"
    for i in range(len(numbers_lst)):
        msg = f"{msg} *{str(numbers_lst[i])} - {percent_lst[i]}%* \n"

    embedVar = discord.Embed(
        title="Lanceur de dé", description=msg, color=3447003)
    embedVar.set_footer(icon_url=message.author.default_avatar_url,
                        text=f"{message.author.display_name}  vient de lancer 1 dé de {dice_faces} faces")
    return embedVar


def make_error_response(message, error):
    embedVar = discord.Embed(
        title="Lanceur de dé", description=error, color=0xbf1e1e)
    embedVar.set_footer(icon_url=message.author.default_avatar_url,
                        text=f"{message.author.display_name}  est idiot")
    return embedVar


@client.event
async def on_ready():
    print("Le bot est prêt !")


@client.event
async def on_message(message):
    if len(message.content) > 0:
        cmd_lst = message.content.split()
        if cmd_lst[0] == '!dice':
            if cmd_lst[1][0] == "p":
                try:
                    parse_rolled_percent_dice(message.content)
                    result = rolled_percent_dice(message.content)
                    message_delete = await message.channel.history(limit=1).flatten()
                    for msg in message_delete:
                        await msg.delete()

                    await message.channel.send(embed=make_response(message.content, message, result))
                except Exception as e:
                    await message.channel.send(embed=make_error_response(message, e))
            else:
                try:
                    nb_dice = int(cmd_lst[1][0])
                    if nb_dice > 0:
                        pass
                    else:
                        await message.channel.send(embed=make_error_response(message, "Idiot ! Choisis au minimum un dé !"))
                except ValueError:
                    await message.channel.send(embed=make_error_response(message, "Idiot ! Ta commande est invalide"))


client.run(os.getenv("TOKEN"))
