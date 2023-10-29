with open('data/aoc-2019-08.txt') as f:
    dat = [x.strip() for x in f.readlines()]

width = 25
height = 6
layer_size = width * height
layer_count = len(dat[0]) // layer_size

layers = [dat[0][layer_size*i:layer_size*(i + 1)] for i in range(layer_count)]

zero_cnt = [sum([c == '0' for c in l]) for l in layers]
ones_cnt = [sum([c == '1' for c in l]) for l in layers]
twos_cnt = [sum([c == '2' for c in l]) for l in layers]

tgt_layer = zero_cnt.index(min(zero_cnt))
print('Part 1:', ones_cnt[tgt_layer] * twos_cnt[tgt_layer])

pixel_layers = [[l[i] != '2' for l in layers].index(True) for i in range(layer_size)]
output_pixels = [layers[pixel_layers[i]][i] for i in range(layer_size)]

print('Part 2:')
for y in range(height):
    print(''.join(output_pixels[25 * y:25 * (y + 1)]).translate(str.maketrans('10','# ')))
