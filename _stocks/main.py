import subprocess

from bs4 import BeautifulSoup
from daterangeparser import parse as drparse
from datetime import datetime, date as datetime_date
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
    data = []

    # first, get table
    dates = []
    curr_timestamp = datetime.now()
    for cell in stocking_table.tbody.tr.children:
        cell_data = list(cell.stripped_strings)
        if len(cell_data) == 0:
            continue

        if len(cell_data) == 2:
            date, species = cell_data[0], cell_data[1]
        else:
            date = cell_data[0]
            species = "trout"
        print(date)

        start_date, end_date = drparse(str(date).replace('\xa0', ' '))
        # correct year if no year was specified
        start_date_o = start_date.replace(year=start_date.year - 1)
        end_date_o = end_date.replace(year=end_date.year - 1)

        if abs(start_date_o - curr_timestamp) < abs(start_date - curr_timestamp):
            start_date = start_date_o
        if abs(end_date_o - curr_timestamp) < abs(end_date - curr_timestamp):
            end_date = end_date_o

        dates.append({"start_date": start_date, "end_date": end_date, "species": species})


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
                try:
                    lbs = int(entry)
                except Exception as e:
                    print(f"Lb parsing error, substituting in 0 lbs: {e=}")
                    lbs = 0
                
                start_date = dates[time_i]["start_date"]
                end_date = dates[time_i]["end_date"]
                species = dates[time_i]["species"]
                stocking_data.append({"start_date": start_date, "end_date": end_date, "location": location, "amount": lbs, "source": "EBRPD", "species": species}) #[location].append((dates[time_i], lbs))

    print(f"EBRPD stocking: {stocking_data}")
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

            species = str(stocking_entry_cells[3].string).strip()
                
            stocking_data.append({"start_date": start_date, "end_date": end_date, "location": location_key, "amount": -1, "source": "DFG", "species": species})
        
        #print(f"DFG stocking: {stocking_data}")
        return stocking_data
    else:
        print("Couldn't find DFG stocking table.")
        return []
    
def get_vaqueros_old():
     # The command and its arguments should be passed as a list for safety
    command = "curl \"https://www.ccwater.com/149/Fishing\""
    
    try:
        vaq_html = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True).stdout
    except subprocess.CalledProcessError as e:
        print("DFG curl command failed with error:", e.stderr)
        return []
    soup = BeautifulSoup(vaq_html, 'lxml')


    all_tables = soup.find_all("table")

    all_stocking_data = []


    def get_stocks_for_species(species):
        stocking_data = []
        stocking_table = None
        for table in all_tables:
            row_text = " ".join(table.tbody.tr.stripped_strings)
            if species in row_text:
                stocking_table = table
                break
        
        if stocking_table is None:
            print("Could not find Vaqueros stocking table.")
            return []
        
        stocking_entries = table.tbody.find_all("tr")
        for entry in stocking_entries:
            entry_cells = list(entry.stripped_strings)
            date = datetime.strptime(entry_cells[0], '%m/%d/%Y')

            try:
                lbs = int(entry_cells[1].split(" ")[0].replace(',', ''))
            except:
                lbs = -1

            if entry_cells[2] == "Lassen Trout":
                stocking_data.append({"start_date": date, "end_date": date, "location": "los-vaqueros", "amount": lbs, "source": "CCWD", "species": "Lassen Trout"})
            elif species == "Tsai":
                stocking_data.append({"start_date": date, "end_date": date, "location": "los-vaqueros", "amount": lbs, "source": "CCWD", "species": "Channel Catfish"})
            else:
                print("Unknown stocking source:", entry_cells)
        print(stocking_data)
        return stocking_data
    all_stocking_data = get_stocks_for_species("Trout") + get_stocks_for_species("Tsai")
    return all_stocking_data
