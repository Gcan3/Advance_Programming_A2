#Importing useful modules
from tkinter import *
import tkinter.messagebox
import requests

#tkinter window adjustment and configuration
window = Tk()
window.title("NBA Game Day")
#Making fixed size
window.minsize(width=1000, height=600)
window.maxsize(width=1000, height=600)
window.config(bg='#8D918D')

#Setting up the global variables to be accessed by the function and tkinter
team_name = StringVar()
yearVar = IntVar()
monthVar = IntVar()
dayVar = IntVar()
APIKEY = '40130162'
format_month = ''
format_day = ''
format_team = ''

#==============================================FUNCTION/API PROCESSING================================================
def analyze():
    #Setting the first batch of variables which gets the data from the entry widgets
    entered_team = team_name.get()
    format_year = yearVar.get()
    entered_month = monthVar.get()
    entered_day = dayVar.get()
    
    #Verifying if the dates are appropriate and within of the given range
    if entered_month < 1 or entered_month > 12 or entered_day < 1 or entered_day > 31 or format_year < 2000 or format_year > 2023:
        #otherwise, show a message box of invalidity
        tkinter.messagebox.showinfo("Invalid Date","Month, Day, or Year Input is invalid, try again.")
        
    #When all the dates are correct, reformat the month and day to tenth place if they are given in single digits
    #.title() the entered team name to properly access the api data
    format_month = f'{entered_month:02}'
    format_day = f'{entered_day:02}'
    format_team = f'{entered_team.title()}'
    
    #After reformatting the months and days, they are conjoined in a string pattern
    date = f'{format_year}-{format_month}-{format_day}'
    #Make the date on the display the same as the string pattern
    date_happen.configure(text=f'{format_day}/{format_month}/{format_year}', bg='gray', fg='white')

    #Request for two API's, with one needing an api key and a date(which is the conjoined string pattern)
    source = requests.get(f'https://www.thesportsdb.com/api/v1/json/{APIKEY}/eventsday.php?d={date}&l=4387')
    team_dict = requests.get(f'https://www.thesportsdb.com/api/v1/json/2/search_all_teams.php?l=NBA')

    #Set the number of games variable to default 0
    gameLength = 0
    
    #Search through the data if there was any games during the given date
    if source.json()['events'] == None:
        #Display a notice if the data gives null
        tkinter.messagebox.showinfo("No games", "There were no games during that date.")
    else:
        #Set the length of events in the data. In other words, the number of games happened are stored inside the variable
        gameLength = len(source.json()['events'])
    
    #Setting the second variables which are set to empty
    trueGame = []
    home_team = ''
    visit_team = ''
    getHomeShort = ''
    getVisitShort = ''
    homeScore = 0
    visitScore = 0
    
    #Check all games of the date for involved team
    for games in range(gameLength):
        #If gates to see if the entered team is either playing for home team or away team
        #If any of them happens to BE there, append that index of the game to their respective empty list
        #For debug purposes, printing true or false
        if format_team == source.json()['events'] [games] ['strHomeTeam'] or format_team == source.json()['events'] [games] ['strAwayTeam']:
            # print("True")
            trueGame.append(games)
        # else:
        #     print("false")

    #Collect the data of that specific event and store them in the respective variables
    if len(trueGame) > 0:
        home_team = source.json() ['events'] [trueGame[0]] ['strHomeTeam']
        visit_team = source.json() ['events'] [trueGame[0]] ['strAwayTeam']
        homeScore = int(source.json() ['events'] [trueGame[0]] ['intHomeScore'])
        visitScore = int(source.json() ['events'] [trueGame[0]] ['intAwayScore'])
    #If the lists are all empty, it means no games were found during the search and returned nothing
    else:
        #Display the notice to the user
        tkinter.messagebox.showinfo("Invalid Team", "The entered team did not play or does not exist. Try changing the date or team name.")
        #Along with this, clear the configured text that may have been displayed earlier
        home_Name.delete("1.0","end")
        home_finalScore.delete("1.0","end")
        visit_Name.delete("1.0","end")
        visit_finalScore.delete("1.0","end")
        homeShort.delete("1.0","end")
        awayShort.delete("1.0","end")
    
    #Display the collected data to tkinter through configuration
    home_Name.config(text=home_team)
    visit_Name.config(text=visit_team)
    home_finalScore.config(text=homeScore)
    visit_finalScore.config(text=visitScore)
    
    #Finding the abbreviation for the playing teams
    #Find the length of teams in the second api
    team_length = len(team_dict.json() ['teams'])
    #Search through the team index for the playing teams
    for team in range(team_length):
        #If it found the home team's name, store the team's abbreviation to the empty variable
        if home_team == team_dict.json() ['teams'] [team] ['strTeam']:
            getHomeShort = team_dict.json() ['teams'] [team] ['strTeamShort']
        #If it found the visiting team's name, store the team's abbreviation to the empty variable
        elif visit_team == team_dict.json() ['teams'] [team] ['strTeam']:
            getVisitShort = team_dict.json() ['teams'] [team] ['strTeamShort']
        #continue the loop if the team did not match to any of the playing teams
        else:
            continue
    
    #Display the data-given team abbreviations
    homeShort.config(text=getHomeShort)
    awayShort.config(text=getVisitShort)
    
    #If gates to show which team won during that match
    #Configure the losing team's background color to white while the winning team gets a light green background
    #Display the name of the winning team
    if homeScore > visitScore:
        visit_finalScore.config(bg='white')
        home_finalScore.config(bg='#9CEA99')
        who_wins.config(text=home_team)
    else:
        home_finalScore.config(bg='white')
        visit_finalScore.config(bg='#9CEA99')
        who_wins.config(text=visit_team)
    
    #Getting the quarter scores of that game
    quarter_scores = source.json() ['events'] [trueGame[0]] ['strResult']
    #Replace the html breaks with spaces
    q_Score = quarter_scores.replace('<br>', ' ')
    #Split the data into two (this is because there is two spaces separating the two teams)
    split_score = q_Score.split('  ')
    #Replace the "Quarters" string into colons for both of the teams
    final_score_display = [x.replace(' Quarters:', ':') for x in split_score]
    #Configure them to the window
    home_team_qts.config(text=final_score_display[0])
    away_team_qts.config(text=final_score_display[1])
        
