import json
import markdown 
import numpy as np
import os
import pandas as pd

from json import loads, dumps

# Python ICD10
# https://pypi.org/project/python-icd10/





def build_dataset():
    """
    """

    print("running build_dataset")

    tasks = [0]

    # add keys 
    num_county()
    enumerate_dengue()
    total_westnile()
    num_county()
    geojson_cdc()

    #organize_cdc()

    print("completed build_dataset")



def num_county():
    """
    number county
    """

    num_county = pd.read_csv(os.path.join("user_provided", "refs", "stateAbbr.csv"))
    print(num_county)

    src_df = os.path.join("user_provided", "Palmer2023.csv")
    print(src_df)
    df = pd.read_csv(src_df)

    for col in df.columns: 
        print(col)
        if "Unnamed" not in col: continue  
        print(df.columns)
        del df[col]


    df["County"] = list(df["ID"])


    county_codes = []
    for i in range(len(list(df["ID"]))):        

        county_num = str(df.loc[i]["ID"]).split("-")[1]
        
        print(county_num)

        state = df.loc[i]["State"]

        print("state = " + str(state))
        state_code = num_county[num_county["State"] == state]

        if len(list(state_code["State"])) == 0: 
            state_code = num_county[num_county["Abbreviation"] == state]

        print(state_code)

        state_code = list(state_code["Code"])[0]
        county_code = str(state_code).zfill(2) + county_num.zfill(3)
        print(county_code)

        county_codes.append(county_code)
    
    df["County"] = county_codes
    df.to_csv(src_df)




def total_westnile():
    """
    total westnile 
    """

    src_westnile = os.path.join("user_provided", "WestNile2023.csv")

    df = pd.read_csv(src_westnile)

    totals = []
    for i in range(len(df["Reported human cases"])):

        total = df.loc[i]["Reported human cases"]
        total = total + df.loc[i]["Neuroinvasive disease cases"]
        total = total + df.loc[i]["Identified by Blood Donor Screening"]
        totals.append(total)

    df["totals"] = totals

    for col in df.columns: 
        print(col)
        if "Unnamed" not in col: continue  
        print(df.columns)
        #df = df.drop([col])
        del df[col]

    df.to_csv(src_westnile)



def enumerate_dengue():
    """
    add data column to dengue 
    """

    for fil in os.listdir("user_provided"): 

        if "." not in fil: continue 
        if "Dengue" not in fil: continue 
        print(fil)

        df = pd.read_csv(os.path.join("user_provided", fil))

        for col in df.columns: 
            print(col)
            if "Unnamed" not in col: continue  
            print(df.columns)
            #df = df.drop([col])
            del df[col]
        
        if "LengendInt" in df.columns: df = df.drop(["LegendInt"])

        legendints = []
        for i in range(len(list(df["Legend"]))): 

            legendint = str(df.loc[i]["Legend"]).split(" ")[-1]
            if "+" in legendint: legendint = legendint.replace("+", "")

            legendint = int(legendint)
            legendints.append(legendint)

        df["LegendInts"] = legendints
        df.to_csv(os.path.join("user_provided", fil))



def retrieve_json(src):
    """
    return geojson from path     
    """

    with open(src, 'r') as file:
        src_json = json.load(file)

    return(src_json)



def save_json(dst_json, data):
    """
    save json to fil
    """

    with open(dst_json , 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)




def geojson_cdc():
    """
    add keys to geojson for cdc data 
    """

    src_geojson = os.path.join("docs", "js", "geojson.json")
    geojson = retrieve_json(src_geojson)
    print(geojson.keys())   

    src_path = os.path.join("user_provided")
    for fil in os.listdir(src_path): 
        
        if "." not in fil: continue
        print(fil)
        geojson = add_field(geojson, os.path.join(src_path, fil))


        dst_json = os.path.join("docs", "js", "cdc" + ".json")
        with open(dst_json , 'w') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=4)

        dst_json = os.path.join("docs", "js", "cdc" + ".js")
        with open(dst_json , 'w') as f:
            f.write("var cdc_stats = ")
            json.dump(geojson, f, ensure_ascii=False, indent=4)
            f.write(";")




def add_field(geojson, fil):
    """
    add geojson 
    """

    df = pd.read_csv(fil)

    name_data = str(fil.split("/")[-1]).split(".")[0]
    print(name_data)

    #print(geojson)
    #print(geojson.keys())

    for i in range(len(geojson["features"])):

        county = geojson["features"][i]

        if "properties" not in county.keys(): continue 
        #print(county["properties"]["countyFIDS"])

        countyFID = str(county["properties"]["GEO_ID"])[-5:]
        #print(countyFID)
        values = match_countyFID(fil, countyFID)
        
        geojson["features"][i]["properties"][name_data] = values  

    return(geojson)



