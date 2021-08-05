import discord
from dotenv import load_dotenv
import random
import os


load_dotenv(dotenv_path="config")
client = discord.Client()


def parse_rolled_percent_dice(cmd):
    cmd = cmd.split()[1:]
    try:
        int(cmd[0][2:])
    except ValueError:
        raise Exception("Idiot ! Ta commande est invalide !")
    if cmd[1] != "d" or "p" not in cmd:
        raise Exception("Idiot ! Ta commande est invalide !")
    i = 2
    number_list = []
    dice_value = int(cmd[0][2:])
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
    elif len(number_list) == dice_value and total_percent != 100:
        raise Exception(
            "Idiot ! Le total doit atteindre 100% si tu souhaites selectionner des valeurs pour chaque face de ton dé ! ")


def rolled_percent_dice(cmd):
    cmd = cmd.split()[1:]
    dice_faces = int(cmd[0][2:])
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
        if len(numbers_lst) != dice_faces:
            for value in range(1, dice_faces + 1):
                if value not in numbers_lst:
                    value_lst.append(value)
            for i in range(len(numbers_final_lst), 100):
                numbers_final_lst.append(value_lst[i % len(value_lst)])
        random.shuffle(numbers_final_lst)
        return numbers_final_lst[value_select]


def parse_rolled_dice(cmd):
    cmd = cmd.split()[1:]
    if len(cmd) != 1 or 'd' not in cmd[0]:
        raise Exception("Idiot ! Ta commande est invalide !")
    cmd = cmd[0].split('d')
    try:
        nb_dice = int(cmd[0])
        dice_value = int(cmd[1])
    except ValueError:
        raise Exception("Idiot ! Ta commande est invalide !")


def rolled_dice(cmd):
    cmd = cmd.split('d')
    nb_dice = int(cmd[0])
    dice_value = int(cmd[1])
    result_lst = []
    for i in range(nb_dice):
        result_lst.append(random.randint(1, dice_value))
    return result_lst


def make_response(cmd, message, result, percent=False):
    cmd = cmd.split()[1:]
    if percent:
        dice_faces = int(cmd[0][2:])
        numbers_lst = []
        i = 2
        while cmd[i] != "p":
            numbers_lst.append(cmd[i])
            i += 1
        percent_lst = cmd[i + 1:]

        msg = f"Le résultat de 1d{dice_faces} est: **{result}\n** *Pourcentage demandé :*\n"
        for i in range(len(numbers_lst)):
            msg = f"{msg} *{str(numbers_lst[i])} - {percent_lst[i]}%* \n"
    else:
        msg = f"Le résultat de {cmd[0]} est "
        dice_faces = int(cmd[0].split("d")[1])
        if len(result) > 1:
            msg += " [ "
        for i in range(len(result)):
            msg += str(result[i])
            if i < len(result) - 1:
                msg += " + "
        if len(result) > 1:
            msg += f" ] = {sum(result)}"

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
            if cmd_lst[1][0:2] == "dp":
                try:
                    parse_rolled_percent_dice(message.content)
                    result = rolled_percent_dice(message.content)
                    message_delete = await message.channel.history(limit=1).flatten()
                    for msg in message_delete:
                        await msg.delete()

                    await message.channel.send(embed=make_response(message.content, message, result, True))
                except Exception as e:
                    await message.channel.send(embed=make_error_response(message, e))
            else:
                try:
                    parse_rolled_dice(message.content)
                    result = rolled_dice(cmd_lst[1])
                    message_delete = await message.channel.history(limit=1).flatten()
                    for msg in message_delete:
                        await msg.delete()
                    
                    await message.channel.send(embed=make_response(message.content, message, result, False))

                except ValueError:
                    await message.channel.send(embed=make_error_response(message, "Idiot ! Ta commande est invalide"))


client.run(os.getenv("TOKEN"))
