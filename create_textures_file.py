# Creates a text file with all the textures in your project, which you can then use to replace the dummy textures with the real ones.

# Author:  peek6

# Usage:  point the script to your exported textures from Umodel or Fmodel and to your UE project root, and run the script.

from pathlib import Path

# TODO: Set this to root of Game in Umodel texture extraction folder
texture_root = r"D:\modding\T8\vanilla_textures"

# TODO: Set this to your UE project root
project_root = r"D:\polar_project_custom_git"

p = Path(project_root+'\\Content')

count=0

file_str = ''

for file in p.glob('**/T_*.uasset'):
    texture_path_in_project = str(file)

    tokens = texture_path_in_project.split('\\')
    asset_name = tokens[-1].split('.')[0]
    tokens_after_content = []
    found_content = False
    for token in tokens[:-1]:
        if (token == 'Content'):
            found_content = True
            tokens_after_content.append('Game')
        else:
            if (found_content):
                tokens_after_content.append(token)
    asset_path = '/' + '/'.join(tokens_after_content) + '/'


    texture_path_to_import = texture_root + '\\'.join(asset_path.split('/'))+asset_name+".tga"

    #print(texture_path_in_project)
    #print(asset_path + ', ' + asset_name)
    #print(texture_path_to_import)

    if (Path(texture_path_to_import).is_file()):
        file_size = Path(texture_path_in_project).stat().st_size
        # if file_size < 10000:
        #print("Size of "+asset_name+" is "+ str(Path(texture_path_in_project).stat().st_size) )
        file_str = file_str + texture_path_to_import + '\n'
        count = count+1
        #if(asset_name[-2:]=='_C'):
        #    task_tuples.append((texture_path_to_import, asset_path)) #, 'srgb', True, 'never_stream', True))
        #else:
        #    task_tuples.append((texture_path_to_import, asset_path)) #, 'srgb',False, 'never_stream', True))
        #count = count + 1
        #tasks.append(buildImportTask(texture_path_to_import, asset_path))
    else:
        print("WARNING:  texture "+asset_name+" not found in umodel extract directory.")


print("Found "+str(count)+" texture files in the project.")


with open('all_textures.txt','w') as fp:
    fp.write(file_str)