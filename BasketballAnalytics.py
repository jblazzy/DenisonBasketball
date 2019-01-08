"""
-- BasketballAnalytics.py
-- Josh Blaz
-- Denison University -- c/o 2019
-- blaz_j1@denison.edu
NOTE: User must enter SST credentials below @ lines 88 & 89
"""

# Imports allowing the use of Selenium and Geckodriver. 
from lxml import html
from selenium import webdriver
# Allows us to send keys through the Webdriver.
from selenium.webdriver.common.keys import Keys 
# Allows us to wait for certain elements to load in. Gives us much more control over the Webdriver.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Allows us to write a function that confirms the existence of an element (EBS issue)
from selenium.common.exceptions import NoSuchElementException  
# Imported to use simple sleep function. (used rarely)
import time 
# Import pandas allowing us to export Lists of Lists to excel files.
import pandas as pd

def dropdown(team):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - 
    Determines the input team's dropdown search string. Only NCAC teams.
    '''
    if team == "Denison":
        return "Denison (OH) Big Red"
    elif team == "Wittenberg" or "Witt":
        return "Wittenberg"
    elif team == "Wooster":
        return "Wooster Fighting Scots"
    elif team == "OWU":
        return "Ohio Wesleyan"
    elif team == "Hiram":
        return "Hiram Terriers"
    elif team == "Wabash":
        return "Wabash College Little Giants"
    elif team == "Depauw":
        return "DePauw University Tigers"
    elif team == "Oberlin":
        return "Oberlin College Yeomen"
    elif team == "Kenyon":
        return "Kenyon Lords"
    elif team == "Allegheny":
        return "Allegheny Gators"

def confirm_element(xpath,driver):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

    Function that confirms the existence of an element, given that element's xpath.
    The reason for this function is that some teams don't record Extended Box Score (EBS), which we need
    to analyze data. IE: Mount Vernon Nazarene
    xpath - xpath of the element whose existence we're confirming
    driver - webdriver used to access the site, pass this so we don't have to create another webdriver
    If this element does not exist, we need to skip this team.
    Returns True if the element exists, False if not.
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ''' 
    if driver.find_elements_by_xpath(xpath):
        return True
    else:
        return False


