from rasa_core_sdk import Action
from rasa_core_sdk.events import *
from pony.orm import *

# from job_db_actions import get_task_for_technology, get_task_for_domain, get_domain_for_task, get_domain_for_technology, get_technology_for_domain, get_technology_for_task, get_domain_for_task_and_tech, get_task_for_domain_and_tech, get_technology_for_task_and_domain

jobs = [
    {"name": "Werkstudent Software-Entwicklung", "formOfEmployment": "werkstudent",
        "jobTask": ["entwickeln"], "domain": ["web", "mobile"], "technology": ["java ee", "java"]},

    {"name": "Webdesigner", "formOfEmployment": "vollzeit", "jobTask": [
        "designen"], "domain": ["web"], "technology": ["photoshop", "html", "css", "javascript"]},

    {"name": "Praktikant Webdesign", "formOfEmployment": "praktikum",
        "jobTask": "[designen]", "domain": ["web"], "technology": "photoshop"},

    {"name": "Frontend Developer", "formOfEmployment": "vollzeit", "jobTask": ["entwickeln", "designen"], "domain": ["web", "mobile", "frontend"], "technology": [
        "angular", "typescript", "javascript", "html", "css", "sass", "less", "react", "vue", "jquery", "npm", "buildtools", "photoshop", "illustrator", "sketch", "invision", "ui-test"]}

]

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)