def match_countyFID(fil, countyFID):
    """
    return json of values 
    """

    values = {}
    values["color"] = "rgba(255, 255, 255, 0.01)"
    values["value"] = 0

    df = pd.read_csv(fil)

    for i in range(len(list(df["County"]))): 

        #print(str(df.loc[i]["County"]).zfill(5))
        #print(str(countyFID).zfill(5))

        if str(df.loc[i]["County"]).zfill(5) != str(countyFID).zfill(5): continue
        #print("county matched!") 

        for col in df.columns: 
            if "Unnamed" in col: continue
            if "County" in col: continue
            if "LegendInts" in col: continue
            if "Population" in col: continue
            if "Year" in col: continue

            values[col] = str(df.loc[i][col])

        if "LegendInts" in df.columns: target_col = "LegendInts"
        elif "Value" in df.columns: target_col = "Value"
        elif "Incidence" in df.columns: target_col = "Incidence"
        elif "totals" in df.columns: target_col = "totals"
        
        #values["value"] = df.loc[i][target_col]
        #print(fil)
        #print(target_col)
        #print(i)
        values["color"] = assign_color(target_col, i, df, fil)

        return(values)

    return(values)


def assign_color(col, i, df, fil):
    """
    assign rgb value 
    """

    max_value = float(max(list(df[col])))
    min_value = float(min(list(df[col])))
    
    if "Dengue" in fil: min_value = 0 
    if "WestNile" in fil: min_value = 0 

    value = float(df.loc[i][col])
    normalized = (value - min_value)/(max_value-min_value)
    modifier = (value - min_value)/(max_value-min_value)*255
    
    r = int(255)
    g = int(modifier)*0.9
    b = int(modifier)*0.33

    a = 0.7

     

    color = str("rgba( " + str(r) + " , " + str(g) + " , " + str(b) + " , " + str(a) + ")")


    if "Dengue" in fil: 
        if normalized < 0.01: a = 0 
        color = str("rgba( " + str(r) + " , " + str(b) + " , " + str(b) + " , " + str(a) + ")")

    elif "WestNile" in fil: 
        if normalized < 0.01: a = 0 
        color = str("rgba( " + str(r) + " , " + str(g) + " , " + str(r) + " , " + str(a) + ")")

    elif "Palmer" in fil: 
        if normalized <= 0.55 and normalized >= 0.45: a = 0 

        if normalized > 0.5: color = str("rgba( " + str(b) + " , " + str(r) + " , " + str(b) + " , " + str(a) + ")")
        else: color = str("rgba( " + str(g) + " , " + str(g) + " , " + str(g) + " , " + str(a) + ")")
 
    return(color)



def organize_cdc():
    """
    turn downloaded csv to json 
    create a .json for each virus 
    """

    dst_path = os.path.join("user_provided")
    for fol in os.listdir(dst_path):

        data = {}

        dst_fol = os.path.join(dst_path, fol)
        for fil in os.listdir(dst_fol):

            dst_fil = os.path.join(dst_fol, fil)
            df = pd.read_csv(dst_fil)

            print(df.columns)

            #result = df.to_json(orient="split")
            #parsed = loads(result)
            #dumps(parsed, indent=4)  

            years = np.linspace(1990, 2024, num=2024-1990+1)
            for year in years: 
                
                year = int(year)
                print(year)
                print(df["Year"][0])

                if year != df["Year"][0]: continue 

                #if "County" not in df.columns: continue 

                print(" list(df[County]) = ")
                print(list(df["County"]))


                for county in list(df["County"]):

                    print(df)

                    county = str(county).zfill(5)

                    df_temp = df[df["County"] == county]

                    if len(list(df_temp["County"])) < 1: continue
                    

                    values = {}
                    for col_temp in df_temp.columns: 

                        if len(list(df_temp[col_temp])) < 1: print(df_temp)

                        if col_temp == "County": continue 
                        if col_temp == "Year": continue 
                        print(list(df_temp[col_temp]))
                        values[col_temp] = list(df_temp[col_temp])[0]

                    if values == {}: continue
                    
                    
                    if county not in data.keys(): data[county] = {}
                    if year not in data[county].keys(): data[county][year] = {}
                    data[county][year] = values
                
            
                dst_json = os.path.join("code", "json", fol + ".json")
                with open(dst_json , 'w') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    build_dataset()
