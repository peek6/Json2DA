This is a set of Python scripts for automating the importing of assets into UE.  It is based on scripts written for Hogwarts Legacy, now ported into UE 5.2 to support Tekken 8.  

Currently supports constructing dummy materials by importing the JSON files corresponding to material instances.  Importing other custom Tekken 8 datatypes is not supported yet, but I am working on it now.

For making custom MIs, you want to be able to edit texture, vector, or scalar parameters.  One way to do this is to follow the "MI Parent Swapping" approach described in [https://github.com/CDDTreborn/Tekken7_PC-Modding-Guides/wiki/Info-for-Modders-T8](https://github.com/CDDTreborn/Tekken7_PC-Modding-Guides/wiki/Info-for-Modders-T8) to set up a dummy material with the same name as an in-game material, add parameters for each parameter you will want to change, and then create instances of that dummy material in which you change those parameters.  You need to make sure you get every parameter name exactly right and there can be a large number of parameters for each material.  I have now automated this process for you.

1) Clone this repository into your UE project so that the Python scripts are in the Contents/Python directory.
   
2) Make sure your "Python Editor Script Plugin" is enabled.
![Screenshot (2326)](https://github.com/peek6/Json2DA/assets/28815226/251e4ac1-fe8e-4dce-9f0b-a2e4b1f86714)

3) In Editor Preferences, search for Python and enable Developer Mode and Content Browser Integration.
![Screenshot (2322)](https://github.com/peek6/Json2DA/assets/28815226/c4f2764b-6967-4925-a23c-e4a30bc85214)
  
4) To create a dummy master material for the MI you want to use as a parent, first create the MI in UE (it must have the same name and be in the same folder as the original game's MI you will want to use as a parent), then right-click on it, pick "Scripted Asset Actions" and "Import MI JSON", then point to the JSON from Fmodel which you want to import.  You can either import the JSON for the MI you want to use as a parent (for example, if you are using it for many different instances that inherit different parameters from the master), or the one you want to instance (for example, if you only want to see/change the parameters corresponding that single instance).  Then watch the magic happen.
![Screenshot (2328)](https://github.com/peek6/Json2DA/assets/28815226/42abb7ae-1ae1-484e-8c26-2b89e2406af4)

5) Create any instances of this parent MI that you want to customize and then customize these instances as you like by setting the parameters as desired.  You should be able to see the default values for each parameter and texture that will be inherited from the parent if you don't change them.  Make sure to overwrite anything you want to change.  Package your inherited customized instances with your chunk, but do not package the parents, so that the game will use the real parent MIs rather than your dummy ones.
