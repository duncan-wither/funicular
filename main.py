import toml
import os

# Impoting Settings
# TODO: return an error if no config file.
config=toml.load("config.toml")

#
for count, location in enumerate(config['Library']):
  library=data['Libraries'][count]
  lib_location=library["location"]
  lib_name=library["name"]
  lib_depth=library["depth"]




## If page class is picture
## for each folder
##   look for index.png in folder
##   if so image_string = folder/index.png
##   elseif image_string = default_image.png
##   description_string = folder name
##   if next page_class is "endpoint" link_sting=file_in_folder (USE VLC URI)
##   else link_str = folder/index.html and recurse here!!
##
##   Return from recursion...
##
##   convert strings to html format.
##
##   Then copy the following to index.html
##   <div class="responsive">
##     <div class="gallery">
##       <a target="_blank" href="link_sting">
##         <img src="image_string" alt="link_" width="600" height="400">
##       </a>
##       <div class="desc">Add a description of the image here</div>
##     </div>
##   </div>


# Folders in dir: [f.path for f in os.scandir("/home/slam/Pictures") if f.is_dir() ])
# Folder and sub folders in dir: [x[0] for x in os.walk(directory)]
