import random

file = open('file.tsv', 'a')

for movie_id in range(2000, 2041):
    for user_id in range(1, 201):
        rating = random.randint(3, 5)
        timestamp = random.randint(1000000000, 2000000000)

        file.write(f"{user_id}\t{movie_id}\t{rating}\t{timestamp}\n")

file.close()

print("Ratings added!")