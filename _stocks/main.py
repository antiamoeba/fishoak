import subprocess

from bs4 import BeautifulSoup
from daterangeparser import parse as drparse
from datetime import datetime
import json
import os

rel_path = "_stocks"
def get_ebrpd():
    with open(os.path.join(rel_path, "ebrpd_aliases.json"), "r") as f:
        ebrpd_aliases = json.load(f)
    # The command and its arguments should be passed as a list for safety
    command = "curl \"https://www.ebparks.org/recreation/fishing/anglers-edge-online\""
    
    try:
        ebrpd_html = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True).stdout
    except subprocess.CalledProcessError as e:
        print("EBRPD curl command failed with error:", e.stderr)
        return []
    

    # now, parse html
    soup = BeautifulSoup(ebrpd_html, 'lxml')

    all_tables = soup.find_all('table')
    stocking_table = None
    for table in all_tables:
        # check for "Location" tag to make sure it is the stocking table
        if str(table.tbody.find_all("tr")[1].td.string) == "Location":
            stocking_table = table
            break
    
    if stocking_table is None:
        print("Couldn't find EBRPD stocking table.")
        return []
    
    # get dates
    dates = []
    curr_timestamp = datetime.now()
    for date in stocking_table.tbody.tr.stripped_strings:
        start_date, end_date = drparse(str(date))
        # correct year if no year was specified
        start_date_o = start_date.replace(year=start_date.year - 1)
        end_date_o = end_date.replace(year=end_date.year - 1)

        if abs(start_date_o - curr_timestamp) < abs(start_date - curr_timestamp):
            start_date = start_date_o
        if abs(end_date_o - curr_timestamp) < abs(end_date - curr_timestamp):
            end_date = end_date_o

        dates.append((start_date, end_date))


    # now, extract locations/dates (we'll remove zeros from here)
    stocking_loc_rows = table.tbody.find_all("tr")[2:]

    stocking_data = []
    for stocking_loc_row in stocking_loc_rows:
        location = None
        for i, entry in enumerate(stocking_loc_row.stripped_strings):
            if i == 0:
                # this should be the location name
                if entry in ebrpd_aliases:
                    location = ebrpd_aliases[entry]
                else:
                    location = entry
            else:
                time_i = i - 1 # account for location name index
                lbs = int(entry)
                if lbs > 0:
                    stocking_data.append((dates[time_i], location, lbs, "EBRPD")) #[location].append((dates[time_i], lbs))

    #print(f"EBRPD stocking: {stocking_data}")
    return stocking_data

def get_dfg():
    with open(os.path.join(rel_path, "dfg_aliases.json"), "r") as f:
        dfg_aliases = json.load(f)
    # The command and its arguments should be passed as a list for safety
    command = "curl \"https://nrm.dfg.ca.gov/fishplants/publicplantsearch?Params.Regions=R3&Params.Counties=1&Params.Counties=7&Params.Counties=21&Params.Counties=28&Params.Counties=38&Params.Counties=41&Params.Counties=43&Params.Counties=44&Params.Counties=48&Params.Counties=49&RegionCountyMappings=&Params.PlantTimeFrame=1&submit=Search\""
    
    try:
        dfg_html = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True).stdout
    except subprocess.CalledProcessError as e:
        print("DFG curl command failed with error:", e.stderr)
        return []
    soup = BeautifulSoup(dfg_html, 'lxml')
    
    table_id = "fishPlantsExternal"
    stocking_table = soup.find('table', {'id': table_id})

    if stocking_table:
        stocking_entries = stocking_table.tbody.find_all("tr")
        stocking_data = []
        for stocking_entry in stocking_entries:
            stocking_entry_cells = stocking_entry.find_all("td")
            stocking_date_str = str(stocking_entry_cells[0].string).strip()
            start_date_str, end_date_str = stocking_date_str.split("-")
            start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
            end_date = datetime.strptime(end_date_str, '%m/%d/%Y')
            # start_date, end_date = drparse(stocking_date_str) doesn't seem like drparse can handle this string

            location = str(stocking_entry_cells[1].find(text=True).string).strip()
            county = str(stocking_entry_cells[2].string).strip()

            if location + "_" + county in dfg_aliases:
                location_key = dfg_aliases[location + "_" + county]
            else:
                location_key = f"{location} ({county})"
                
            stocking_data.append(((start_date, end_date), location_key, -1, "DFG"))
        
        #print(f"DFG stocking: {stocking_data}")
        return stocking_data
    else:
        print("Couldn't find DFG stocking table.")
        return []
    
