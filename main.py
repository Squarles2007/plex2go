from plexapi.myplex import MyPlexAccount

account = MyPlexAccount('Squarles2007','Fdq7765319$')
plex = account.resource('plex').connect()

print(plex)
playlist = plex.playlist('Kids Movies')
videos =  playlist.items()

total_size = 0

for v in videos:
    print(v.title, str(v.media[0].parts[0].size))
    total_size = total_size + v.media[0].parts[0].size
print(str(total_size))
