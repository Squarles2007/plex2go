from plexapi.myplex import MyPlexAccount
from datetime import datetime
account = MyPlexAccount('Squarles2007','Fdq7765319$')
plex = account.resource('plex').connect()

max_bytes = 375000000000
class movie:
    cRating_max = 0
    cRating_min = 10
    aRating_max = 0
    aRating_min = 10
    yr_min = datetime.today().year
    yr_max = datetime.today().year
    count = 0
    aWt = 0.2
    cWt = 0.8
    yWt = 0.0

    def __init__(self, video, year, aRating, cRating, size):
        self.video = video
        self.year = year
        self.aRating = aRating
        self.cRating = cRating
        self.size = size

        movie.count += 1
        if cRating is not None and cRating > movie.cRating_max:
            movie.cRating_max = cRating
        if cRating is not None and cRating < movie.cRating_min:
            movie.cRating_min = cRating

        if aRating is not None and aRating > movie.aRating_max:
            movie.aRating_max = aRating
        if aRating is not None and aRating < movie.aRating_min:
            movie.aRating_min = aRating

        if year < movie.yr_min:
            movie.yr_min = year

    def getARatingScore(self):
        if self.aRating is not None:
            return (self.aRating - movie.aRating_min) / (movie.aRating_max - movie.aRating_min)
        else:
            return 0.5


    def getCRatingScore(self):
        if self.cRating is not None:
            return (self.cRating - movie.cRating_min) / (movie.cRating_max - movie.cRating_min)
        else:
            return 0.5


    def getYrScore(self):
        return (self.year - movie.yr_min) / (movie.yr_max - movie.yr_min)


    def combinedScore(self):
        return self.getARatingScore() * movie.aWt + self.getCRatingScore() * movie.cWt + self.getYrScore() * movie.yWt
        #return (self.getARatingScore() + self.getCRatingScore() + self.getYrScore()) / 3
    def __lt__(self, other):
        return self.combinedScore() < other.combinedScore()

def main():
    print(plex)
    playlist = plex.playlist('Kids Movies')
    videos =  playlist.items()
    mov_list = []
    total_size = 0

    for v in videos:
        mov_list.append(movie(v, v.year, v.audienceRating, v.rating, v.media[0].parts[0].size))

    mov_list.sort(reverse=True)
    n = 0
    for m in mov_list:
        if total_size + m.size <= max_bytes:
            print(m.video.title, m.combinedScore(), m.getYrScore(), m.year)
            total_size += m.size
            n += 1
        else:
            break
    print(n, str(total_size))


if __name__=="__main__":
    main()

