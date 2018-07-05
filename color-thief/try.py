from colorthief  import ColorThief

color_thief = ColorThief('/Users/yasu/Downloads/30309571_p0.png')
# get the dominant color
dominant_color = color_thief.get_color(quality=1)
# build a color palette
palette = color_thief.get_palette(color_count=6)
print(dominant_color)
print(palette)
