"""
BasketballAnalytics.py

Josh Blaz
Denison University -- 2019
blaz_j1@denison.edu

NOTE: User must enter SST credentials below @ lines 79 & 80.
"""
# *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
# Imports allowing the use of Selenium and Geckodriver. 
from lxml import html
from selenium import webdriver
# Allow us to send keys through the Webdriver.
from selenium.webdriver.common.keys import Keys 
# Allow us to wait for certain elements to load in. Gives us much more control over the Webdriver.
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Imported to use simple sleep function. (used rarely)
import time 
# Import pandas allowing us to export Lists of Lists to excel files.
import pandas as pd
# *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***

def dropdown(team):
    ''' - - - - - - - - - - - - - - - - - - - - - - - - 
    Determines the input team's dropdown search string. In this case, we're only going to be searching for NCAC teams. 
    '''
    if team == "Denison":
        return "Denison (OH) Big Red"
    elif team == "Wittenberg":
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
    
    # *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
    # NOTE: USER: Insert Sports Synergy Tech Credentials below
    
    elem1 = driver.find_element_by_name("txtUserName")
    elem2 = driver.find_element_by_name("txtPassword")

    # Clear previous inputs
    elem1.clear() 
    elem2.clear()

    elem1.send_keys("") # Insert Email inside of quotes
    elem2.send_keys("")  # Insert Password inside of quotes
    
    elem2.send_keys(Keys.RETURN) # Presses "Enter" Key, submitting the credentials to SST
    # *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
    # Extended Box Score (EBS) Collections

    # WebDriverWait allows us to wait until a certain condition is met. In this case we're waiting for the "Game" button.
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/div[2]/center/div[2]/div[2]/table[3]/tbody/tr[2]/td/center/a/font/b')))
    gameButton = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/div[2]/center/div[2]/div[2]/table[3]/tbody/tr[2]/td/center/a/font/b')
    gameButton.click()

    # Uses the 'dropdown' function in order to find the correct 'dropdown string' for the team on the SST site.
    # This string is then entered into the textbox at 'dropdownpath'.
    DDstring = dropdown(team)
    dropdownpath = '//*[@id="ctl00_MainContent_lstTeamA"]/option[text()="{}"]'.format(DDstring)
    elem = driver.find_element_by_xpath(dropdownpath).click()
    time.sleep(3)

    # row_count is the number of games the current team played this season. 
    row_count = len(driver.find_elements_by_xpath("//table[2]/tbody/tr"))
    
    # We iterate through the table containing every game for the current team in this season, and select (click) each one.
    for i in range(2, row_count + 1):
        path = "/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/table[2]/tbody/tr[{}]/td[2]/a".format(i)
        wait.until(EC.presence_of_element_located((By.XPATH, path)))
        elem = driver.find_element_by_xpath(path).click()

    driver.switch_to.default_content()
    # Now we have a tab open for each game played in the season, each tab has the EBS we want to scrape.
    for i in range(1, len(driver.window_handles)): # Skip the first tab (the list of games)
        driver.switch_to.window(driver.window_handles[i])
        wait = WebDriverWait(driver, 30) # Cannot proceed until we find this element
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr[1]/td[1]')))
        hometeam = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr[1]/td[1]')

        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr[1]/td[1]')))
        awayteam = driver.find_element_by_xpath('/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr[1]/td[1]')

        row_count_table1 = len(driver.find_elements_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[1]/tbody/tr"))
        row_count_table2 = len(driver.find_elements_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/div/span/nobr/div/table[3]/tbody/tr"))
        
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
        csv_name = teamname + "_" + str(counter) + "_Table1.csv"
        df = pd.DataFrame(table, columns = headerlist1)
        df['Min'] = df['Min'].str.split(":").str[0] #Convert minutes to alpha numeric
        df.replace('-', 0)
        print(df['Min'])
        df.to_csv(csv_name)
        counter = counter + 1
    
    counter = 1 # reset counter
    for table in opp1:
        csv_name = teamname + "_" + str(counter) + "_Opponent_Table1.csv"
        df = pd.DataFrame(table, columns = headerlist1)
        df['Min'] = df['Min'].str.split(":").str[0]
        df.replace('-', 0)
        print(df['Min'])
        df.to_csv(csv_name)
        counter = counter + 1
    
def toPanda2(data2, o, teamname):
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

def main():
    # Initialize NCAC team datasets globally, will eventually be converted to Pandas, then exported as CSVs.
    DenisonData1 = [] #Denison tables 1 and 2
    DenisonData2 = []
    DenisonOpp1 = [] #Denison opponent tables 1 and 2
    DenisonOpp2 = []

    WittData1 = []
    WittData2 = []
    WittOpp1 = []
    WittOpp2 = []

    WoosterData1 = []
    WoosterData2 = []
    WoosterOpp1 = []
    WoosterOpp2 = []

    OWUData1 = []
    OWUData2 = []
    OWUOpp1 = []
    OWUOpp2 = []

    HiramData1 = []
    HiramData2 = []
    HiramOpp1 = []
    HiramOpp2 = []

    WabashData1 = []
    WabashData2 = []
    WabashOpp1 = []
    WabashOpp2 = []

    DepauwData1 = []
    DepauwData2 = []
    DepauwOpp1 = []
    DepauwOpp2 = []

    OberlinData1 = []
    OberlinData2 = []
    OberlinOpp1 = []
    OberlinOpp2 = []

    KenyonData1 = []
    KenyonData2 = []
    KenyonOpp1 = []
    KenyonOpp2 = []
    
    AlleghenyData1 = []
    AlleghenyData2 = []
    AlleghenyOpp1 = []
    AlleghenyOpp2 =

    # Collect data for every NCAC team
    NCAC = ["Denison", "Wittenberg", "Wooster", "OWU", "Hiram", "Wabash", "Depauw", "Oberlin", "Kenyon", "Allegheny"]   
    for team in NCAC:
        if team == "Denison":
            teamData(team, DenisonData1, DenisonData2, DenisonOpp1, DenisonOpp2)
            toPanda1(DenisonData1, DenisonOpp1, "Denison")
            toPanda2(DenisonData2, DenisonOpp2, "Denison")
        elif team == "Wittenberg":
            teamData(team, WittData1, WittData2, WittOpp1, WittOpp2)
            toPanda1(WittData1, WittOpp1, "Wittenberg")
            toPanda2(WittData2, WittOpp2, "Wittenberg")
        elif team == "Wooster":
            teamData(team, WoosterData1, WoosterData2, WoosterOpp1, WoosterOpp2)
            toPanda1(WoosterData1, WoosterOpp1, "Wooster")
            toPanda2(WoosterData2, WoosterOpp2, "Wooster")
        elif team == "OWU":
            teamData(team, OWUData1, OWUData2, OWUOpp1, OWUOpp2)
            toPanda1(OWUData1, OWUOpp1, "OWU")
            toPanda2(OWUData2, OWUOpp2, "OWU")
        elif team == "Hiram":
            teamData(team, HiramData1, HiramData2, HiramOpp1, HiramOpp2)
            toPanda1(HiramData1, HiramOpp1, "Hiram")
            toPanda2(HiramData2, HiramOpp2, "Hiram")
        elif team == "Wabash":
            teamData(team, WabashData1, WabashData2, WabashOpp1, WabashOpp2)
            toPanda1(WabashData1, WabashOpp1, "Wabash")
            toPanda2(WabashData2, WabashOpp2, "Wabash")
        elif team == "Depauw":
            teamData(team, DepauwData1, DepauwData2, DepauwOpp1, DepauwOpp2)
            toPanda1(DepauwData1, DepauwOpp1, "Depauw")
            toPanda2(DepauwData2, DepauwOpp2, "Depauw")
        elif team == "Oberlin":
            teamData(team, OberlinData1, OberlinData2, OberlinOpp1, OberlinOpp2)
            toPanda1(OberlinData1, OberlinOpp1, "Oberlin")
            toPanda2(OberlinData2, OberlinOpp2, "Oberlin")
        elif team == "Kenyon":
            teamData(team, KenyonData1, KenyonData2, KenyonOpp1, KenyonOpp2)
            toPanda1(KenyonData1, KenyonOpp1, "Kenyon")
            toPanda2(KenyonData2, KenyonOpp2, "Kenyon")
        if team == "Allegheny":
            teamData(team, AlleghenyData1, AlleghenyData2, AlleghenyOpp1, AlleghenyOpp2)
            toPanda1(AlleghenyData1, AlleghenyOpp1, "Allegheny")
            toPanda2(AlleghenyData2, AlleghenyOpp2, "Allegheny")
            
if __name__ == "__main__":
    main()