import re
def get_vaqueros():
    # The command and its arguments should be passed as a list for safety
    command = "curl \"https://www.ccwater.com/149/Fishing\""
    
    try:
        vaq_html = subprocess.run(command, capture_output=True, text=True, check=True, encoding='utf-8', shell=True).stdout
    except subprocess.CalledProcessError as e:
        print("DFG curl command failed with error:", e.stderr)
        return []
    soup = BeautifulSoup(vaq_html, 'lxml')
    header = soup.find("h3", string="Recent Fish Plants")

    stocking_data = []
    if header:
        ul = header.find_next("ul")

        stocking_entries = ul.find_all("li")

        for stocking_entry in stocking_entries:
            entry_txt = stocking_entry.get_text(strip=True)

            stocking_date_str, stocking_amt_str = entry_txt.split(":")

            stocking_date = datetime.strptime(stocking_date_str, "%B %d, %Y")

            pattern = re.compile(
                r'([\d,]+)\s+(?:lb|lbs|pound|pounds)\s+of\s+(.+)',
                re.IGNORECASE,
            )

            m = pattern.match(stocking_amt_str)
            stocking_amt = int(m.group(1).replace(",", ""))
            species = m.group(2)

            stocking_data.append({"start_date": stocking_date, "end_date": stocking_date, "location": "los-vaqueros", "amount": stocking_amt, "source": "CCWD", "species": species})


    return stocking_data


old_stocking_load = ["EBRPD"]

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, datetime_date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))

def load_old_stocking():
    try:
        with open(os.path.join(rel_path, "stocking_cache.json")) as f:
            old_stocking = json.load(f)


            # all we need to do is return dates to datetime objects

            old_stocking_proc = []

            for entry in old_stocking:
                if entry["source"] in old_stocking_load:
                    old_stocking_proc.append(entry)
            return old_stocking_proc
    except:
        return []
    

def entry_to_key(entry):
    # index everything but lbs
    return frozenset({k:v for k, v in entry.items() if k != "amount"})



if __name__ == "__main__":
    ebrpd_stocking = get_ebrpd()
    dfg_stocking = get_dfg()
    vaq_stocking = get_vaqueros()
    old_stocking = load_old_stocking()

    # stocking entries: (date, location, lbs, source)

    # combine stocking info
    full_stocking = ebrpd_stocking + vaq_stocking # + dfg_stocking + vaq_stocking

    # add old stocks that do not conflate with current stocks
    # 1: create dict mapping entries to lbs
    old_stocking_valid = []
    stocking_dict = {}
    for entry in full_stocking:
        stocking_dict[entry_to_key(entry)] = entry["amount"]
    # 2: check if entry is in new dict
    
    for entry in old_stocking:
        if entry_to_key(entry) not in stocking_dict:
            old_stocking_valid.append(entry)
    print(f"Loading old stockings: {old_stocking_valid}")
    full_stocking = full_stocking + old_stocking_valid

    # remove any entries that are any older than one month
    curr_timestamp = datetime.now()

    relevant_stocking = []
    for entry in full_stocking:
        entry_date = entry["start_date"]
        date_diff = curr_timestamp - entry_date

        if date_diff.days < 30 and entry["amount"] != 0:
            relevant_stocking.append(entry)

    # remove dupes
    # relevant_stocking = list(set(relevant_stocking))

    # now, sort by date
    relevant_stocking.sort(key=(lambda x: x["start_date"]), reverse=True)


    # finally, convert entries to format expected by Jekyll
    output_stocking = []
    for i in range(len(relevant_stocking)):
        entry = relevant_stocking[i]
        start_date = entry["start_date"]
        end_date = entry["end_date"]
        start_date_str = start_date.strftime('%m/%d/%Y')
        end_date_str = end_date.strftime('%m/%d/%Y')


        output_stocking.append((f"{start_date_str}-{end_date_str}", entry["location"], entry["amount"], entry["source"]))

    print("Processed stocking:", relevant_stocking)


    with open(os.path.join(rel_path, "stocking_cache.json"), "w") as f:
        json.dump(relevant_stocking, f, indent=2, default=json_serial)
    with open(os.path.join("_data", "stocking.json"), "w") as f:
        json.dump(relevant_stocking, f, indent=2, default=json_serial)
