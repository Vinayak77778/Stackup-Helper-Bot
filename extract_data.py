from llama_index.readers.zendesk import ZendeskReader

# subdomain stackuphelpcenter
zendesk_subdomain = "stackuphelpcentre"  
locale = "en-us"  

# initialize zendesk reader
loader = ZendeskReader(zendesk_subdomain=zendesk_subdomain, locale=locale)

# load the data from the Zendesk help center
documents = loader.load_data()

# output data file
output_file = 'faq_data.txt'

# save the extracted text data to the specified file
with open(output_file, 'w', encoding='utf-8') as f:
    for doc in documents:
        f.write(doc.text + "\n\n")  

print(f"Text data saved to {output_file}")