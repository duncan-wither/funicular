# funicular

A way of accessing your local video archive via the browser.
Effectively a static website with some simple pictures and automatic links.

## Info
Looks for a `config.toml` for config. Durr.

`template/` holds the html templates you might want to use.
Categories are:
 - `picture_list.html`
    - picture list pages, good for films or series pages
 - `list.html`
    - test list pages, for TV
 - `player.html`
    - the page with the file to play???

## Config
 - The `Library` table contains info about the libraries.
   - Most fields are self explanitory.
   - The `folder_stucture` list is how it will display folders as you go from top level down to the video files.
     - The options are the same as the template file names.
     - `endpoint` is means that the file is there
       - this pushes the layer above to launch the video when clicked.
       - look to use the VLC URI.
