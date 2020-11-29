import Map
import Images

alignment_list = ['Hero','Minion','Fallen-wizard','Elf-lord','Dwarf-lord','Atani-lord']
# alignment_list = ['Hero']

for alignment in alignment_list:
    Images.combined_images(alignment)
    Map.map_html(alignment)


