from typing import Tuple, List
import pandas as pd


# global this, dont need best practice for side projects
def check_day(original_time):
    # split on comma
    event_time = str(original_time).split(",")
    # get first element
    event_time = event_time[0].lower()
    if event_time in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        return original_time
    else:
        return None

def split_tables(url = "https://www.marketwatch.com/economy-politics/calendar")-> Tuple[List[pd.DataFrame], List[str]]:

    # extract calendar events from urls
    # for now only get the upcoming events for the current week
    df = pd.read_html(url)[0]

    # split df into separate arrays based on values in column "Time (ET)"
    # split by MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY

    tables = []

    event_times = []

    table = None
    current_day = None
    # iterate across df
    for index, row in df.iterrows():
        # check Time (ET) column for Monday, Tuesday, Wednesday, Thursday, Friday
        date_label = check_day(row["Time (ET)"])
        if date_label is not None:
            # append row to table
            # add row to table
            event_times.append(date_label)
            if table is not None:
                tables.append(table)
                table = None
            # create new table
            if table is None:
                current_day = row["Time (ET)"]
                # append old table
                columns = df.columns
                table = pd.DataFrame(columns=columns)
                table.style.set_caption(current_day)
                # table.loc[len(table)] = row
        else:
            # add row to table element
            table.loc[len(table)] = row
            
            # append last table
            if len(df) == index + 1:
                tables.append(table)
                table = None


    # write tables to file
    return tables, event_times
    
def main():
    tables, event_times = split_tables()
    print(tables)
    print(event_times)
# write tables to file

# if main
if __name__ == "__main__":
    main()