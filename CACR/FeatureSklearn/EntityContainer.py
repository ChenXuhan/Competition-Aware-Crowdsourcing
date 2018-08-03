#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:ChenXuhan
from CACR.FeatureSklearn.BasicService import *
from CACR.DocPrepare.DocContainer import DocContainer
import pandas,pickle
from pandas import DataFrame


class QuestionContainer:

    def __init__(self):
        self.QuesId = []
        self.AcceptedAnswerId = []
        self.CreationDate = []
        self.Score = []
        self.ViewCount = []
        self.Body = []
        self.UserId = []
        self.ActiveDays = []
        self.ClosedDays = []
        self.Title = []
        self.AnswerCount = []
        self.CommentCount = []
        self.QuesTags = []
        self.tagMySQL = []

    def transformQuestions(self, quesList):
        for q in quesList:
            if not isinstance(q['OwnerUserId'],int) or q['OwnerUserId']<0:
                continue
            self.UserId.append(q['OwnerUserId'])
            self.QuesId.append(q['Id'])
            self.AcceptedAnswerId.append(q['AcceptedAnswerId'])
            createDate = count_day(q['CreationDate'])
            self.CreationDate.append(createDate)
            self.Score.append(q['Score'])
            self.ViewCount.append(q['ViewCount'])
            body = DocContainer.removeAnnotation(q['Body'])
            self.Body.append(body)
            self.ActiveDays.append(count_day(q['LastActivityDate'])-createDate)
            if len(q['ClosedDate'])>10:
                self.ClosedDays.append(count_day(q['ClosedDate'])-createDate)
            else:
                self.ClosedDays.append(-3)
            self.Title.append(q['Title'])
            self.AnswerCount.append(q['AnswerCount'])
            self.CommentCount.append(q['CommentCount'])
            tagList = str_to_list2(q['Tags'])
            self.addQuesTags(q['Id'], tagList)

    def addQuesTags(self, quesId, tagList):
        for tag in tagList:
            if tag in self.tagMySQL:
                self.QuesTags.append([quesId,self.tagMySQL.index(tag)])

    def exportQuestion(self):
        file = "../../data/Questions.data"
        data=[self.QuesId,self.CreationDate,self.Score,self.ViewCount,self.Body,\
            self.UserId,self.ActiveDays,self.ClosedDays,self.Title,self.AnswerCount,self.CommentCount]
        data = DataFrame(data, index=['QuesId','CreationDate','Score', 'ViewCount','Body',\
                               'UserId','ActiveDays','ClosedDays','Title','AnswerCount',\
                               'CommentCount'])
        data = data.T
        data.to_csv("../../data/Questions.csv")
        data.to_pickle(file)
        return data

    def exportQuesTags(self):
        print('There are %d records, %d questions.'%(len(self.QuesTags),len(set(self.QuesId))))
        file = "../../data/Ques-Tags"
        data = DataFrame(self.QuesTags, columns=['Question', 'Tag'])
        data['TagName'] = data['Tag'].map(lambda x: self.tagMySQL[x].lower())
        data.to_pickle(file+'.data')
        data = data.groupby(['Tag','TagName']).count().sort_values(by="Question",ascending=False)
        data.to_csv(file+'.csv')

    def getQuesByTags(self,TagName):
        file = "../../data/Ques-Tags.data"
        data = pandas.read_pickle(file)
        QuesId = data[data['TagName']==TagName]['Question']
        file = "../../data/Questions.data"
        questions = pandas.read_pickle(file).set_index('QuesId')
        sampleQues = questions.loc[list(QuesId)]
        return sampleQues

    def exportQuesAcceptedAns(self):
        file = "../../data/Ques-AcceptedAnswers"
        data = DataFrame([self.QuesId,self.UserId,self.AcceptedAnswerId], index=['Question','Questioner','AnswerId'])
        data = data.T
        data['Accepted'] = 1
        data.to_pickle(file+'.data')


class AnswerContainer:
    def __init__(self):
        self.UserId = {}
        self.CreationDate = {}
        self.Score = {}
        self.Comments = {}
        self.Posts = {}

    def transformAnswers(self, ansList):
        for answer in ansList:
            if not isinstance(answer['OwnerUserId'],int) or answer['OwnerUserId']<0: continue
            ansId = answer["Id"]
            self.UserId[ansId] = answer['OwnerUserId']
            createDate = count_day(answer['CreationDate'])
            self.CreationDate[ansId] = createDate
            self.Score[ansId] = answer['Score']
            self.Comments[ansId] = []
            self.Posts[ansId] = []


class CommentContainer:
    def __init__(self):
        self.UserId = {}
        self.CreationDate = {}
        self.Type = {}

    def transformComments(self, comList):
        for comment in comList:
            if not isinstance(comment['OwnerUserId'],int) or comment['UserId']<0:
                continue
            comId = comment["Id"]
            self.UserId[comId] = comment['UserId']
            createDate = count_day(comment['CreationDate'])
            self.CreationDate[comId] = createDate


class PostContainer:
    def __init__(self):
        self.UserId = {}
        self.CreationDate = {}

    def transformPosts(self, postList):
        for post in postList:
            if not isinstance(post['OwnerUserId'],int) or post['UserId']<0:
                continue
            postId = post["Id"]
            self.UserId[postId] = post['UserId']
            createDate = count_day(post['CreationDate'])
            self.CreationDate[postId] = createDate


class UserContainer:

    def __init__(self):
        self.questions = {}
        self.answers = {}
        self.comments = {}
        self.post = {}
        self.acAnswers = {}

    def getUsers(self):
        return self.questions.keys()

    def addActivity(self,userId,action,actionType):
        if action[0]<0: return
        if not userId in self.questions:
            self.questions[userId] = []
            self.answers[userId] = []
            self.comments[userId] = []
            self.post[userId] = []
            self.acAnswers[userId] = []
        if (actionType == 1):
            self.questions[userId].append(action)
            return
        if (actionType == 2):
            self.answers[userId].append(action)
            return
        if (actionType == 3):
            self.comments[userId].append(action)
            return
        if (actionType == 4):
            self.post[userId].append(action)
            return
        if (actionType == 5):
            self.acAnswers[userId].append(action)
            return

    def exportUserActivity(self, tagName):
        file = "../../data/UserActivity_%s.data" % tagName
        with open(file,"wb")as f:
             pickle.dump(self, f)

    def utility(self):
        data = []
        for userId in self.questions.keys():
            data.append([userId,len(self.questions[userId]),len(self.answers[userId]),len(self.comments[userId]),\
                            len(self.post[userId]),len(self.acAnswers[userId])])
        file = "../../data/UserData.csv"
        data = DataFrame(data,columns=['UserId','Questions','Answers','Comments','Posts','AcAnswers'])
        data.to_csv(file)