def get_vaqueros():
     # The command and its arguments should be passed as a list for safety
    command = "curl \"https://www.ccwater.com/149/Fishing\""
    
    try:
        vaq_html = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True).stdout
    except subprocess.CalledProcessError as e:
        print("DFG curl command failed with error:", e.stderr)
        return []
    soup = BeautifulSoup(vaq_html, 'lxml')


    all_tables = soup.find_all("table")
    stocking_table = None
    for table in all_tables:
        row_text = " ".join(table.tbody.tr.stripped_strings)
        if "Trout" in row_text:
            stocking_table = table
            break
    
    if stocking_table is None:
        print("Could not find Vaqueros stocking table.")
        return []
    
    stocking_entries = table.tbody.find_all("tr")
    stocking_data = []
    for entry in stocking_entries:
        entry_cells = list(entry.stripped_strings)
        date = datetime.strptime(entry_cells[0], '%m/%d/%Y')

        try:
            lbs = int(entry_cells[1].split(" ")[0].replace(',', ''))
        except:
            lbs = -1

        if entry_cells[2] == "Lassen Trout":
            stocking_data.append((date, "los-vaqueros", lbs, "CCWD"))
        else:
            print("Unknown stocking source:", entry_cells)
    return stocking_data

def load_old_stocking():
    try:
        with open(os.path.join(rel_path, "stocking.json")) as f:
            old_stocking = json.load(f)


            # all we need to do is return dates to datetime objects

            old_stocking_proc = []

            for entry in old_stocking:
                if "-" in entry[0]:
                    start_date_str, end_date_str = entry[0].split("-")
                    start_date = datetime.strptime(start_date_str, '%m/%d/%Y')
                    end_date = datetime.strptime(end_date_str, '%m/%d/%Y')

                    old_stocking_proc.append(((start_date, end_date), entry[1], entry[2], entry[3]))
                else:
                    start_date = datetime.strptime(entry[0], '%m/%d/%Y')
                    old_stocking_proc.append((start_date, entry[1], entry[2], entry[3]))
            
            return old_stocking_proc
    except:
        return []


if __name__ == "__main__":
    ebrpd_stocking = get_ebrpd()
    dfg_stocking = get_dfg()
    vaq_stocking = get_vaqueros()
    old_stocking = load_old_stocking()


    # combine stocking info
    full_stocking = old_stocking + ebrpd_stocking + dfg_stocking + vaq_stocking

    # remove any entries that are any older than one month
    curr_timestamp = datetime.now()

    relevant_stocking = []
    for entry in full_stocking:
        entry_date = entry[0]

        if isinstance(entry_date, tuple):
            entry_date = entry_date[0]

        date_diff = curr_timestamp - entry_date

        if date_diff.days < 30:
            relevant_stocking.append(entry)

    # remove dupes
    relevant_stocking = list(set(relevant_stocking))

    # now, sort by date
    relevant_stocking.sort(key=(lambda x: x[0][0] if isinstance(x[0], tuple) else x[0]), reverse=True)


    # finally, convert dates to standard format
    for i in range(len(relevant_stocking)):
        entry = relevant_stocking[i]
        if isinstance(entry[0], tuple):
            start_date = entry[0][0]
            end_date = entry[0][1]
            start_date_str = start_date.strftime('%m/%d/%Y')
            end_date_str = end_date.strftime('%m/%d/%Y')


            relevant_stocking[i] = (f"{start_date_str}-{end_date_str}", entry[1], entry[2], entry[3])
        else:
            start_date_str = entry[0].strftime('%m/%d/%Y')


            relevant_stocking[i] = (f"{start_date_str}", entry[1], entry[2], entry[3])


    print("Processed stocking:", relevant_stocking)


    with open(os.path.join(rel_path, "stocking.json"), "w") as f:
        json.dump(relevant_stocking, f, indent=2)
    with open(os.path.join("_data", "stocking.json"), "w") as f:
        json.dump(relevant_stocking, f, indent=2)
