<!-- Most stories have been removed for privacy reasons. More data is needed for training than is available here. -->

## thankyou
* thankyou
    - utter_youarewelcome

#greet
* greet
    - utter_greet

## greet and confirm
* greet
    - utter_greet
* confirm
    - utter_askTechnology

## goodbye
* goodbye
    - utter_bye

## help
* help
    - utter_help

## Generated Story 7034160589158999056
* find_job{"jobTask": "entwickeln"}
    - slot{"jobTask": ["entwickeln"]}
    - action_match_job_slots
    - slot{"possibleTechnologies": ["typescript", "arc42", "requirements engineering", "sql", "scrum", "javascript", "nosql", "kanban", "mysql", "sqlite", "html", "postgresql", "css", "mongodb", "sass", "couchdb", "less", "nofs", "react", "verschl\u00fcsselung", "vue", "docker", "jquery", "ios", "openshift", "nodejs", "continuous integration", "npm", "continuous deployment", "python", "releasemanagement", "konfigurationsmanagement", "c", "build tools", "systemadministration", "c#", "systemintegration", "Natural Language Understanding", "software_testing", "Natural Language Processing", "teststrategie", "tensorflow", "testautomatisierung", "scikit-learn", "cucumber", "angular", "rasa", "mocha", "cui", "chai", "swift", "dialogflow", "supertest", "kotlin", "alexa", "unit test", "snips", "integrationstest", "java", "clustering", "end-to-end test", "android", "watson", "accessibility", "spring", "azure", "usability", "softwarearchitektur", "design thinking"]}
    - slot{"possibleDomains": ["web", "backend", "devops", "frontend", "testing", "security", "machine learning", "mobile", "fullstack", "agile"]}
    - followup{"name": "utter_askTechnology"}
    - utter_askTechnology
* enter_data{"technology": "CSS"}
    - slot{"technology": ["Angular", "TypeScript", "html", "CSS"]}
    - action_match_job_slots
    - slot{"possibleDomains": ["web", "frontend", "fullstack", "mobile", "backend"]}
    - followup{"name": "action_listen"}
* enter_data{"domain": "web"}
    - slot{"domain": ["web"]}
    - utter_askFormOfEmployment
* enter_data{"formOfEmployment": "vollzeit"}
    - slot{"formOfEmployment": ["vollzeit"]}
    - action_find_job
    - slot{"jobs": [{"domain": ["web", "mobile", "frontend"], "formOfEmployment": "vollzeit", "jobTask": ["entwickeln", "designen"], "name": "Frontend Developer", "technology": ["angular", "typescript", "javascript", "html", "css", "sass", "less", "react", "vue", "jquery", "npm", "buildtools", "photoshop", "illustrator", "sketch", "invision", "ui-test"]}]}

## Generated Story 2867705280703038743
* find_job{"jobTask": "entwickeln"}
    - slot{"jobTask": ["entwickeln"]}
    - action_match_job_slots
    - slot{"possibleTechnologies": ["watson", "softwarearchitektur", "design thinking", "arc42", "requirements engineering", "clustering", "sql", "scrum", "snips", "nosql", "kanban", "mysql", "alexa", "sqlite", "dialogflow", "postgresql", "cui", "mongodb", "android", "rasa", "couchdb", "nofs", "scikit-learn", "verschl\u00fcsselung", "swift", "tensorflow", "docker", "Natural Language Processing", "openshift", "Natural Language Understanding", "continuous integration", "continuous deployment", "releasemanagement", "azure", "c#", "konfigurationsmanagement", "build tools", "systemadministration", "spring", "c", "systemintegration", "python", "angular", "software_testing", "npm", "teststrategie", "kotlin", "nodejs", "testautomatisierung", "java", "jquery", "cucumber", "vue", "mocha", "typescript", "css", "chai", "supertest", "sass", "unit test", "html", "integrationstest", "react", "end-to-end test", "less", "accessibility", "ios", "javascript", "usability"]}
    - slot{"possibleDomains": ["web", "testing", "fullstack", "machine learning", "agile", "mobile", "security", "backend", "devops", "frontend"]}
    - followup{"name": "utter_askTechnology"}
    - utter_askTechnology
* enter_data{"technology": "React"}
    - slot{"technology": ["Vue", "React"]}
    - action_match_job_slots
    - slot{"possibleDomains": ["web", "frontend", "fullstack", "mobile", "backend"]}
    - followup{"name": "action_listen"}
* enter_data{"domain": "frontend"}
    - slot{"domain": ["frontend"]}
    - utter_askFormOfEmployment
* enter_data{"formOfEmployment": "vollzeit"}
    - slot{"formOfEmployment": ["vollzeit"]}
    - action_find_job
    - slot{"jobs": [{"domain": ["web", "mobile", "frontend"], "formOfEmployment": "vollzeit", "jobTask": ["entwickeln", "designen"], "name": "Frontend Developer", "technology": ["angular", "typescript", "javascript", "html", "css", "sass", "less", "react", "vue", "jquery", "npm", "buildtools", "photoshop", "illustrator", "sketch", "invision", "ui-test"]}]}

