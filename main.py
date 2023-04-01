from telethon import TelegramClient, events
import requests
import pyshorteners


# replace <YOUR_API_ID> and <YOUR_API_HASH> with your actual API ID and hash
api_id = 27989413
api_hash = 'bf7f2540d24231e3b8e4854683d6bb9a'

# replace <YOUR_PHONE_NUMBER> with your actual phone number
phone_number = '8005658035'

# Define the AWS credentials and region
aws_access_key_id = 'AKIAIETEZGQ4YORYMAKQ'
aws_secret_access_key = 'ITWwo3UPZaibYZesTBompiLPyIMH7KCFeLgeQk3r'
aws_region_name = 'us-east-1'

# Define the AWS Product Advertising API client
#paapi5 = boto3.client('paapi5', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)



# replace <YOUR_BOT_TOKEN> with your actual bot token
bot_token = '6295391205:AAFUPKaed4Joiott4P0UKUaZeve3IG6lcxM'

source_group_ids = [-1001388213936, -1001363680849]
destination_group_ids = -1001320986887

# replace <YOUR_AFFILIATE_TAG> with your actual affiliate tag
affiliate_tag = 'vinodkumar016-21'

# create a TelegramClient object with your API ID, hash, and phone number
client = TelegramClient('send_message_bot', api_id, api_hash)
client.connect()

# log in to your account with the phone number and code
if not client.is_user_authorized():
    client.send_code_request(phone_number)
    client.sign_in(phone_number, code)

# create a PyShorteners object for URL shortening
s = pyshorteners.Shortener()
#(chats=source_group_ids)
# define a function to handle incoming messages in the source group
@client.on(events.NewMessage)
async def handle_message(event):
    try:
        # check if the source chat ID matches the expected 
        #print(event.chat.title)
    
        # get the incoming message text
        message_text = event.message.message
        
        # check if the message contains a short URL
        if 'http' in message_text:
            # retrieve the short URL from the message
             short_url = message_text.split('https://')[1].split()[0]
             short_url = "https://"+short_url
            # decode the short URL
             decoded_url = requests.get(short_url).url
            # check if the URL is from amazon.in
             if 'amazon.in' in decoded_url:
             # Extract the existing affiliate tag from the URL
               start_index = decoded_url.find('tag=') + len('tag=')
               end_index = decoded_url.find('&', start_index)
             if  end_index == -1:
                 end_index = len(decoded_url)
                 existing_affiliate_tag = decoded_url[start_index:end_index]

               # Replace the existing affiliate tag with the new tag
             new_url = decoded_url.replace(existing_affiliate_tag, affiliate_tag)
             short_url = s.tinyurl.short(new_url)
             await client.send_message(destination_group_ids, short_url)
                # replace the existing tag with the user's tag
               # parsed_url = urlparse(decoded_url)
               # query = parse_qs(parsed_url.query)
                #query['tag'] = [affiliate_tag]
                #new_url = parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path + '?' + '&'.join([f'{k}={v[0]}' for k, v in query.items()])
      
       
    except Exception as e:
        print(f"Exception occurred: {e}")

# start the client
client.start()

# run the client until you stop it manually
client.run_until_disconnected()
