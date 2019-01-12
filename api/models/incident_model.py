from flask import json

redflag_table = []
intervention_table = []


class Incident():

    def __init__(self, **kwags):
        self.id = kwags['id']
        self.title = kwags['title']
        self.created_on = kwags['createdOn']
        self.comment = kwags['comment']
        self.created_by = kwags['createdBy']
        self.location = kwags['location']
        self.status = kwags['status']
        self.type = kwags['type']
        if 'images' in kwags:
            self.images = kwags['Images']
        if 'videos' in kwags:
            self.videos = kwags['Videos']

    def get_id(self):
        return self.id

    def to_string(self):
        return f'{self.id}, {self.title}, {self.comment}, {self.date}, {self.location}, {self.status}'

    def to_dict(self):
        return self.__dict__


class IncidentServices():

    def create_incident(self, Incident, incident_type):
        if incident_type == 'red-flag':
            redflag_table.append(Incident)
        elif incident_type == 'intervention':
            intervention_table.append(Incident)

    def count(self, incident_type):
        if incident_type == 'red-flag':
            return len(redflag_table)
        elif incident_type == 'intervention':
            return len(intervention_table)

    def get_next_id(self, incident_type):
        if incident_type == 'red-flag':
            return self.count('red-flag') + 1
        elif incident_type == 'intervention':
            return self.count('intervention') + 1

    def get_all(self, user_id, is_admin, incident_type):
        # check if user is admin
        if incident_type == 'red-flag' and is_admin:
            return [incident.__dict__ for incident in redflag_table]
        elif incident_type == 'red-flag' and not is_admin:
            return [incident.__dict__ for incident in redflag_table
                    if incident.created_by == user_id]

        if incident_type == 'intervention' and is_admin:
            return [incident.__dict__ for
                    incident in intervention_table]
        if incident_type == 'intervention' and not is_admin:
            return [incident.__dict__ for incident in intervention_table
                    if incident.created_by == user_id]

    def remove_all(self, incident_type):
        if incident_type == 'red-flag':
            redflag_table.clear()
        elif incident_type == 'intervention':
            intervention_table.clear()

    def get_incident(self, incident_id, incident_type):
        # covert flag item to dictionaties
        incidents = []
        if incident_type == 'red-flag':
            incidents = [incident for incident in
                         redflag_table if incident.id == incident_id]
        elif incident_type == 'intervention':
            incidents = [incident for incident in
                         intervention_table if incident.id == incident_id]

        if len(incidents) > 0:
            return incidents[0]

    def put_incident(self, existing_incident, update_incident, incident_type):
        keys = ['title', 'location', 'Images', 'Videos', 'createdOn', 'comment',
                'status']
        for key in keys:
            if hasattr(update_incident, key):
                setattr(existing_incident, key, getattr(update_incident, key))

    def patch_incident(self, existing_incident, update_incident, key):
        setattr(existing_incident, key, getattr(update_incident, key))

    def delete_incident(self, incident, incident_type):
        if incident_type == 'red-flag':
            redflag_table.remove(incident)
        elif incident_type == 'intervention':
            intervention_table.remove(incident)