## Generated Story -8320867140332627399
* find_job{"jobTask": "entwickeln"}
    - slot{"jobTask": ["entwickeln"]}
    - action_match_job_slots
    - slot{"possibleTechnologies": ["html", "azure", "usability", "softwarearchitektur", "design thinking", "typescript", "arc42", "requirements engineering", "javascript", "sql", "scrum", "nosql", "kanban", "mysql", "css", "sqlite", "postgresql", "swift", "sass", "mongodb", "couchdb", "less", "nofs", "react", "verschl\u00fcsselung", "vue", "docker", "jquery", "openshift", "nodejs", "continuous integration", "continuous deployment", "npm", "python", "releasemanagement", "c", "konfigurationsmanagement", "build tools", "systemadministration", "ios", "c#", "systemintegration", "Natural Language Understanding", "software_testing", "Natural Language Processing", "teststrategie", "tensorflow", "testautomatisierung", "scikit-learn", "cucumber", "android", "rasa", "mocha", "angular", "cui", "chai", "dialogflow", "supertest", "alexa", "unit test", "kotlin", "snips", "integrationstest", "java", "clustering", "end-to-end test", "spring", "watson", "accessibility"]}
    - slot{"possibleDomains": ["agile", "mobile", "web", "security", "testing", "machine learning", "backend", "devops", "fullstack", "frontend"]}
    - followup{"name": "utter_askTechnology"}
    - utter_askTechnology
* enter_data{"technology": "Angular"}
    - slot{"technology": ["Angular"]}
    - action_match_job_slots
    - slot{"possibleDomains": ["fullstack", "frontend", "web"]}
* enter_data{"domain": "web"}
    - slot{"domain": ["web"]}
    - utter_askFormOfEmployment
* enter_data{"formOfEmployment": "vollzeit"}
    - slot{"formOfEmployment": ["vollzeit"]}
    - action_find_job
    - slot{"jobs": [{"domain": ["web", "mobile", "frontend"], "formOfEmployment": "vollzeit", "jobTask": ["entwickeln", "designen"], "name": "Frontend Developer", "technology": ["angular", "typescript", "javascript", "html", "css", "sass", "less", "react", "vue", "jquery", "npm", "buildtools", "photoshop", "illustrator", "sketch", "invision", "ui-test"]}]}

## Generated Story 5724709280556869179
* find_job{"domain": "frontend"}
    - slot{"domain": ["frontend"]}
    - action_match_job_slots
    - slot{"possibleTechnologies": ["vue", "illustrator", "spring", "arc42", "react", "angular", "softwarearchitektur", "less", "photoshop", "invison", "build tools", "typescript", "sass", "sketch", "python", "java", "css", "npm", "html", "design thinking", "nodejs", "javascript", "usability", "jquery", "indesign", "accessibility"]}
    - slot{"possibleTasks": ["designen", "entwickeln", "coachen"]}
    - followup{"name": "utter_askTechnology"}
    - utter_askTechnology
* ask_for_technologies
    - action_show_technologies
    - followup{"name": "utter_askTechnology"}
    - utter_askTechnology
* enter_data{"technology": "react"}
    - slot{"technology": ["angular", "Vue", "react"]}
    - action_match_job_slots
    - slot{"jobTask": ["entwickeln"]}
    - followup{"name": "utter_askFormOfEmployment"}
    - utter_askFormOfEmployment
* enter_data{"formOfEmployment": "vollzeit"}
    - slot{"formOfEmployment": ["vollzeit"]}
    - action_find_job
    - slot{"jobs": [{"domain": ["web", "mobile", "frontend"], "formOfEmployment": "vollzeit", "jobTask": ["entwickeln", "designen"], "name": "Frontend Developer", "technology": ["angular", "typescript", "javascript", "html", "css", "sass", "less", "react", "vue", "jquery", "npm", "buildtools", "photoshop", "illustrator", "sketch", "invision", "ui-test"]}]}

## Generated Story 723948800213092792
* confirm
    - utter_askTechnology
* ask_for_technologies
    - action_show_technologies
    - followup{"name": "utter_askTechnology"}
    - utter_askTechnology
* enter_data{"technology": "Kanban"}
    - slot{"technology": ["SCRUM", "Kanban"]}
    - action_match_job_slots
    - slot{"possibleTasks": ["coachen", "entwickeln"]}
    - slot{"domain": ["agile"]}
    - followup{"name": "action_listen"}
* enter_data{"jobTask": "coachen"}
    - slot{"jobTask": ["coachen"]}
    - utter_askFormOfEmployment
* enter_data{"formOfEmployment": "vollzeit"}
    - slot{"formOfEmployment": ["vollzeit"]}
    - action_find_job
    - followup{"name": "utter_askSpeculativeApplication"}
    - utter_askSpeculativeApplication
* confirm
    - utter_startSpeculativeApplication

## Generated Story -2672295187300215437
* ask_speculative_application
    - utter_startSpeculativeApplication
* thankyou
    - utter_youarewelcome

## Generated Story 2814679698059565295
* goodbye
    - utter_bye