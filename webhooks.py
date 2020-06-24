import requests
import discord
from discord import Webhook, RequestsWebhookAdapter, File
from instances import *

#https://discordapp.com/api/webhooks/725452347668561951/S03rnc5iONBka04j_qMvSVNE82n5JeJEF66Strrw6X7S1IdjGQJCd90lY5VGRW1jK413
class LoreWebhook():
    def __init__(self):
        webhook1 = Webhook.partial(725452347668561951, "S03rnc5iONBka04j_qMvSVNE82n5JeJEF66Strrw6X7S1IdjGQJCd90lY5VGRW1jK413",adapter=RequestsWebhookAdapter())

    def hello()
        webhook1.send("Hello")

    def send_embed():
        e = discord.Embed(title="Title")
