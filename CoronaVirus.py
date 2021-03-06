############################################################
#Hello all, I'm Daniel Berrones and as you can see, I 
#forked this brilliant repo that Dr. Sarkar put together
#using COVID-19 data offered by the New York Times.  
############################################################

#TODO: Build GUI framework to conceptualize data more easily using TKinter

############################################################
#Email [daniel.a.berrones@gmail.com]
#Website [http://www.danielberrones.com]
############################################################
# from itertools import product

import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tkinter as tk
from datetime import datetime, date
from io import StringIO
from time import time, sleep

class CoronaVirus:
    def __init__(self):
        self.statedf = None
        self.countydf = None
        self._stateupdated = False
        self._countyupdated = False
        self._processed = False
        self._today = datetime.today()
    
    def today(self):
        'Prints today\'s date'
        print("",self._today.strftime("%B %d, %Y").center(50,"-"))

    def updateState(self):
        url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv"
        s=requests.get(url).content
        self.statedf = pd.read_csv(StringIO(s.decode('utf-8')))
        self.statedf['date'] =  pd.to_datetime(self.statedf['date'], format='%Y-%m-%d')
        self._stateupdated = True
    
    def process(self):
        pd.set_option('mode.chained_assignment', None)
        self.statedict= {}
        self.countydict= {}
        print("Processing...")
        t1 = time()
        if self._stateupdated:
            self.statelist = list(self.statedf['state'].unique())
            for s in self.statelist:
                state_df=self.statedf[self.statedf['state']==s]
                state_df['newcases'] = state_df['cases'].diff()
                state_df['newdeaths'] = state_df['deaths'].diff()
                self.statedict[s]=state_df
        if self._countyupdated:
            self.countylist = list(self.countydf['county'].unique())
            for c in self.countylist:
                county_df=self.countydf[self.countydf['county']==c]
                county_df['newcases'] = county_df['cases'].diff()
                county_df['newdeaths'] = county_df['deaths'].diff()
                self.countydict[c]=county_df
        self._processed = True
        t2 = time()
        delt = round(t2-t1,3)
        print("Finished. Took {} seconds".format(delt))
    
    def plot_state(self, state='New York', last_30_days=False):
        'Plots statewise data'
        if self._processed==False:
            print("Data not processed. Cannot plot statewise.")
        
        s = str(state)
        assert s in self.statelist,"Input does not appear in list of states. Possibly wrong name/spelling"
        df = self.statedict[s]
        
        dates = df['date']
        cases = df['cases']
        deaths = df['deaths']
        newcases = df['newcases']
        newdeaths = df['newdeaths']
        
        if last_30_days:
            dates = df['date'][-31:-1]
            cases = df['cases'][-31:-1]
            deaths = df['deaths'][-31:-1]
            newcases = df['newcases'][-31:-1]
            newdeaths = df['newdeaths'][-31:-1]

        #########################
        print("CUMULATIVE CASES")
        plt.figure(figsize=(14,4))
        if last_30_days:
            plt.title("Cumulative cases in {}, for last 30 days".format(s),fontsize=18)
        else:
            plt.title("Cumulative cases in {}".format(s),fontsize=18)
        plt.bar(x=dates,height=cases,color='blue',edgecolor='k')
        plt.xticks(rotation=15,fontsize=16)
        plt.show()

        #########################
        print("CUMULATIVE DEATHS")
        plt.figure(figsize=(14,4))
        if last_30_days:
            plt.title("Cumulative deaths in {}, for last 30 days".format(s),fontsize=18)
        else:
            plt.title("Cumulative deaths in {}".format(s),fontsize=18)
        plt.bar(x=dates,height=deaths,color='red',edgecolor='k')
        plt.xticks(rotation=15,fontsize=17)
        plt.show()

        #########################
        print("NEW CASES")
        plt.figure(figsize=(14,4))
        if last_30_days:
            plt.title("New cases in {}, for last 30 days".format(s),fontsize=18)
        else:
            plt.title("New cases in {}".format(s),fontsize=18)
        plt.bar(x=dates,height=newcases,color='yellow',edgecolor='k')
        plt.xticks(rotation=15,fontsize=17)
        plt.show()

        #########################
        print("NEW DEATHS") 
        plt.figure(figsize=(14,4))
        if last_30_days:
            plt.title("New deaths in {}, for last 30 days".format(s),fontsize=18)
        else:
            plt.title("New deaths in {}".format(s),fontsize=18)
        plt.bar(x=dates,height=newdeaths,color='orange',edgecolor='k')
        plt.xticks(rotation=15,fontsize=17)
        plt.show() 
        
    def plot_multi_state(self, 
                         states = ['New York','Illinois','Kentucky'],
                         last_30_days=False):
        """
        Plots multiple states data in a single plot for comparison
        """
        states = states
        plt.figure(figsize=(14,4))
        if last_30_days:
            plt.title("Cumulative cases, for last 30 days",fontsize=18)
            colors=[]
            for s in states:
                color = tuple(np.round(np.random.random(3),2))
                colors.append(color)
                plt.plot(self.statedict[s]['date'][-31:-1],
                        self.statedict[s]['cases'][-31:-1],
                        color=color,
                        linewidth=2)
                plt.xticks(rotation=15,fontsize=17)
            plt.legend(states,fontsize=14)
            plt.show()
        else:
            plt.title("Cumulative cases",fontsize=18)
            colors=[]
            for s in states:
                color = tuple(np.round(np.random.random(3),2))
                colors.append(color)
                plt.plot(self.statedict[s]['date'],
                        self.statedict[s]['cases'],
                        color=color,
                        linewidth=2)
                plt.xticks(rotation=15,fontsize=17)
            plt.legend(states,fontsize=14)
            plt.show()
    
    def rankState(self, N=5, daterank=None):
        """
        Ranks the states in a bar chart
        Arguments:
            N: Top N states to be ranked
            date: Date at which the ranking is done. 
                  Must be a string in the form '2020-3-27'
        """

        cases = {}
        deaths = {}
        newcases = {}
        newdeaths = {}

        if daterank==None:
            d = self.statedf.iloc[-1]['date'].date()
        else:
            d = datetime.strptime(daterank,'%Y-%m-%d').date()

        for s in self.statedict:
            df=self.statedict[s]
            for i in range(len(df)):
                if df['date'].iloc[i].date()==d:
                    cases[s]=df.iloc[i]['cases']
                    deaths[s]=df.iloc[i]['deaths']
                    newcases[s]=df.iloc[i]['newcases']
                    newdeaths[s]=df.iloc[i]['newdeaths']

        sorted_cases = sorted(((value, key) for (key,value) in cases.items()),reverse=True)
        sorted_cases = sorted_cases[:N]

        sorted_deaths = sorted(((value, key) for (key,value) in deaths.items()),reverse=True)
        sorted_deaths = sorted_deaths[:N]

        sorted_newcases = sorted(((value, key) for (key,value) in newcases.items()),reverse=True)
        sorted_newcases = sorted_newcases[:N]

        sorted_newdeaths = sorted(((value, key) for (key,value) in newdeaths.items()),reverse=True)
        sorted_newdeaths = sorted_newdeaths[:N]

        _,axs = plt.subplots(2,2,figsize=(15,9))
        axs = axs.ravel()
        #0#########################
        axs[0].bar(x=[val[1] for val in sorted_cases], height=[val[0] for val in sorted_cases], color='blue',edgecolor='k')
        axs[0].set_title("Cumulative cases on {}".format(str(d)), fontsize=15)
        #1#########################
        axs[1].bar(x=[val[1] for val in sorted_deaths],height=[val[0] for val in sorted_deaths],color='red',edgecolor='k')
        axs[1].set_title("Cumulative deaths on {}".format(str(d)),fontsize=15)
        #2#########################
        axs[2].bar(x=[val[1] for val in sorted_newcases],height=[val[0] for val in sorted_newcases],color='yellow',edgecolor='k')
        axs[2].set_title("New cases on {}".format(str(d)),fontsize=15)
        #3#########################
        axs[3].bar(x=[val[1] for val in sorted_newdeaths],height=[val[0] for val in sorted_newdeaths],color='orange',edgecolor='k')
        axs[3].set_title("New deaths on {}".format(str(d)),fontsize=15)
        plt.show()

def printIntro():
    print("".center(50,"*"))
    print("Welcome to the COVID-19 Data Analytics Center")
    print("".center(50,"*"))
    sleep(2)
    CoronaVirus().today()
    return None

def main():
    corona=CoronaVirus()
    printIntro()
    print("Updating State database...")
    corona.updateState()
    corona.process()
    #corona.plot_state(state='Illinois',last_30_days=True)
    #corona.plot_state(state='Kentucky',last_30_days=True)
    #corona.plot_state(state='Texas',last_30_days=True)
    #corona.plot_state(state='Arizona',last_30_days=True)
    #corona.plot_state(state='California',last_30_days=True)
    #corona.plot_state(state='Florida',last_30_days=True)
    #corona.plot_multi_state(states=['Texas','New York','Florida','Illinois','Kentucky','Arizona','California'],last_30_days=False)
    corona.plot_multi_state(states=['Texas','Florida','Illinois','Kentucky','Arizona','California'],last_30_days=False)
    #corona.rankState()


main()
