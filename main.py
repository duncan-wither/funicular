#!/usr/bin/env python3

import toml
import json
import os
import requests
import glob
import re
import shutil


def getOMDB(key, title, year=""):
    url_str = "http://www.omdbapi.com/?t="
    tit_str = title.replace(" ", "+")
    if year != "":
        year_str = "&y=" + str(year)
    else:
        year_str = ""
    api_str = "&apikey=" + api_key
    response = requests.get(url_str + tit_str + year_str + api_str)
    resp_dict = response.json()
    return response


def setup_html_file(file_name):
    # print(file_name)
    shutil.copyfile("./resources/head.html", file_name)
    # with open('./resources/head.html','r') as fixed, open(file_name,'w') as work_file:
    #    for line in fixed:
    #         work_file.write(line)
    # fixed.close()
    # work_file.close()
    with open("./resources/header.html", "r") as fixed, open(
        file_name, "a"
    ) as work_file:
        for line in fixed:
            work_file.write(line)
    fixed.close()
    work_file.close()
    return


def close_html_file(filename):
    with open("./resources/footer.html", "r") as fixed, open(
        filename, "a"
    ) as work_file:
        for line in fixed:
            work_file.write(line)
    fixed.close()
    work_file.close()
    return


# Impoting Settings
# TODO: return an error if no config file.
config = toml.load("config.toml")

if config["API"][0]["use"]:
    get_data = True
else:
    get_data = False

if config["API"][0]["overwrite"]:
    get_all_data = True
else:
    get_all_data = False
# get_all_data=True ## ONLY FOR DEBUG

api_key = config["API"][0]["OMDB"]

if api_key == "":
    use_api = False
    print("Reccomended to get OMDB Key")
    print("Please include it in your config.toml")
    print("If you don't have one, register at: https://www.omdbapi.com/apikey.aspx")
else:
    use_api = True

stuff_with_no_data = []

for count, library in enumerate(config["Library"]):
    lib_location = library["location"]
    print(lib_location)
    lib_name = library["name"]
    html_filename = lib_location + lib_name.replace(" ", "_") + ".html"
    setup_html_file(html_filename)
    for folder_path in glob.glob(lib_location + "/*/"):
        print(folder_path)
        # Change the -2 here to a sum so it matches with the folder.
        folder_name = folder_path.split("/")[-2]
        year_re = re.search(".\(\d\d\d\d\)$", folder_name)

        filename = glob.glob(folder_path + "/" + folder_name + "*")
        print(filename)

        # glob.glob("./test_dirs/Films/*/")
        if year_re != None:
            year_str = folder_name.split("(")[-1][0:4]
            title_str = folder_name[0 : year_re.span(0)[0]]
        else:
            year_str = ""
            title_str = folder_name
        print(title_str)
        # if use_api: # Currenlty we're always using the api.
        info_path = folder_path + "info.json"
        # print(info_path)
        if not (os.path.exists(info_path)) or get_all_data:
            OMDB_resp = getOMDB(
                api_key, title_str, year_str
            )  # Calling function for OMDB req.
            OMDB_data = OMDB_resp.json()
            json_object = json.dumps(
                OMDB_resp.json(), indent=4
            )  # Converts to readable JSON
            with open(info_path, "w") as f:  # Writing to gile for later
                f.write(str(json_object))
            # print("Write Type=",type(OMDB_data)) # Comparison of type for debug
        else:  # If we've got a version cached read it.
            with open(info_path) as f:
                OMDB_data = json.load(f)
            # print("Read Type=",type(OMDB_data)) # Comparison of type for debug

        if OMDB_data["Response"] == "False":
            print("API Error:", OMDB_data["Error"], "(Film =", title_str, ")")
            stuff_with_no_data.append([folder_name])
            continue

        # print(OMDB_data["Poster"])
        # Getting Images
        img_url = OMDB_data["Poster"]
        img_path = folder_path + "cover.jpg"
        if not (os.path.exists(img_path)):  # Making sure we don't have one already
            img = requests.get(img_url)
            with open(img_path, "wb") as f:
                f.write(img.content)
        print("Filename:", filename, ", Type:", type(filename))
        link_url_string = "file:///" + os.path.realpath(filename[0])
        with open(html_filename, "a") as f:
            f.write('<div class="responsive">\n')
            f.write('  <div class="gallery">\n')
            f.write('    <a target="_blank" href="' + link_url_string + '">\n')
            f.write(
                '      <img src="'
                + "./"
                + folder_name
                + "/cover.jpg"
                + '" alt="link_" width="600" height="400">\n'
            )
            f.write("    </a>\n")
            f.write('    <div class="desc">' + title_str + "</div>\n")
            f.write("  </div>\n")
            f.write("</div>\n")

    close_html_file(html_filename)
    css_file_loc = lib_location + "/default.css"
    # print("CSS File Loc:"+css_file_loc)
    if not (os.path.exists(css_file_loc)):
        shutil.copyfile("./resources/default.css", css_file_loc)
