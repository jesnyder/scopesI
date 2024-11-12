import markdown 
import os

from admin import check_folders_exist

def markdown_to_html():
    """
    """

    print("running markdown to html")

    tasks = [0]

    src_md = os.path.join("code", "markdown")
    dst_md = os.path.join("code", "html")

    for fil in os.listdir(src_md): 

        print(fil)
        if ".md" not in fil: continue 
        
        src_fil = os.path.join(src_md, fil)
        dst_fil = os.path.join(dst_md, fil.split(".")[0] + ".html")

        with open(src_fil) as s: md = s.read()

        print(md)

        html = markdown.markdown(md)
        print(html)


        check_folders_exist(dst_fil)
        with open(dst_fil, 'w+') as d: d.write(html)


        dst_docs = os.path.join("docs", "index.html")
        insert_markdown_to_html(dst_docs, html)
            

    print("completed markdown to html")


def insert_markdown_to_html(dst_html, htmls):
    """
    find existing html 
    locate tag 
    insert markdown 
    return lines to be written as html 
    """

    f = open(dst_html, "r")
    lines = f.readlines()
    f.close() 

    dst_lines = []
    append_bool = True
    for line in lines: 
        
        if "<!-- Insert index markdown end -->" in str(line): 
            append_bool = True 
        
        if append_bool == True: 
            dst_lines.append(line)

        if "<!-- Insert index markdown begin -->" in str(line): 
            dst_lines.append("\n \n")
            for html in htmls: 
                dst_lines.append(html)
            dst_lines.append("\n \n")
            append_bool = False
    

    with open(dst_html, 'w+') as d: 
        for dst_line in dst_lines: 
            d.write(dst_line) 


if __name__ == "__main__":
    markdown_to_html()