class Task(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    technologies = Set('Technology')
    domains = Set('Domain')


class Technology(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    tasks = Set('Task')
    domains = Set('Domain')


class Domain(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    tasks = Set(Task)
    technologies = Set('Technology')
    otherDomains = Set('Domain', reverse='otherDomains')


db.generate_mapping(create_tables=True)


result = select(p for p in Technology)


# Get Tasks for Technology
@db_session
def get_task_for_technology(inTech):
    taskName = []

    if inTech is not None:
        for techResult in inTech:
            techResult = techResult.lower()
            result = select(
                tech for tech in Technology if tech.name == techResult)[:]
            for tech in result:
                for task in tech.tasks:
                    if task.name not in taskName:
                        taskName.append(task.name)
        print("TaskForTech: ", taskName)
        return taskName

    else:
        return []


# Get Domains for Technology
@db_session
def get_domain_for_technology(inTech):
    domainName = []

    if inTech is not None:
        for techResult in inTech:
            techResult = techResult.lower()
            result = select(
                tech for tech in Technology if tech.name == techResult)[:]
            for tech in result:
                for domain in tech.domains:
                    if domain.name not in domainName:
                        domainName.append(domain.name)
        print("DomainForTech: ", domainName)
        return domainName

    else:
        return []


# Get Technology for Task
@db_session
def get_technology_for_task(inTask):
    technologyName = []

    if inTask is not None:
        for taskResult in inTask:
            taskResult = taskResult.lower()
            result = select(
                task for task in Task if task.name == taskResult)[:]
            for task in result:
                for technology in task.technologies:
                    if technology.name not in technologyName:
                        technologyName.append(technology.name)
        print("TechnologyForTask: ", technologyName)
        return technologyName

    else:
        return []


# Get Domain for Task
@db_session
def get_domain_for_task(inTask):
    domainName = []

    if inTask is not None:
        for taskResult in inTask:
            taskResult = taskResult.lower()
            result = select(
                task for task in Task if task.name == taskResult)[:]
            for task in result:
                for domain in task.domains:
                    if domain.name not in domainName:
                        domainName.append(domain.name)
        print("DomainForTask: ", domainName)
        return domainName

    else:
        return []


# Get Technology for Domain
@db_session
def get_technology_for_domain(inDomain):
    technologyName = []

    if inDomain is not None:
        for domainResult in inDomain:
            domainResult = domainResult.lower()
            result = select(
                domain for domain in Domain if domain.name == domainResult)[:]
            for domain in result:
                for technology in domain.technologies:
                    if technology.name not in technologyName:
                        technologyName.append(technology.name)
        print("TechnologyForDomain: ", technologyName)
        return technologyName

    else:
        return []


# Get Task for Domain
@db_session
def get_task_for_domain(inDomain):
    taskName = []
    if inDomain is not None:
        for domainResult in inDomain:
            domainResult = domainResult.lower()
            result = select(
                domain for domain in Domain if domain.name == domainResult)[:]
            for domain in result:
                for task in domain.tasks:
                    if task.name not in taskName:
                        taskName.append(task.name)
        print("TaskForDomain: ", taskName)
        return taskName

    else:
        return []


# Get Task for Domain and Technology
@db_session
def get_task_for_domain_and_tech(inDomain, inTech):

    if inDomain is not None and inTech is not None:

        taskNameinDomain = get_task_for_domain(inDomain)
        taskNameinTech = get_task_for_technology(inTech)

        if taskNameinDomain is not None and taskNameinTech is not None:
            tasksInCommon = list(
                set(taskNameinDomain).intersection(taskNameinTech))
            print(tasksInCommon)
            return tasksInCommon
        else:
            return []

    else:
        return []


# Get Domain for Task and Technology
@db_session
def get_domain_for_task_and_tech(inTask, inTech):

    if inTask is not None and inTech is not None:
        domainNameinTask = get_domain_for_task(inTask)
        domainNameinTech = get_domain_for_technology(inTech)

        if domainNameinTask is not None and domainNameinTech is not None:
            domainsInCommon = list(
                set(domainNameinTask).intersection(domainNameinTech))
            print(domainsInCommon)
            return domainsInCommon
        else:
            return []

    else:
        return []


# Get Technology for Task and Domain
@db_session
def get_technology_for_task_and_domain(inTask, inDomain):

    if inTask is not None and inDomain is not None:
        techNameinTask = get_technology_for_task(inTask)
        techNameinDomain = get_technology_for_domain(inDomain)

        if techNameinTask is not None and techNameinDomain is not None:
            techsInCommon = list(
                set(techNameinTask).intersection(techNameinDomain))
            print(techsInCommon)
            return techsInCommon
        else:
            return []

    else:
        return []


# Populate Database
@db_session
def populate_database():

    # Tasks
    entwickeln = Task(name='entwickeln')
    designen = Task(name='designen')
    administrieren = Task(name='administrieren')
    coachen = Task(name='coachen')
    analysieren = Task(name='analysieren')

    # Domains
    web = Domain(name="web", tasks=[entwickeln,
                                    designen, coachen], otherDomains=[])
    mobile = Domain(name="mobile", tasks=[
        entwickeln, designen, coachen], otherDomains=[])
    backend = Domain(name="backend", tasks=[
        entwickeln, coachen], otherDomains=[])
    devops = Domain(name="devops", tasks=[
        entwickeln, coachen], otherDomains=[])
    frontend = Domain(name="frontend", tasks=[
        entwickeln, designen, coachen], otherDomains=[web, mobile])
    fullstack = Domain(name="fullstack", tasks=[entwickeln, coachen], otherDomains=[
        web, mobile, backend, frontend])
    agile = Domain(name="agile", tasks=[coachen, entwickeln], otherDomains=[])
    data_science = Domain(name="data science", tasks=[
        analysieren, ], otherDomains=[])
    security = Domain(name="security", tasks=[
        analysieren, entwickeln], otherDomains=[])
    personal = Domain(name="personal", tasks=[administrieren], otherDomains=[])
    business = Domain(name="business", tasks=[
        administrieren, designen, analysieren], otherDomains=[])
    finanzen = Domain(name="finanzen", tasks=[
        administrieren, analysieren], otherDomains=[])
    machine_learning = Domain(name="machine learning", tasks=[
        entwickeln, analysieren], otherDomains=[])
    testing = Domain(name="testing", tasks=[
        entwickeln, analysieren], otherDomains=[])
    recht = Domain(name="recht", tasks=[administrieren], otherDomains=[])
    consulting = Domain(name="consulting", tasks=[], otherDomains=[])
    marketing = Domain(name="marketing", tasks=[], otherDomains=[])

    # Technologies
    angular = Technology(name='angular', tasks=[
        entwickeln], domains=[frontend, web, fullstack])
    java = Technology(name='java', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, mobile, web])
    spring = Technology(name='spring', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, web])
    kotlin = Technology(name='kotlin', tasks=[entwickeln], domains=[
        backend, fullstack, mobile])
    android = Technology(name='android', tasks=[entwickeln], domains=[
        backend, fullstack, mobile])
    swift = Technology(name='swift', tasks=[entwickeln], domains=[
        backend, fullstack, mobile])
    ios = Technology(name='ios', tasks=[entwickeln], domains=[
        backend, fullstack, mobile])
    typescript = Technology(name='typescript', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, mobile, web])
    javascript = Technology(name='javascript', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, mobile, web])
    html = Technology(name='html', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, web])
    css = Technology(name='css', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, web])
    sass = Technology(name='sass', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, web])
    less = Technology(name='less', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, web])
    react = Technology(name='react', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, backend, web])
    vue = Technology(name='vue', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, backend, web])
    jquery = Technology(name='jquery', tasks=[entwickeln], domains=[
        frontend, fullstack, mobile, web])
    nodejs = Technology(name='nodejs', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, mobile, web, machine_learning])
    npm = Technology(name='npm', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, mobile, web])
    python = Technology(name='python', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, web, machine_learning, data_science])
    c = Technology(name='c', tasks=[entwickeln], domains=[backend, fullstack])
    build_tools = Technology(name='build tools', tasks=[entwickeln], domains=[
        frontend, backend, fullstack, mobile, web])
    csharp = Technology(name='c#', tasks=[entwickeln], domains=[
        backend, fullstack])
    nlu = Technology(name='Natural Language Understanding', tasks=[
        entwickeln], domains=[machine_learning])
    nlp = Technology(name='Natural Language Processing', tasks=[
        entwickeln], domains=[machine_learning])
    tensorflow = Technology(name='tensorflow', tasks=[entwickeln], domains=[
        machine_learning, data_science])
    scikit_learn = Technology(
        name='scikit-learn', tasks=[entwickeln], domains=[data_science, machine_learning])
    rasa = Technology(name='rasa', tasks=[entwickeln], domains=[
        mobile, backend, fullstack, machine_learning])
    cui = Technology(name='cui', tasks=[entwickeln], domains=[
        mobile, backend, fullstack, machine_learning])
    dialogflow = Technology(name='dialogflow', tasks=[entwickeln], domains=[
        mobile, backend, fullstack, machine_learning])
    alexa = Technology(name='alexa', tasks=[entwickeln], domains=[
        mobile, backend, fullstack, machine_learning])
    snips = Technology(name='snips', tasks=[
        entwickeln], domains=[machine_learning])
    clustering = Technology(name='clustering', tasks=[entwickeln], domains=[
        machine_learning, data_science])
    watson = Technology(name='watson', tasks=[
        entwickeln], domains=[machine_learning])
    azure = Technology(name='azure', tasks=[
        entwickeln], domains=[machine_learning])

    softwarearchitektur = Technology(name='softwarearchitektur', tasks=[
        entwickeln], domains=[backend, fullstack, mobile, web, frontend, testing])
    arc42 = Technology(name='arc42', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, frontend, testing])

    sql = Technology(name='sql', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    nosql = Technology(name='nosql', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    mysql = Technology(name='mysql', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    sqlite = Technology(name='sqlite', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    postgresql = Technology(name='postgresql', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    mongodb = Technology(name='mongodb', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    couchdb = Technology(name='couchdb', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])
    nofs = Technology(name='nofs', tasks=[entwickeln], domains=[
        backend, fullstack, mobile, web, testing, data_science])

    verschlüsselung = Technology(name='verschlüsselung', tasks=[
        entwickeln], domains=[security])

    docker = Technology(name='docker', tasks=[entwickeln], domains=[devops])
    openshift = Technology(name='openshift', tasks=[
        entwickeln], domains=[devops])
    ci = Technology(name='continuous integration', tasks=[
        entwickeln], domains=[devops])
    cd = Technology(name='continuous deployment', tasks=[
        entwickeln], domains=[devops])
    config_management = Technology(name='releasemanagement', tasks=[
        entwickeln], domains=[devops])
    release_management = Technology(name='konfigurationsmanagement', tasks=[
        entwickeln], domains=[devops])
    systemadministration = Technology(name='systemadministration', tasks=[
        entwickeln, administrieren], domains=[devops])
    systemintegration = Technology(name='systemintegration', tasks=[
        entwickeln], domains=[devops])

    software_testing = Technology(name='softwaretesting', tasks=[
        entwickeln], domains=[testing])
    teststrategie = Technology(name='teststrategie', tasks=[
        entwickeln], domains=[testing])
    testautomatisierung = Technology(name='testautomatisierung', tasks=[
        entwickeln], domains=[testing])
    cucumber = Technology(name='cucumber', tasks=[
        entwickeln], domains=[testing])
    mocha = Technology(name='mocha', tasks=[
        entwickeln], domains=[testing])
    chai = Technology(name='chai', tasks=[
        entwickeln], domains=[testing])
    supertest = Technology(name='supertest', tasks=[
        entwickeln], domains=[testing])
    unit_test = Technology(name='unit test', tasks=[
        entwickeln], domains=[testing])
    integrationstest = Technology(name='integrationstest', tasks=[
        entwickeln], domains=[testing])
    end_to_end_test = Technology(name='end-to-end test', tasks=[
        entwickeln], domains=[testing]),
    ui_test = Technology(name='ui-test', tasks=[
        entwickeln, designen], domains=[testing, frontend, web, mobile])

    accessibility = Technology(name='accessibility', tasks=[
        designen, entwickeln, coachen], domains=[web, mobile, frontend, fullstack, testing])
    usability = Technology(name='usability', tasks=[
        designen, entwickeln, coachen], domains=[web, mobile, frontend, fullstack, testing])
    design_thinking = Technology(name='design thinking', tasks=[
        designen, entwickeln, coachen, analysieren], domains=[web, mobile, frontend, fullstack, testing])

    photoshop = Technology(name='photoshop', tasks=[
        designen], domains=[web, mobile, frontend])
    illustrator = Technology(name='illustrator', tasks=[
        designen], domains=[web, mobile, frontend])
    indesign = Technology(name='indesign', tasks=[
        designen], domains=[web, mobile, frontend])
    sketch = Technology(name='sketch', tasks=[
        designen], domains=[web, mobile, frontend])
    invison = Technology(name='invison', tasks=[
        designen], domains=[web, mobile, frontend])

    office = Technology(name='office', tasks=[
        administrieren], domains=[personal, business, finanzen, recht])
    word = Technology(name='word', tasks=[
        administrieren], domains=[personal, business, finanzen, recht])
    excel = Technology(name='excel', tasks=[
        administrieren], domains=[personal, business, finanzen, recht])
    powerpoint = Technology(name='powerpoint', tasks=[
        administrieren], domains=[personal, business, finanzen, recht])

    prozessdesign = Technology(name='prozessdesign', tasks=[
        administrieren, designen], domains=[business])
    prozessanalyse = Technology(name='prozessanalyse', tasks=[
        administrieren, analysieren], domains=[business])
    businessanalyse = Technology(name='businessanalyse', tasks=[
        administrieren, analysieren], domains=[business])
    geschäftsmodell = Technology(name='geschäftsmodell', tasks=[
        administrieren, analysieren], domains=[business])
    strategieberatung = Technology(name='strategieberatung', tasks=[
        administrieren, analysieren], domains=[business])
    bewerbermanagement = Technology(name='bewerbermanagement', tasks=[
        administrieren], domains=[personal])
    weiterbildungsmanagement = Technology(name='weiterbildungsmanagement', tasks=[
        administrieren], domains=[personal])
    personalverwaltung = Technology(name='personalverwaltung', tasks=[
        administrieren], domains=[personal])
    projektplan = Technology(name='projektplan', tasks=[
        administrieren], domains=[business])
    gantt = Technology(name='gantt', tasks=[
        administrieren], domains=[business])
    requirements_engineering = Technology(name='requirements engineering', tasks=[
        administrieren, analysieren, entwickeln], domains=[business])
    projektmanagement = Technology(name='projektmanagement', tasks=[
        administrieren], domains=[business])

    controlling = Technology(name='controlling', tasks=[
        administrieren], domains=[finanzen])
    buchführung = Technology(name='buchführung', tasks=[
        administrieren], domains=[finanzen])
    buchhaltung = Technology(name='buchhaltung', tasks=[
        administrieren], domains=[finanzen])

    arbeitsrecht = Technology(name='arbeitsrecht', tasks=[
        administrieren], domains=[recht])
    steuerrecht = Technology(name='steuerrecht', tasks=[
        administrieren], domains=[recht])
    sozialversicherungsrecht = Technology(name='sozialversicherungsrecht', tasks=[
        administrieren], domains=[recht])

    workshop = Technology(name='workshop', tasks=[
        coachen], domains=[agile])
    schulung = Technology(name='schulung', tasks=[
        coachen], domains=[agile])
    scrum = Technology(name='scrum', tasks=[
        coachen, entwickeln], domains=[agile])
    kanban = Technology(name='kanban', tasks=[
        coachen, entwickeln], domains=[agile])

    commit()

class ActionFindExistingJob(Action):

    def name(self):
        # type: () -> Text
        return "action_find_job"

    def run(self, dispatcher, tracker, domain):
        foundJobs = []

        # Store the values of slots given by the user with the tracker object
        taskSlot = tracker.get_slot('jobTask')
        domainSlot = tracker.get_slot('domain')
        technologySlot = tracker.get_slot('technology')
        formOfEmploymentSlot = tracker.get_slot('formOfEmployment')

        for job in jobs:
            # Store the values of each key for all job dictionaries in the jobs list
            tech = job["technology"]
            task = job["jobTask"]
            domain = job["domain"]
            employment = job["formOfEmployment"]

            # Search for matches between slots sent by the user and stored jobs in the jobs list.
            # If a job has at least one value for each key in the dictionary the job is appended to the foundJobs list.
            if [i.lower() for i in technologySlot if i.lower() in tech] and \
                [i.lower() for i in domainSlot if i.lower() in domain] and \
                [i.lower() for i in taskSlot if i.lower() in task] and \
                    [i.lower() for i in formOfEmploymentSlot if i.lower() in employment]:
                foundJobs.append(job)

        if len(foundJobs) >= 1:
            # Create a message for the user with a list of names of all found jobs, separated by comma
            jobMessage = ", ".join([c["name"] for c in foundJobs])

            # Send message with all found jobs to the user with the dispatcher object
            dispatcher.utter_message("Ich habe folgende Stellenanzeigen für dich gefunden:")
            dispatcher.utter_message("{}".format(jobMessage))

            # Set jobs slot with all found jobs
            return [SlotSet("jobs", foundJobs if foundJobs is not None else [])]
        else:
            return[FollowupAction("utter_askSpeculativeApplication")]


class ActionShowTechnologies(Action):

    def name(self):
        # type: () -> Text
        return "action_show_technologies"

    def run(self, dispatcher, tracker, domain):

        # Store the values of slots given by the user with the tracker object
        possibleTechnologySlot = tracker.get_slot('possibleTechnologies')

        if possibleTechnologySlot == None:
            possibleTechnologySlot = ["JavaScript", "Kotlin", "Photoshop", "SCRUM", "Docker", "Projektmanagement"]

        technologyMessage = ', '.join(possibleTechnologySlot[:6])

        # Send message to user with the dispatcher object
        dispatcher.utter_message(
            "Mögliche Technologien sind z.B.: " + technologyMessage + ".")

        return [FollowupAction("utter_askTechnology")]


class ActionMatchJobSlots(Action):
    def name(self):
        # type: () -> Text
        return "action_match_job_slots"

    def run(self, dispatcher, tracker, domain):
        foundJobsByName = []

        # Store the values of slots given by the user with the tracker object
        taskSlot = tracker.get_slot('jobTask')
        domainSlot = tracker.get_slot('domain')
        technologySlot = tracker.get_slot('technology')
        latest_message = (tracker.latest_message)['text']

    # search for jobName in latest user utterance
        for job in jobs:
            # Store the name for all job dictionaries in the jobs list
            jobName = job["name"]

            if(jobName in latest_message):
                foundJobsByName.append(job)

        if len(foundJobsByName) >= 1:
            jobMessage = ", ".join([c["name"] for c in foundJobsByName])

            # Send message with all found jobs to the user with the dispatcher object
            dispatcher.utter_message(
                "Ich habe folgende Jobs für dich gefunden:")
            dispatcher.utter_message("{}".format(jobMessage))

            # Set jobs slot with all found jobs
            return [SlotSet("jobs", foundJobsByName if foundJobsByName is not None else []), FollowupAction("action_listen")]

    # if no job could be found in the users utterance proceed with questions
        else:
            # for given task and domain: ask for technologies
            if taskSlot is not None and domainSlot is not None:

                possibleTechnologies = get_technology_for_task_and_domain(
                    taskSlot, domainSlot)

                return [
                    SlotSet("possibleTechnologies", possibleTechnologies),
                    FollowupAction("utter_askTechnology")]

            # for given task and technology: differentiate between 1 or more than 1 possible domain
            elif taskSlot is not None and technologySlot is not None:

                possibleDomains = get_domain_for_task_and_tech(
                    taskSlot, technologySlot)

                # if only 1 domain is possible: automatically set it and proceed with utter_askFormOfEmployment
                if len(possibleDomains) == 1:
                    return [
                        SlotSet("domain", possibleDomains),
                        FollowupAction("utter_askFormOfEmployment")]

                # if no domain is possible:
                elif len(possibleDomains) == 0:
                    return [FollowupAction("utter_askSpeculativeApplication")]

                # if more than 1 domain is possible: ask for domain
                else:

                    message = "Für welches dieser Gebiete interessiert du dich am meisten?"
                    buttons = []
                    for possDomain in possibleDomains:
                        payload = (
                            '/enter_data{\"domain\":' + '\"' + possDomain + '\"}')
                        buttons.append(
                            {"title": possDomain, "payload": payload})
                    dispatcher.utter_button_message(message, buttons)

                    return [
                        SlotSet("possibleDomains", possibleDomains)]

            # for given domain and technology: differentiate between 1 or more than 1 possible task
            elif domainSlot is not None and technologySlot is not None:

                possibleTasks = get_task_for_domain_and_tech(
                    domainSlot, technologySlot)

                # if only 1 task is possible: automatically set it and proceed with utter_askFormOfEmployment
                if len(possibleTasks) == 1:
                    return [
                        SlotSet("jobTask", possibleTasks),
                        FollowupAction("utter_askFormOfEmployment")]

                # if no task is possible:
                elif len(possibleTasks) == 0:
                    return [FollowupAction("utter_askSpeculativeApplication")]

                # if more than 1 task is possible: ask for task
                else:
                    message = "Welche dieser Tätigkeiten beschreibt deine gesucht Stelle am besten?"
                    buttons = []
                    for possTask in possibleTasks:
                        payload = (
                            '/enter_data{\"jobTask\":' + '\"' + possTask + '\"}')
                        buttons.append({"title": possTask, "payload": payload})
                    dispatcher.utter_button_message(message, buttons)

                    return [
                        SlotSet("possibleTasks", possibleTasks),
                        FollowupAction("action_listen")]

            elif taskSlot is not None:

                possibleDomains = get_domain_for_task(taskSlot)
                possibleTechnologies = get_technology_for_task(taskSlot)

                # if only 1 domain is possible: automatically set it and ask for technology
                if len(possibleDomains) == 1:
                    return[
                        SlotSet("possibleTechnologies", possibleTechnologies),
                        SlotSet("domain", possibleDomains),
                        FollowupAction("utter_askTechnology")]

                # if no domain is possible:
                elif len(possibleDomains) == 0:
                    return [FollowupAction("utter_askSpeculativeApplication")]

                # if more than 1 domain is possible: ask for technology
                else:
                    return [
                        SlotSet("possibleTechnologies", possibleTechnologies),
                        SlotSet("possibleDomains", possibleDomains),
                        FollowupAction("utter_askTechnology")]

            elif domainSlot is not None:

                possibleTasks = get_task_for_domain(domainSlot)
                possibleTechnologies = get_technology_for_domain(domainSlot)

                # if only 1 task is possible: automatically set it and ask for technology
                if len(possibleTasks) == 1:
                    return[
                        SlotSet("possibleTechnologies", possibleTechnologies),
                        SlotSet("jobTask", possibleTasks),
                        FollowupAction("utter_askTechnology")]

                # if no task is possible:
                elif len(possibleTasks) == 0:
                    return [FollowupAction("utter_askSpeculativeApplication")]

                # if more than 1 task is possible: ask for domain
                else:
                    return [
                        SlotSet("possibleTechnologies", possibleTechnologies),
                        SlotSet("possibleTasks", possibleTasks),
                        FollowupAction("utter_askTechnology")]

            elif technologySlot is not None:
                possibleDomains = get_domain_for_technology(technologySlot)
                possibleTasks = get_task_for_technology(technologySlot)

                # if only 1 task is possible and only 1 domain is possible:
                # automatically set both and proceed with utter_askFormOfEmployment
                if len(possibleTasks) == 1 and len(possibleDomains) == 1:
                    return [
                        SlotSet("jobTask", possibleTasks),
                        SlotSet("domain", possibleDomains),
                        FollowupAction("utter_askFormOfEmployment")]

                # if only 1 task is possible: automatically set it
                # ask for domain in form of buttons of all domains which are still possible
                elif len(possibleTasks) == 1:

                    message = "Für welches dieser Gebiete interessiert du dich am meisten?"
                    buttons = []
                    for possDomain in possibleDomains:
                        payload = (
                            '/enter_data{\"domain\":' + '\"' + possDomain + '\"}')
                        buttons.append(
                            {"title": possDomain, "payload": payload})
                    dispatcher.utter_button_message(message, buttons)

                    return [
                        SlotSet("jobTask", possibleTasks),
                        SlotSet("possibleDomains", possibleDomains),
                        FollowupAction("action_listen")]

                # if only 1 domain is possible: automatically set it
                # ask for task in form of buttons of all tasks which are still possible
                elif len(possibleDomains) == 1:

                    message = "Welche dieser Tätigkeiten beschreibt deine gesucht Stelle am besten?"
                    buttons = []
                    for possTask in possibleTasks:
                        payload = (
                            '/enter_data{\"jobTask\":' + '\"' + possTask + '\"}')
                        buttons.append({"title": possTask, "payload": payload})
                    dispatcher.utter_button_message(message, buttons)

                    return [
                        SlotSet("possibleTasks", possibleTasks),
                        SlotSet("domain", possibleDomains),
                        FollowupAction("action_listen")]

                # if no task is possible:
                elif ((len(possibleTasks) == 0) or (len(possibleDomains) == 0)):
                    return [FollowupAction("utter_askSpeculativeApplication")]

                # if non or more than 1 in both slots is possible:
                # ask for domain in form of buttons of all domains which are still possible
                else:
                    message = "Für welches dieser Gebiete interessiert du dich am meisten?"
                    buttons = []
                    for possDomain in possibleDomains:
                        payload = (
                            '/enter_data{\"domain\":' + '\"' + possDomain + '\"}')
                        buttons.append(
                            {"title": possDomain, "payload": payload})
                    dispatcher.utter_button_message(message, buttons)

                    return [
                        SlotSet("possibleTasks", possibleTasks),
                        SlotSet("possibleDomains", possibleDomains),
                        FollowupAction("action_listen")]
            return
