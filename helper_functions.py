import numpy as np
import scipy.io
import matplotlib.pyplot as plt
from random import *
from pathlib import Path

def load_data2():

################
#Extractin the session 1, young subjects data from PEERS

#Download entire PEERS dataset from: http://memory.psych.upenn.edu/Data_Archive

############

    # PARAMETERS
    # data directory
    files_dir = '/Users/qiongz/Downloads/'

    # select subjects
    all_subjects = range(63,301)
    subject_dir = files_dir + 'PEERS.data/PEERS_older_adult_subject_list.txt'
    with open(subject_dir) as f:
        content = f.readlines()
        content = [x.split() for x in content]
    subjects_old = [int(x[0]) for x in content]
    subjects_young = [x for x in all_subjects if x not in subjects_old]

    # options: 1. all_subjects 2. subjects_old 3. subjects_young
    subjects = subjects_young

    # other parameters
    LL = 16

    # DATA
    recalls_sp = []
    recalls = []
    presents = []
    presented_words = []
    recalled_words = []
    sessionlengths = []
    listlengths = []
    subjs = []
    subjs_list = [] # re-numbered subjects starting from zero - consistent with 'subjs'
    for s, subj in enumerate(subjects):
        subjs_list.append(s)
        #sessionlength = []
        listlength = []
        length = 0
        for session in [1,2,3,4,5,6]: # excluding the first section which is a practice section
            # Specify data file directory - 3 digits for each subj ID
            if len(str(subj))<3:
                parent_dir = files_dir + 'PEERS.data/LTP0' + str(subj) + '/session_' + str(session)
            else:
                parent_dir = files_dir + 'PEERS.data/LTP' + str(subj) + '/session_' + str(session)
            data_dir1 = parent_dir + '/session.log'
            data_dir2 = parent_dir + '/ffr.par'
            my_file1 = Path(data_dir1)
            my_file2 = Path(data_dir2)


            # Load presentation details
            if my_file1.is_file():
                data_dir1 = parent_dir + '/session.log'
                with open(data_dir1) as f:
                    content = f.readlines()
                    content = [x.split() for x in content]
                pre_list = 0
                position = 0
                dics= []
                presented = []
                present = []
                for i in range(len(content)):
                    if content[i][2] == 'FR_PRES': # record only stimuli in the encoding stage
                        current_list = int(content[i][3])
                        item = int(content[i][5])
                        word = content[i][4]
                        presented.append(word)
                        dics.append([item,current_list,position]) # create dictionary of word ID, list number, serial position
                        if current_list != pre_list:
                            position = 0
                            presented_words.append(presented)
                            presents.append(present)
                            presented = []
                            present = []
                        present.append([subj,session,item,current_list,position,word]) #subj, session, item ID, list number, serial position, word
                        pre_list = current_list
                        position = position + 1
                presented_words.append(presented)
                presents.append(present)

                data_dir = parent_dir + '/15.par'
                my_file = Path(data_dir)
                if position == LL and my_file.is_file(): # two kinds of trials (3 or 16 items during encoding), only take trials with 16 items encoded; only take sessions with 16 lists
                    listlength.append(position)

                    # IMMEDIATE FREE RECALL
                    for listno in range(16): # every selected session has 16 lists
                        data_dir3 = parent_dir + '/' + str(listno)+ '.par'
                        my_file3 = Path(data_dir3)
                        if my_file3.is_file():
                            length = length + 1
                            recall = []
                            recall_sp = []
                            subjs.append(s)

                            with open(data_dir3) as f:
                                content = f.readlines()
                                content = [x.split() for x in content]
                            lasttime = 0
                            words = []
                            for i in range(len(content)):
                                item = int(content[i][1])
                                word = content[i][2]
                                temp = [x for x in dics if x[0]== item]
                                currenttime = int(content[i][0])
                                RT = (currenttime - lasttime)/1000
                                lasttime = currenttime
                                #words.append(word)
                                if len(temp)>0:
                                    recall_sp.append(temp[0][2])
                                    words.append(word)
                                    recall.append([subj,session,item,temp[0][1],temp[0][2],word]) #subj, session, item ID, list number, serial position, word
                                else:
                                    recall_sp.append(-1)
                                    recall.append([subj,session,item,-1,-1,word]) #subj, session, item ID, list number, serial position, word

                            recalled_words.append(words)
                            recalls.append(recall)
                            recalls_sp.append(recall_sp)
        listlengths.append(listlength)
        sessionlengths.append(length)
    return recalls, recalls_sp, listlengths, sessionlengths, subjects, subjs, presented_words, recalled_words, presents
