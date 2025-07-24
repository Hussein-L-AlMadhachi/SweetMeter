import json

from utils.PrintLog import error, panic
import utils.Settings as Settings





is_language_set = False
messages = {}

english_messages = {} # default to this when localization word not found



# load the default localization file (will be used as a default when translations are not available yet)
try:
    with open( "localization/english.json" , "r" ) as f:
        english_messages = json.loads( f.read() )
except FileNotFoundError:
    panic( "No default English localization file" )





## NOTE:  I don't expect this to change in runtime
def set_language( language_used ):
    global messages , english_messages , is_language_set

    is_language_set = True

    if language_used == "english":
        messages = english_messages
        return

    try:
        with open( f"localization/{language_used}.json" , "r" ) as f:
            messages = json.loads( f.read() )
    except FileNotFoundError:
        error( "localization file not found or language is not supported" )



set_language( Settings.configs["language"] )





def message( message ):
    if not is_language_set: 
        raise Exception( "you have to use set_language( lang ) before using get_message( msg )" )

    msg = messages.get( message )

    if msg != None:
        return str( msg )
    
    msg = english_messages.get( message )

    if msg == None:
        raise Exception( "English Localization Fallback Failure: Message " + str( msg ) + " undeclared in english.json" )

    return str( english_messages.get( message ) )