#==============================================GUI DISPLAY================================================
heading = Label(window,
                text= "Welcome! See if the NBA team played that date!",
                fg="black",
                bg="white",
                font=('Times New Roman', 26, 'bold'))
#Making a container using Label widget without any text
box = Label(bg='white',
            width=83,
            height=32)

homeLabel = Label(window,
                  text='Hosting/Home',
                  bg='black',
                  fg='white',
                  font=('Times New Roman', 19))
visitingLabel = Label(window,
                  text='Visiting/Away',
                  bg='black',
                  fg='white',
                  font=('Times New Roman', 19))
versus = Label(window,
               text='vs',
               fg='black',
               bg='white',
               font=('Times New Roman', 23))
#These text labels have no text so that they can be configured during the function but has set display adjustments
homeShort = Label(window, bg='white', font=('Courier', 40))
awayShort = Label(window, bg='white', font=('Courier', 40))
home_Name = Label(window, bg='white', font=('Courier', 13, 'bold'))
visit_Name = Label(window, bg='white', font=('Courier', 13, 'bold'))
home_finalScore = Label(window, bg='white', font=('Courier', 18, 'bold'))
visit_finalScore = Label(window, bg='white', font=('Courier', 18, 'bold'))
winner_label = Label(window, bg='white', text='Winner:', font=('Helvetica', 23))
who_wins = Label(window, bg='white', font=('Helvetica', 20, 'italic'))
date_happen = Label(window, bg='white', font=('Times New Roman', 15))
home_team_qts = Label(window, bg='white', font=('Courier', 12))
away_team_qts = Label(window, bg='white', font=('Courier', 12))

#==============================================GUI ENTRY POINT/GUIDE================================================
guide = Label(window, text= 'Enter the NBA team:', fg='black', bg='white', font=('Times New Roman', 15))
team_entry = Entry(window, width=25, bd=5, font=('Times New Roman', 16), textvariable= team_name)
year_Entry = Entry(window, width=5, bd=2, font=('Times New Roman', 16), textvariable= yearVar)
month_Entry = Entry(window, width=5, bd=2, font=('Times New Roman', 16), textvariable= monthVar)
day_Entry = Entry(window, width=5, bd=2, font=('Times New Roman', 16), textvariable= dayVar)
date_guide = Label(window, text= 'Enter the appropriate date:', fg='black', bg='white', font=('Times New Roman', 15))
year_guide = Label(window, text= 'Year (2000-2023)', fg='black', bg='white', font=('Times New Roman', 10, 'italic'))
month_guide = Label(window, text= 'Month (1-12)', fg='black', bg='white', font=('Times New Roman', 10, 'italic'))
day_guide = Label(window, text= 'Day (1-31)', fg='black', bg='white', font=('Times New Roman', 10, 'italic'))
processBtn = Button(window, text='Analyze', width=35, height=1, bg='gray', bd=10, command= analyze)

#==============================================WIDGET PLACEMENT================================================
versus.place(x=670, y=220)
homeLabel.place(x=450, y=130)
visitingLabel.place(x=775, y=130)
box.place(x=400, y=80)
heading.place(x=150,y=20)
guide.place(x=110, y=150)
team_entry.place(x=60, y=200)
year_Entry.place(x=50, y=350)
month_Entry.place(x=175, y=350)
day_Entry.place(x=300,y=350)
processBtn.place(x=70,y=500)
date_guide.place(x=90, y=300)
year_guide.place(x=27, y=390)
month_guide.place(x=170, y=390)
day_guide.place(x=300, y=390)
homeShort.place(x=465, y=200)
awayShort.place(x=795, y=200)
home_Name.place(x=450, y=275)
visit_Name.pack(padx=(700, 0), pady=275)
home_finalScore.place(x=500, y=310)
visit_finalScore.place(x=820, y=310)
winner_label.place(x=470, y=480)
who_wins.place(x=590, y=481)
date_happen.place(x=645, y=130)
home_team_qts.place(x=510, y=380)
away_team_qts.place(x=510, y=425)

#Running the window using .mainloop()
window.mainloop()