#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:ChenXuhan
from CACR.FeatureSklearn.ConnectDB import connectDB,executeSQL
from CACR.FeatureSklearn.EntityContainer import QuestionContainer,AnswerContainer,UserContainer
from CACR.FeatureSklearn.BasicService import printArray,count_day
maxInteger = 32768


def initData():
    sample = ''
    try:
        users = UserContainer()

        con = connectDB()
        sqlstr = 'select Id,AcceptedAnswerId,CreationDate,Score,ViewCount,Body,OwnerUserId,LastActivityDate,' \
                 'ClosedDate,Title,AnswerCount,CommentCount,Tags from questions%s;'%(sample)
        quesMysql = executeSQL(con,sqlstr)
        questions = QuestionContainer()

        sql = "select TagName from tags;"
        tagList = executeSQL(con, sql)
        questions.tagMySQL = [tag['TagName'] for tag in tagList]
        questions.transformQuestions(quesMysql)
        questions.exportQuestion()
        questions.exportQuesTags()
        questions.exportQuesAcceptedAns()
        # 添加用户提问和回答采用记录
        for index in range(len(questions.QuesId)):
            users.addActivity(questions.UserId[index],[questions.QuesId[index], questions.CreationDate[index]],1)

    except Exception as e:
        print(e.args)
    finally:
        if con:
            con.close()
            # print("connection for select questions closed.")


def sampleData(tagName):
    try:
        sample = ""
        questionDf = QuestionContainer().getQuesByTags(tagName)
        quesStr = printArray(questionDf.index)
        users = UserContainer()
        con = connectDB()

        sqlstr = "select Id,ParentId,CreationDate,OwnerUserId,Score from answers%s where ParentId in %s;" % (sample, quesStr)
        # print(sqlstr)
        ansMysql = executeSQL(con,sqlstr)
        answers = AnswerContainer()
        answers.transformAnswers(ansMysql)
        # 添加用户回答记录
        for ansId in answers.UserId.keys():
            users.addActivity(answers.UserId[ansId],[ansId,answers.CreationDate[ansId]],2)
        # for userId in users.answers.keys():
        #     print(userId,",answer:",users.answers[userId])

        # 添加用户comment记录
        ansStr = printArray(answers.UserId.keys())
        sqlstr = "select Id,PostId,CreationDate,UserId from comments%s where PostId in %s;" % (sample, quesStr)
        comMysql = executeSQL(con, sqlstr)
        for comment in comMysql:
            if not isinstance(comment["UserId"], int) or (comment["UserId"])<0: continue
            users.addActivity(comment["UserId"], [comment['Id'], count_day(comment["CreationDate"]), 0], 3)
        sqlstr = 'select Id,PostId,CreationDate,UserId from comments%s where PostId in '%(sample) + ansStr + ";"
        comMysql = executeSQL(con, sqlstr)
        for comment in comMysql:
            if not isinstance(comment["UserId"], int) or (comment["UserId"])<0: continue
            users.addActivity(comment["UserId"], [comment['Id'], count_day(comment["CreationDate"]), 1], 3)

        # for userId in users.comments.keys():
        #     print(userId,",comments:",users.comments[userId])

        # 添加用户post记录
        sqlstr = 'select Id,PostId,CreationDate,UserId from posthistory%s where PostId in '%(sample) + quesStr + ";"
        postMysql = executeSQL(con, sqlstr)
        for post in postMysql:
            if not isinstance(post["UserId"], int) or (post["UserId"])<0: continue
            users.addActivity(post["UserId"], [post['Id'], count_day(post["CreationDate"]), 0], 4)
        sqlstr = 'select Id,PostId,CreationDate,UserId from posthistory%s where PostId in '%(sample) + ansStr + ";"
        postMysql = executeSQL(con, sqlstr)
        for post in postMysql:
            if not isinstance(post["UserId"], int) or (post["UserId"])<0: continue
            users.addActivity(post["UserId"], [post['Id'], count_day(post["CreationDate"]), 1], 4)

        # for userId in users.post.keys():
        #     print(userId,",post:",users.post[userId])

        users.exportUserActivity(tagName)
        users.utility()

    except Exception as e:
        print(e.args)
    finally:
        if con:
            con.close()
            # print("connection for select questions closed.")

initData()
sampleData("c")