def teamData(team, data1, data2, opp1, opp2):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    Function aggregating EBS stats from every game of every team into each team's respective List of Lists of Lists.
    team - team whose data is currently being collected.
    data1 - list of list of lists storing all of the first tables of every game for this team
    data2 - same as above, but stores the second table of each game
    opp1 and opp2 - storage for the opponent's tables for each game
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
    
    # make sure datasets are cleared first
    data1.clear()
    data2.clear()

    # create new driver
    driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')
    driver.get("https://www.synergysportstech.com/synergy/")
    assert "Synergy" in driver.title
    
    # *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
    # NOTE: USER: Insert Sports Synergy Tech Credentials below
    
    user = driver.find_element_by_name("txtUserName")
    pword = driver.find_element_by_name("txtPassword")

    # Clear previous inputs
    user.clear() 
    pword.clear()

    # Send the User's SST Email and Pass to the text field elements
    user.send_keys("sullivanc@denison.edu") # Insert Email inside of quotes
    pword.send_keys("Bigred1014")  # Insert Password inside of quotes
    
    pword.send_keys(Keys.RETURN) # Presses "Enter" Key, submitting the credentials to SST

    # *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
    # Extended Box Score (EBS) Collections

    # WebDriverWait allows us to wait until a certain condition is met. In this case we're waiting for the "Game" button.
    ## Path used to access 'Game' button
    Game_xpath = '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/div[2]/center/div[2]/div[2]/table[3]/tbody/tr[2]/td/center/a/font/b'
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, Game_xpath))) ## Wait until the 'Game' button loads in
    gameButton = driver.find_element_by_xpath(Game_xpath)
    gameButton.click()

    # Use the 'dropdown' function in order to find the correct 'dropdown string' for the team on the SST site.
    # This string is then entered into the textbox at 'dropdownpath', we wait for the textbox to load in before we fill it.
    dropdown_wait = WebDriverWait(driver, 10)
    dropdown_wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_MainContent_lstTeamA"]'))) ## Wait until the 'Game' button loads in
    DDstring = dropdown(team)
    dropdownpath = '//*[@id="ctl00_MainContent_lstTeamA"]/option[text()="{}"]'.format(DDstring)
    elem = driver.find_element_by_xpath(dropdownpath).click()
    time.sleep(3)
    # row_count is the number of games the current team played this season. 
    row_count = len(driver.find_elements_by_xpath("//table[2]/tbody/tr"))

    # We iterate through the table containing every game for the current team in this season, and select (click) each one.
    ## Once we select the game, we can access the game's data
    shortWait = WebDriverWait(driver, 5)
    shortWait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/table[2]/tbody/tr[2]/td[2]/a')))

    # Can't have games that don't have EBS
    for i in range(2, row_count + 1):
        path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/table[2]/tbody/tr[{}]/td[2]/a".format(i)
        elem = driver.find_element_by_xpath(path)
        print(elem.text)
        if elem.text != "Denison(OH)@MountVernon":
            elem.click()
    # Now we have a tab open for each game played in the season, each tab has the EBS we want to scrape.
    driver.switch_to.default_content()

    ## Preliminary for loop to make sure each game has an EBS, before we dive into the fat for loop
    ## If a game doesn't have 'home team' and 'away team' elements, then it doesn't have an EBS
    ## NOTE: if a game has an EBS, it will start on the EBS tab
    
    home_xpath = '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr[1]/td[1]'
    away_xpath = '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr[1]/td[1]'
    EBS_xpath =  '//*[@id="ctl00_MainContent_btnBoxScore"]'
    

    # need a list of indices that we skip - these are games that don't have Extended Box Scores -- no data
    for i in range(1, len(driver.window_handles)): 

        driver.switch_to.window(driver.window_handles[i])

        # Find Home team
        wait = WebDriverWait(driver, 30) 
        wait.until(EC.presence_of_element_located((By.XPATH, home_xpath)))
        hometeam = driver.find_element_by_xpath(home_xpath)

        # Find Away team
        wait.until(EC.presence_of_element_located((By.XPATH, away_xpath)))
        awayteam = driver.find_element_by_xpath(away_xpath)

        row_count_table1 = len(driver.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr'))
        row_count_table2 = len(driver.find_elements_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr'))

        # Variable counts for both EBS tables on each tab.
        col_count_table1 = 16 
        col_count_table2 = 22 
            
        # 4 Outer lists to prevent scope issues.
        tempOuter1 = []
        tempOuter2 = []
        tempOuter3 = []
        tempOuter4 = []
    

        """
        If the current team is the home team, we collect both Home EBS tables (1st and 2nd for loops) and both Away EBS tables
        (3rd and 4th for loops). This logic proceeds with the formatting of the table - the Home team's tables are always first
        and the Away team's tables second.
        """
        if hometeam.text == DDstring:
            for i in range (2, row_count_table1 + 1): # team table 1 (Home)
                tempInner = []
                for x in range(1, col_count_table1):
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem1 = driver.find_element_by_xpath(path)
                    tempInner.append(elem1.text)
                    if len(tempInner) == 15:
                        tempOuter1.append(tempInner)
            data1.append(tempOuter1) # append this table (stored as a list of lists) into the team LoLoL


            for i in range(2, row_count_table1 + 1): # team table 2 (Home)
                tempInner = []
                for x in range(1,col_count_table2): 
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[2]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem2 = driver.find_element_by_xpath(path)
                    tempInner.append(elem2.text)
                    if len(tempInner) == 15:
                        tempOuter2.append(tempInner)
            data2.append(tempOuter2)   
            
            for i in range(2, row_count_table2 + 1): # Opponent team table 1 (Away)
                tempInner = []
                for x in range(1, col_count_table1): 
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem1 = driver.find_element_by_xpath(path)
                    tempInner.append(elem1.text)
                    if len(tempInner) == 15:
                        tempOuter3.append(tempInner)
            opp1.append(tempOuter3)      
                    
            for i in range(2, row_count_table2 + 1): # Opponent team table 1 (Away)
                tempInner = []
                for x in range(1,col_count_table2):
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[4]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem2 = driver.find_element_by_xpath(path)
                    tempInner.append(elem2.text)
                    if len(tempInner) == 15:
                        tempOuter4.append(tempInner)
            opp2.append(tempOuter4)


        else: 
            """
            Current team is the away team, so we collect away data first (1st and 2nd for loop), and then the home team data
            AKA the opponent Data (3rd and 4th for loops)
            """
            for i in range(2, row_count_table2 + 1): # team table 1 (Away)
                tempInner = []
                for x in range(1, col_count_table1): 
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem1 = driver.find_element_by_xpath(path)
                    tempInner.append(elem1.text)
                    if len(tempInner) == 15:
                        tempOuter3.append(tempInner)
            data1.append(tempOuter3) 
                    
            for i in range(2, row_count_table2 + 1): # team table 2 (Away)
                tempInner = []
                for x in range(1,col_count_table2):
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[4]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem2 = driver.find_element_by_xpath(path)
                    tempInner.append(elem2.text)
                    if len(tempInner) == 15:
                        tempOuter4.append(tempInner)
            data2.append(tempOuter4)

            for i in range (2, row_count_table1 + 1): # opponent table 1 (Home)
                tempInner = []
                for x in range(1, col_count_table1):
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem1 = driver.find_element_by_xpath(path)
                    tempInner.append(elem1.text)
                    if len(tempInner) == 15:
                        tempOuter1.append(tempInner)
            opp1.append(tempOuter1) 

            for i in range(2, row_count_table1 + 1): #opponent table 2 (Home)
                tempInner = []
                for x in range(1,col_count_table2): 
                    path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[2]/tbody/tr[{}]/td[{}]".format(i,x)
                    elem2 = driver.find_element_by_xpath(path)
                    tempInner.append(elem2.text)
                    if len(tempInner) == 15:
                        tempOuter2.append(tempInner)
            opp2.append(tempOuter2)   
            
    driver.quit() # Close driver once we get our data.

def toPanda1(data1, opp1, teamname):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    Converts first tabular dataset into a pandas dataframe and exports it. Does so for the Opponent dataset as well.
    The naming conventions are such that the 4 subsequent .csv files are for each game
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
    
    #create header lists for table headers
    headerlist1 = ["Player", "Min", "SST", "SST ex Pts", "Pts", "PPP", "Ast", "T/O", "Ast/TO", "Stl", "Stl Pos", "Blk", "Ttl Reb", "Off Reb", "Def Reb"]
    counter = 1

    for table in data1: 
        # Dynamically create names for each CSV export
        csv_name = teamname + "_" + str(counter) + "_Table1.csv"
        df = pd.DataFrame(table, columns = headerlist1)
        df['Min'] = df['Min'].str.split(":").str[0] # Convert minutes to alpha numeric
        df.replace('-', 0) # Convert -'s to 0's for aggregation
        df.to_csv(csv_name)
        counter = counter + 1
    
    # Reset counter for naming CSVs
    counter = 1 
    for table in opp1:
        csv_name = teamname + "_" + str(counter) + "_Opponent_Table1.csv"
        df = pd.DataFrame(table, columns = headerlist1)
        df['Min'] = df['Min'].str.split(":").str[0]
        df.replace('-', 0)
        df.to_csv(csv_name)
        counter = counter + 1
    
def toPanda2(data2, opp2, teamname):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    Converts second tabular dataset into a pandas dataframe and exports it. Does so for the Opponent dataset as well.
    The naming conventions are such that the 4 subsequent .csv files are for each game
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
    
    headerlist2 = ["Player", "FGA", "FGM", "FGm", "FG%", "aFG%", "2 FGA", "2 FGM", "2 FGm", "2 FG%", "3 FGA", "3 FGM", "3 FGm", "3FG%", "FTA", "FTM", "FTm", "FT%", "+1", "PF Tken", "PF Com"]
    counter = 1

    for table in data2:
        csv_name = teamname + "_" + str(counter) + "_Table2.csv"
        df = pd.DataFrame(table, columns = headerlist2)
        df.replace('-', 0)
        df.to_csv(csv_name)
        counter = counter + 1

    counter = 1
    for table in opp2:
        csv_name = teamname + "_" + str(counter) + "_Opponent_Table2.csv"
        df = pd.DataFrame(table, columns = headerlist2)
        df.replace('-', 0)
        df.to_csv(csv_name)
        counter = counter + 1

def store(teamname,dictionary):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    Runs teamData, toPanda1, and toPanda2 on each team in the NCAC, effectively gathering and storing
    all EBS data for every team.
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - '''
    d = dictionary[str(teamname)]

    teamData(teamname, d["Data1"], d["Data2"], d["Opp1"], d["Opp2"])
    toPanda1(d["Data1"], d["Opp1"], teamname)
    toPanda2(d["Data2"], d["Opp2"], teamname)   

def dictify(teamname):
    # names of the 4 different lists needed for each team
    names = ["Data1", "Data2", "Opp1", "Opp2"]

    d = {}
    for lst in names:
        d[lst] = []

    return d

def main():
    NCAC = ["Denison", "Witt", "Wooster", "OWU", "Hiram", "Wabash", "Depauw", "Oberlin", "Kenyon", "Allegheny"]  

    dictlist = []
    # Create list dictionaries for every NCAC team
    for team in NCAC:
        d_name = str(team) + "Dict"  # Name dictionaries by team
        d_name = dictify(team)
        dictlist.append(d_name)

    # Create dictionary storing all team dictionaries
    dict_dict = {}
    for i in range(len(NCAC)):
        dict_dict[NCAC[i]] = dictlist[i]

    # Collect data for every NCAC team 
    for team in NCAC:
        store(team,dict_dict)
        
if __name__ == "__main__":
    main()