# Chunk IDs ranges for each part type.  Only covering women's parts for now.

# Author: peek6



# TODO:  So far, I have only used this for the women, Alisa, and women's outfits for Leo.
#  Making mods for men (including men's outfits for Leo) may need some more adjustments to the script.
#  At a minimum, the men's outfits need to be added to the tekken8_parts_and_chars dictionaries, and new ranges of chunk IDs need to be specified for the men's outfit parts



# Use 600's for all the clothing items

# 605 -> 654 for shirts (currently there are 44)
# 655 -> 670 for skirts (currently there are 11)
# 671 -> 682 for pants (currently there are 9)
# 683 -> 690 for coats (currently there are 7)

chunk_id_bases = {}
chunk_id_bases['coats'] = 683
chunk_id_bases['shirts'] = 605
chunk_id_bases['skirts'] = 655
chunk_id_bases['pants'] = 671

# Use 700's for shoes and stockings (either replacing the leg/feet MIs or not)

# Use 800's for hair and skin colors
chunk_id_bases['face'] = {}
chunk_id_bases['face']['alisa'] = 846
chunk_id_bases['face']['leo'] = 848
chunk_id_bases['face']['women'] = 850
chunk_id_bases['face']['men'] = 870
