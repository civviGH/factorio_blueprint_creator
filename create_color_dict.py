import pickle
import math

colors = {}
colors["stone-path"] = (99,101,99)
colors["concrete"] = (49,48,49)
colors["concrete-black"] = (8,12,8)
colors["concrete-magenta"] = (57,12,123)
colors["concrete-purple"] = (57,12,123)
colors["concrete-blue"] = (8,12,123)
colors["concrete-cyan"] = (8,125,123)
colors["concrete-green"] = (8,125,8)
colors["concrete-yellow"] = (123,125,8)
colors["concrete-orange"] = (123,60,8)
colors["concrete-red"] = (123,12,8)

shortest_range = {}

def calculate_distance(t1, t2):
    distance = math.sqrt((t1[0]-t2[0])**2 + (t1[1]-t2[1])**2 + (t1[2]-t2[2])**2)
    return distance

print("Calculate nearest color for every (R,G,B)...")
for i in range(256):
    print("{}%".format((float(i+1)/256) * 100.0))
    for j in range(256):
        for k in range(256):
            working_tuple = (i,j,k)
            minimal_distance = 99999999
            nearest_color = ""
            for k, v in colors.iteritems():
                distance = calculate_distance(working_tuple, v)
                if distance < minimal_distance:
                    minimal_distance = distance
                    nearest_color = k
            shortest_range[working_tuple] = nearest_color
print("done.")
print("Saving dictionary to file...")
#save dict of shortest ranges to file
with open("color_coding_ranges.txt", "wb") as f:
    pickle.dump(shortest_range, f, protocol=pickle.HIGHEST_PROTOCOL)
print("done.")
