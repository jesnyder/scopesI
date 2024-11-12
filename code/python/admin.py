import json
import markdown
import os
import pandas as pd
import shutil


def retrieve_path(name):
    """
    
    """

    src_path = os.path.join("user_provided", "admin", "paths.csv")


    df = pd.read_csv(src_path)
    #print(df)

    names = list(df["name"])
    paths = list(df["path"])

    for i in range(len(names)):

        #print(names[i])
        #print(name)

        path = str(paths[i]).split(" ")   
        path = os.path.join(*path)
        #print(path)

        if str(names[i]) == str(name):
            check_folders_exist(path)
            return(path)
        

def check_folders_exist(path):
    """
    check if the path exists
    """

    #print(path)
    path_split = path.split("/")
    #print(path_split)

    for i in range(len(path_split)):

        a = i
        #print(a)
        short_path = path_split[0:a+1]
        built_path = os.path.join(*short_path)
        #print("built_path = ")
        #print(built_path)

        if "." in path_split[a]: continue

        if os.path.exists(built_path) == False: 
            os.mkdir(built_path)



def write_json(record_json, filename):
    """
    write json 
    """    

    #print(filename)
    if "." not in filename: filename = retrieve_path(filename)

    #print("filename = ")
    #print(filename)
    check_folders_exist(filename)

    #print(type(record_json))

    #print(record_json.keys())

    #if type(record_json) is list: record_json = {record_json}

    with open(filename, 'w') as f:
        json.dump(record_json, f, ensure_ascii=False, indent=4, sort_keys = True)




def write_js(record_json, filename):
    """
    write json 
    """

    if "." not in filename: 
        filename = retrieve_path(filename)

    #print("filename = ")
    #print(filename)
    check_folders_exist(filename)

    filename_split = filename.split("/")
    var_name = filename_split[-1].split(".")[0]

    if type(record_json) is dict: 
        if "name_record" in record_json: var_name = record_json["name_record"]

    with open(filename, 'w') as f:
        f.write("var " + str(var_name) + " = " )
        json.dump(record_json, f, ensure_ascii=False, indent=4, sort_keys = True)
        f.close()




def read_json(filename):
    """
    return json from a filename
    """

    if "." not in filename: 
        filename = retrieve_path(filename)

    #print(filename)
    with open(filename) as json_file:
        data = json.load(json_file)
        json_file.close()

    return(data)






def markdown_to_html(src_md, dst_html):
    """
    generate an html file 
    save to the provided filename 

    use data from provided markdown file 
    """


    with open(src_md, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)

    with open(dst_html, 'w') as f:
        f.write(html)



def markdown_insert_html(src_md, dst_html):
    """
    generate an html file 
    save to the provided filename 

    use data from provided markdown file 
    """

    # read in the markdown file 
    # convert the markdown to html 
    with open(src_md, 'r') as f:
        text = f.read()
        html = markdown.markdown(text)
        f.close()
    
    #print(text)
    #print(text[0])


    tag_rough = str(text).split(" -->")[0]
    #print("tag_rough = " + str(tag_rough))
    tag = tag_rough.split("-- ")[-1]
    #print("tag = " + str(tag))

    tag_begin = "<!-- " + str(tag) + " begin -->"
    tag_end = "<!-- " + str(tag) + " end -->"
    
    # read in the html file
    with open(dst_html, 'r') as f: 
        lines = f.readlines()
        f.close()

    # write the html 
    # insert the markdown below tag
    tag_bool = True
    with open(dst_html, 'w') as f:

        for line in lines:


            if tag_end in str(line): 
                f.write("\n")
                tag_bool = True

            if tag_bool == False: continue

            f.write(line)
            if tag_begin in str(line):
                f.write("\n")
                f.write(html)
                f.write("\n")

                tag_bool = False



def add_navigation_to_html(dst_html):
    """
    add navigation to folders 
    copy markdown and html to the folder if not there 
    """

    print("inserting navigation: dst_html = " + str(dst_html))

    tag_begin = "<!-- Side navigation begin -->"
    tag_end = "<!-- Side navigation end -->"

    # read in the html file
    with open(dst_html, 'r') as f: 

        lines = f.readlines()
        f.close()



    # list the folders in the same folder 
    fol_path = os.path.join(*str(dst_html).split("/")[0:-1])
    print("fol_path = ")
    print(fol_path)


    # write the html 
    # insert the navigation below tag
    tag_bool = True
    with open(dst_html, 'w') as f:

        for line in lines:


            if tag_end in str(line): 
                f.write("\n")
                tag_bool = True

            if tag_bool == False: 
                continue

            f.write(line)
            
            if tag_begin in str(line):
                f.write("\n")


                paths, names, fol_count = list_fols_for_nav(fol_path)
                
                # add link to style.css file
                insert_stylecss_link(dst_html,fol_count)

                for i in range(len(paths)):

                    f.write("<a href= \"" + paths[i] + "\">" + names[i] + "</a> <br> \n")

                f.write("\n")

                tag_bool = False

   


def list_fols_for_nav(fol_path):
    """
    return a list of paths and folder names 
    """

    paths = []
    names = []

    print("fol path = " + str(fol_path))

    top_path = os.path.join("docs")

    fol_split = str(fol_path).split("/")
    print("fol_split = ")
    print(fol_split)
    fol_count = len(fol_split)
    print("fol_count = " + str(fol_count))


    if fol_count > 1:

        rel_top_path = os.path.join(*([".."]*(fol_count-1)))
        print("rel_top_path = ")
        print(rel_top_path)
        paths.append(rel_top_path)

    else:
        rel_top_path = ".."
        paths.append(rel_top_path)
        rel_top_path = ""
    
    
    #paths.append(rel_top_path)
    names.append("About")

    

    for fol in os.listdir(top_path):

        if "." in fol: continue 
        path = os.path.join(rel_top_path, fol)
        if str(fol_path) in str(path):
            paths.append("#")
            names.append(fol)
            continue

        paths.append(path)
        names.append(fol)
        

            
                                


    print(fol_path)
    print(paths)
    print(names)



    return(paths, names, fol_count)



def insert_stylecss_link(dst_html,fol_count):
    """
    insert style link
    """

    if fol_count > 1:

        rel_top_path = os.path.join(*([".."]*(fol_count-1)))
        style_path = os.path.join(rel_top_path, "style.css")

    else:
        style_path = os.path.join("style.css")

    tag_begin = "<!-- Style.css insert begin -->"
    tag_end = "<!-- Style.css insert end -->"

    
    text = "<link rel=\"stylesheet\" href=\"" + str(style_path) + "\">\""

   # read in the html file
    with open(dst_html, 'r') as f: 

        lines = f.readlines()
        f.close()


    # write the html 
    # insert the markdown below tag
    tag_bool = True
    with open(dst_html, 'w') as f:

        for line in lines:


            if tag_end in str(line): 
                f.write("\n")
                tag_bool = True

            if tag_bool == False: continue

            f.write(line)
            if tag_begin in str(line):
                f.write("\n")
                f.write(text)
                f.write("\n")

                tag_bool = False



        