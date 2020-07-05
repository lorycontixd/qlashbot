import discord
import itertools
from io import StringIO

role_everyone = 415221296247341066

ALLOWED = "✔️ ALLOWED"
DENIED = "❌ DENIED"
DEFAULT = "〰️ DEFAULT"

permissions = ['create_instant_invite', 'kick_members', 'ban_members',
'administrator', 'manage_channels','manage_guild','add_reactions',
'view_audit_log','priority_speaker','read_messages','send_messages',
'send_tts_messages','manage_messages','embed_links','attach_files','read_message_history','mention_everyone',
'external_emojis','connect','speak','mute_members','deafen_members',
'move_members','use_voice_activation','change_nickname','manage_nicknames','manage_roles','manage_webhooks',
'manage_emojis'
]
def _util_check_channel_overwrites(actor, ow_allow_perms, ow_deny_perms):
    default_perms_dict = dict.fromkeys(permissions, DEFAULT)

    for k in ow_allow_perms:
        if k[1]:
            default_perms_dict[k[0]] = ALLOWED
    for k in ow_deny_perms:
        if k[1]:
            default_perms_dict[k[0]] = DENIED

    return default_perms_dict

async def util_check_channel (cog, ctx, channel):
    output = StringIO()
    for actor in channel.overwrites:
        ow_allow, ow_deny = channel.overwrites[actor].pair()
        ow_allow_perms =  discord.Permissions(ow_allow.value)
        ow_deny_perms =  discord.Permissions(ow_deny.value)
        perms_dict = _util_check_channel_overwrites(actor, ow_allow_perms,ow_deny_perms)
        actor_name = ""
        if type(actor) is discord.Member:
            actor_name = "Member " + actor.name
        elif type(actor) is discord.Role:
            if actor.name.startswith("@"):
                actor_name = actor.name[1:]
            else:
                actor_name = actor.name

        output.write(actor_name)
        output.write("\n")
        output.write("```css\n")
        for k in perms_dict:
            output.write(k + " : " + perms_dict[k] + "\n")
        output.write("```")
        output.write("\n")
        await ctx.send(output.getvalue())
        output.truncate(0)
        output.seek(0)
    output.close()
