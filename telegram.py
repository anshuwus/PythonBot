
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from telethon.errors.rpcerrorlist import UserPrivacyRestrictedError
from telethon.tl.types import InputPeerChannel

# Replace the values with your own API ID, API hash, and session name
api_id = 27989413
api_hash = 'bf7f2540d24231e3b8e4854683d6bb9a'
session_name = 'your_session_name'

client = TelegramClient(session_name, api_id, api_hash)

# Replace the value with the username or ID of the group you want to get users from
group_username = 'ratingreviewamazon'
group_id = 1232881301
with client:
    # Get the full entity of the group
    group_entity = client.get_entity(InputPeerChannel(group_id, 0))
    print('Fetching Members...')
    all_participants = []
    all_participants = client.get_participants(group_username, aggressive=True)
    
    dialogs = client(GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=100,
    hash=0
    )).chats
    #destination_group_entity = 1349913249
    #title = 'BestLootDeals'
    title = 'Amazing Deals (Deals 24x7)'
    for dialog in dialogs:
     if dialog.title == title:
         destination_group_entity = dialog.id
         break

    # Iterate over the participants and print their usernames or phone numbers
    for participant in all_participants:
        try:
           client(InviteToChannelRequest(
           destination_group_entity,
           users=[participant.id]
           ))
        except UserPrivacyRestrictedError:
           print(f'The user {participant}\'s privacy settings do not allow you to do this. Skipping.')
        except Exception as e:
           print(f'Error occurred while adding {participant}: {e}')
           continue
