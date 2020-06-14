#UTILITY FUNCTIONS (mostly non-async)
import discord
import os
import pytz

from discord.ext import commands
from discord.ext.commands import Bot,cooldown
from discord.voice_client import VoiceClient
from datetime import datetime
from instances import *

##***** TAIL FUNCTION -> Grab the last N lines from a file. Returns a list of the last N lines.

def tail(file_name, N):
    # Create an empty list to keep the track of last N lines
    list_of_lines = []
    # Open file for reading in binary mode
    with open(file_name, 'rb') as read_obj:
        # Move the cursor to the end of the file
        read_obj.seek(0, os.SEEK_END)
        # Create a buffer to keep the last read line
        buffer = bytearray()
        # Get the current position of pointer i.e eof
        pointer_location = read_obj.tell()
        # Loop till pointer reaches the top of the file
        while pointer_location >= 0:
            # Move the file pointer to the location pointed by pointer_location
            read_obj.seek(pointer_location)
            # Shift pointer location by -1
            pointer_location = pointer_location -1
            # read that byte / character
            new_byte = read_obj.read(1)
            # If the read byte is new line character then it means one line is read
            if new_byte == b'\n':
                # Save the line in list of lines
                list_of_lines.append(buffer.decode()[::-1])
                # If the size of list reaches N, then return the reversed list
                if len(list_of_lines) == N:
                    return list(reversed(list_of_lines))
                # Reinitialize the byte array to save next line
                buffer = bytearray()
            else:
                # If last read character is not eol then add it in buffer
                buffer.extend(new_byte)

        # As file is read completely, if there is still data in buffer, then its first line.
        if len(buffer) > 0:
            list_of_lines.append(buffer.decode()[::-1])
    # return the reversed list
    return list(reversed(list_of_lines))

##********* Command Logs - Function to be called to register the invocation of a command in a file

def CommandLogs(ctx,commandname):
    author = ctx.message.author
    tz = pytz.timezone('Europe/Rome')
    time = datetime.now(tz=tz)
    logfile = open('command_logs.txt','a+')
    logfile.write(str(author)+" has called the command "+str(commandname)+" at time "+str(time)+'\n')
    logfile.close()

#******************************************************************************

def fileread(filename):
    file = open(filename,'r+')
    content = file.read()
    lines = content.split("\n")
    return lines
