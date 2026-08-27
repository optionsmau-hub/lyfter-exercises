# Read the songs from the file
with open("songs.txt", "r") as file:
    songs = file.readlines()

# Remove extra spaces and line breaks
songs = [song.strip() for song in songs]

# Sort songs alphabetically
songs.sort()

# Write the sorted songs to a new file
with open("songs_sorted.txt", "w") as file:
    for song in songs:
        file.write(song + "\n")

print("Songs sorted successfully.")