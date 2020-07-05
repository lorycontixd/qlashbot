import discord
import itertools
from io import StringIO

role_ids = {'@everyone': 415221296247341066, 'Muted': 700794700378144878}

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

everyone_perms_dict = {'create_instant_invite' : ALLOWED, 'kick_members' : DENIED, 'ban_members' : DENIED,
'administrator' : DENIED, 'manage_channels' :  DENIED, 'manage_guild' : DENIED,'add_reactions' : ALLOWED,
'view_audit_log' : DENIED,'priority_speaker' : DENIED,'read_messages' : ALLOWED,'send_messages' : ALLOWED,
'send_tts_messages' : DENIED, 'manage_messages' : ALLOWED, 'embed_links' : ALLOWED,
'attach_files' : ALLOWED,'read_message_history' : ALLOWED, 'mention_everyone': DENIED,
'external_emojis' : ALLOWED, 'connect' : ALLOWED, 'speak' : ALLOWED, 'mute_members' : DENIED, 'deafen_members' : DENIED,
'move_members' : DENIED,'use_voice_activation' : DENIED,'change_nickname' : ALLOWED,
'manage_nicknames' : DENIED,'manage_roles' : DENIED,'manage_webhooks' : DENIED,
'manage_emojis' : DENIED}

muted_perms_dict = {'create_instant_invite' : DEFAULT, 'kick_members' : DEFAULT, 'ban_members' : DEFAULT,
'administrator' : DEFAULT, 'manage_channels' :  DEFAULT, 'manage_guild' : DEFAULT,'add_reactions' : DEFAULT,
'view_audit_log' : DEFAULT,'priority_speaker' : DEFAULT,'read_messages' : DEFAULT,'send_messages' : DENIED,
'send_tts_messages' : DEFAULT, 'manage_messages' : DEFAULT, 'embed_links' : DEFAULT,
'attach_files' : DEFAULT,'read_message_history' : DEFAULT, 'mention_everyone': DEFAULT,
'external_emojis' : DEFAULT, 'connect' : DEFAULT, 'speak' : DEFAULT, 'mute_members' : DEFAULT, 'deafen_members' : DEFAULT,
'move_members' : DEFAULT,'use_voice_activation' : DEFAULT,'change_nickname' : DEFAULT,
'manage_nicknames' : DEFAULT,'manage_roles' : DEFAULT,'manage_webhooks' : DEFAULT,
'manage_emojis' : DEFAULT}


def _factory_build_permissions(ow_allow_perms, ow_deny_perms):
    default_perms_dict = dict.fromkeys(permissions, DEFAULT)

    for k in ow_allow_perms:
        if k[1]:
            default_perms_dict[k[0]] = ALLOWED
    for k in ow_deny_perms:
        if k[1]:
            default_perms_dict[k[0]] = DENIED

    return default_perms_dict


def _factory_build_actor_name(actor):
    actor_name = ""
    if type(actor) is discord.Member:
        actor_name = "" + actor.name
    elif type(actor) is discord.Role:
        if actor.name.startswith("@"):
            actor_name = actor.name[1:]
        else:
            actor_name = actor.name
    return actor_name

def _factory_build_output(actor, perms_dict):
    with StringIO() as output:
        actor_name = _factory_build_actor_name(actor)
        output.write(actor_name)
        output.write("\n")
        output.write("```css\n")
        for k in perms_dict:
            output.write(k + " : " + perms_dict[k] + "\n")
        output.write("```")
        output.write("\n")
        return output.getvalue()

def _check_expected_actual_overwrites(output,expected,actual):
    for k in {x : x for x in expected if x in actual and expected[x] != actual[x]}:
        output.write(k + "\t" + actual[k] + "\tExpected: " + expected[k] + "\n")

def _factory_build_missing_roles(channel):
    with StringIO() as output:
        output.write("Checking for missing roles\n")
        missing_roles = role_ids.copy()
        for actor in channel.overwrites:
            if type(actor) is discord.Role:
                if actor.name in role_ids:
                    del missing_roles[actor.name]

        for k in missing_roles:
            output.write(k + " has no defined permissions.\n")

        return output.getvalue()

def _factory_build_anomalies(actor, perms_dict):
    with StringIO() as output:
        actor_name = _factory_build_actor_name(actor)
        if type(actor) is discord.Member:
            output.write("Custom setting set for member " + actor_name + "\n")
        elif type(actor) is discord.Role:
            output.write("Checking role permissions for " + actor_name + "\n")
            if(actor.id == role_ids['@everyone']):
                _check_expected_actual_overwrites(output, everyone_perms_dict,perms_dict)
            elif(actor.id == role_ids['Muted']):
                _check_expected_actual_overwrites(output, muted_perms_dict,perms_dict)
            else:
                output.write("No schema defined for role: " + actor_name)

        return output.getvalue()

async def util_check_channel (cog, ctx, channel):
    missing_roles_string = _factory_build_missing_roles(channel)
    await ctx.send(missing_roles_string)
    for actor in channel.overwrites:
        ow_allow, ow_deny = channel.overwrites[actor].pair()
        ow_allow_perms =  discord.Permissions(ow_allow.value)
        ow_deny_perms =  discord.Permissions(ow_deny.value)
        perms_dict = _factory_build_permissions(ow_allow_perms,ow_deny_perms)
        #output_string = _factory_build_output(actor,perms_dict)
        #await ctx.send(output_string)
        error_string = _factory_build_anomalies(actor,perms_dict)
        await ctx.send(error_string)
