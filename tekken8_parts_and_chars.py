# Dictionaries with parts and characters to be used by the automated outfit selector

# Author: peek6

# TODO:  So far, I have only used this for the women, Alisa, and women's outfits for Leo.
#  Making mods for men (including men's outfits for Leo) may need some more adjustments to the script.
#  At a minimum, the men's outfits need to be added to the dictionaries below, and new ranges of chunk IDs need to be specified for the men's outfit parts


body_parts_dict = {}


# parts which can be worn with any bottom
body_parts_dict['shirts'] = [
'blazer',
'blazer_check',
'blazerline',
'blousefrill',
'blousefrill_panther',
'blousefrill_seethrough',
'blousefrillnos',
'blousefrilltie_flower',
'blousefrlnos_dot',
'blousefrlnos_flower',
'henry',
'henrylong',
'knitvest',
'knitvestlong',
'officedresscollar',
'officedresscollarfrill',
'officedressfrilllong',
'officedresswfrill',
'operasuit',
'ridershineck',
'shirtinlong_twotone',
'shirtinseven_scarf',
'shirtinseven_thickstripe',
'shirtinseventie_stripe',
'shirtinss_cami',
'shirtinss_dot',
'shirtinss_flower',
'shirtlong_check',
'shirtlong_design',
'shirtribbon',
'shirtseven',
'tanktopfighter',
'tshirt',
'tshirt_animal',
'tshirt_print',
'tshirt_stripe',
'tshirt_tiger',
'tshirtcamisole',
'tshirtlong',
'tshirtlong_pocket',
'tshirtraglan',
'vneckknit',
'tailcoat',
'tailcoat_embroid'
]

# parts which can only be worn with 'pants'
body_parts_dict['coats'] = [
'longcoat_bigcheck',
'longcoat_check',
'longcoatfur',
'longcoatfurB_crocodile',
'mlongcoat_herringbone',
'mlongcoat_houndstooth',
'pinkcoat'
]

# skirts which cannot be worn with coats
body_parts_dict['skirts'] = [
'bpleat',
'culottesshort',
'culottesshort_cotton',
'pleatshort',
'pleatshort_line',
'pleatshort_wlines',
'pleatshortsps',
'pleatshortsps_tartanA',
'pleatskirt',
'pleatskirt_plain',
'pleatskirt_tartanB'
]

# 'hotpants'

# 'pants' here means anything which can be worn with a coat, so it includes the culottes skirts
body_parts_dict['pants'] = [
'mdenim',
'mdenimdamage',
'slacks',
'slacks_check',
'slacks_embroid',
'widepants_denim',
'culottes',
'culottes_cotton',
'culottes_satin'
]

body_parts_dict['shoes'] = [
'barefoot',
'canvassneaker',
'furshortboots',
'heellongboots',
'highheal',
'loaferA',
'loaferB',
'officemule',
'running',
'sandals',
'shortboots',
'sneakers',
'straighttip',
'trackshoes',
'trailshoes'
]

body_parts_dict['shoes_with_hose'] = [
'heellongboots_stA',
'heellongboots_stB',
'loaferC_khA',
'loaferC_stA',
'officemuletoe_khA',
'officemuletoe_stA',
'officemuletoe_stB',
'sandals_khB',
'shortboots_stA',
'shortboots_stB'
]

chars_dict = {}

chars_dict['women'] = {
    'aml': 'jun',
    'cat': 'azucena',
    'crw': 'zafina',
    'der': 'asuka',
    'hms': 'lili',
    'kal': 'nina',
    'rat': 'xiaoyu',
    'zbr': 'reina'
}

# use chunks 870-892, 870 = all men
chars_dict['men'] = {
'ant':'Jin',
'bbn':'Raven',
'bsn':'Steve',
'cht':'Bryan',
'ctr':'Claudio',
'dog':'Eddy',
'grf':'Paul',
'grl':'Kazuya',
'hrs':'Shaheen',
'jly':'Leroy',
'klw':'Feng',
'kmd':'Dragunov',
'lon':'Victor',
'lzd':'Lars',
'pgn':'King',
'pig':'Law',
'snk':'Hwoarang',
'swl':'Devil_Jin',
'wlf':'Lee'
}

# Alisa works differently, although her lowers could theoretically be included with women if they are compatible with all existing upper body parts
chars_dict['alisa'] = {'mnt': 'alisa'}  # I may be able to include Alisa for bottoms which are compatible with all tops

# It might make sense to include Leo in women
chars_dict['leo'] = {'ghp': 'leo'}  # I may be able to include Leo in "women"

# bears, yoshimitsu, jack probably work differently
chars_dict['other'] = {
    'rbt':'Kuma',
    'ttr':'Panda',
    'cml':'Yoshimitsu',
    'ccn':'Jack'
}


# TODO: Leo is sometimes _f_ and sometimes _m_ depending on part, so I should really index by both part and char_type here in general.
#  This should work for everyone else and should work for Leo if you manually change it based on what char parts you're modding for them
char_type_letter_dict = {
    'men':'_m_',
    'women':'_f_',
    'alisa':'_f_',
    'leo':'_f_',
    'other':'_m_'
}
