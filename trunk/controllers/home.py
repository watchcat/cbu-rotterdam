from framework.controller import *
import giveaminute.location as mLocation
import giveaminute.user as mUser
import giveaminute.project as mProject

class Home(Controller):
    def GET(self, action=None, page=None):
        self.template_data['project_user'] = dict(is_member = True,
                                                is_project_admin = True)          
                                          
        if (not action or action == 'home'):
            return self.showHome()
        elif (action == 'project'):
            return self.showProject(page)                                        
        else:
            return self.render(action)
            
            
    def POST(self, action=None):
        if (action == 'login'):
             return self.login()
        elif (action == 'logout'):
            return self.logout()
        else:
            return self.not_found()
            
            
    def showHome(self):
        #temp fix
#         locations = mLocation.getSimpleLocationDictionary(self.db)
#         allIdeas = self.getAllProjectIdeas();
#         
#         locationsObj = dict(data = locations, json = self.json(locations))
#         allIdeasObj = dict(data = allIdeas, json = self.json(allIdeas))
        
#         self.template_data['locations'] = locationsObj
#         self.template_data['all_ideas'] = allIdeasObj
        
        locations = dict(data = mLocation.getSimpleLocationDictionary(self.db), json = self.json(mLocation.getSimpleLocationDictionary(self.db)))
        allIdeas = dict(data = self.getFeaturedProjectIdeas(), json = self.json(self.getFeaturedProjectIdeas()))
        
        self.template_data['locations'] = locations
        self.template_data['all_ideas'] = allIdeas
        
        return self.render('home', {'locations':locations, 'all_ideas':allIdeas})
        
    def showProject(self, projectId):
        if (not projectId or projectId == -1):
            projDictionary = mProject.getTestData()
        else:
            project = mProject.Project(self.db, project_id)
            
            projDictionary = project.getFullDictionary()
        
        self.template_data['project'] = dict(json = self.json(projDictionary), data = projDictionary)
        return self.render('project')
    
    def login(self):
        email = self.request("email")
        password = self.request("password")
        
        if (email and password):
            userId = mUser.authenticateUser(self.db, email, password)
                
            if (userId):        
                self.session.user_id = userId
                self.session.invalidate()
                
                return userId
            else:
                return False    
        else:
            log.warning("Missing email or password")                        
            return False
            
    def logout(self):
        self.session.kill()

        return True    
        
    def getFeaturedProjectIdeas(self):
        data = []
        
        sql = """select p.project_id, p.title from project p
                inner join featured_project fp on fp.project_id = p.project_id order by fp.ordinal"""
        
        featured = list(self.db.query(sql))
        
        for project in featured:
            data.append(dict(title = str(project.title),
                            ideas = self.getProjectIdeas(project.project_id, 30)))   
        
        return data
        
    def getProjectIdeas(self, projectId, limit):
        data = []
        betterData = []
        
        sql = """select i.idea_id, i.description as text, u.first_name as f_name, u.last_name as l_name, i.submission_type as submitted_by 
                from idea i
                inner join project__idea pi on pi.idea_id = i.idea_id and pi.project_id = $id
                left join user u on u.user_id = i.user_id
                limit $limit"""
                
        log.info("*** proj idea sql = %s" % sql)
                
        try:
            data = list(self.db.query(sql, {'id':projectId, 'limit':limit}))
        
            for item in data:
                betterData.append(dict(text = str(item.text),
                            f_name = str(item.f_name) if item.f_name else '',
                            l_name = str(item.l_name) if item.l_name else '',
                            submitted_by =  str(item.submitted_by)))   
        
        except Exception, e:
            log.info("*** couldn't get project ideas for home page")
            log.error(e)    
            
        return betterData
                
