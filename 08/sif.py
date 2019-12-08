from collections import Counter

with open('input') as f:
    sif = f.read().strip()
input_size = len(sif)
width = 25
height = 6
image_size = width * height
layer_count = input_size // image_size
layers = [sif[i:i + image_size] for i in range(0, input_size, image_size)]
layer_counts = []
for layer in layers:
    layer_counts.append(Counter(list(layer)))
check_layer = min(layer_counts, key=lambda x: x['0'])
# check_layer = max(layers,key=lambda x : sum(1 for c in x if c == '0'))
zeros = check_layer['0']
ones = check_layer['1']
twos = check_layer['2']
assert zeros + ones + twos == image_size
print('Part 1')
print(ones * twos)
print('Part 2')
final_image = ''
for p in range(image_size):
    n = ''.join([c[p] for c in layers]).lstrip('2')
    final_image += '#' if n[0] == '1' else ' '
for w in range(0, image_size, width):
    print(final_image[w:w + width])
