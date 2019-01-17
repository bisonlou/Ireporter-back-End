from flask import json

redflag_table = []
intervention_table = []


class Incident():
    statuses = ['Pending', 'Under investigation', 'Resolved', 'Rejected']

    def __init__(self, **kwags):
        self._id = kwags['id']
        self._title = kwags['title']
        self._created_on = kwags['created_on']
        self._comment = kwags['comment']
        self._created_by = kwags['created_by']
        self._location = kwags['location']
        self._status = kwags['status']
        self._incident_type = kwags['type']
        self._images = kwags.get('images', list())
        self._videos = kwags.get('videos', list())

    @property
    def id(self):
        return self._id

    @property
    def created_on(self):
        return self._created_on

    @property
    def created_by(self):
        return self._created_by

    @property
    def title(self):
        return self._title

    @property
    def comment(self):
        return self._comment

    @property
    def location(self):
        return self._location

    @property
    def videos(self):
        return self._videos

    @property
    def images(self):
        return self._images

    @property
    def status(self):
        return self._status

    @created_on.setter
    def created_on(self, created_on):
        self._created_on = created_on

    @title.setter
    def title(self, title):
        self._title = title

    @comment.setter
    def comment(self, comment):
        self._comment = comment

    @location.setter
    def location(self, location):
        self._location = location

    @images.setter
    def images(self, images):
        self._images = images

    @videos.setter
    def videos(self, videos):
        self._videos = videos

    @status.setter
    def status(self, status):
        self._status = status

    def to_dict(self):
        return dict(id=self._id,
                    created_on=self._created_on,
                    created_by=self._created_by,
                    title=self._title,
                    comment=self._comment,
                    location=self._location,
                    type=self._incident_type,
                    status=self._status,
                    images=self._images,
                    videos=self._videos
                    )


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
        # check  incident type
        table = []
        if incident_type == 'red-flag':
            table = redflag_table
        if incident_type == 'intervention':
            table = intervention_table

        # check if user is admin
        if is_admin is True:
            return [incident.to_dict() for incident in table]
        else:
            return [incident.to_dict() for incident in table
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
        keys = ['title', 'location', 'images', 'videos', 'created_on',
                'comment', 'status']
        for key in keys:
            self.patch_incident(existing_incident, update_incident, key)

    def patch_incident(self, existing_incident, update_incident, key):
        setattr(existing_incident, key, getattr(update_incident, key))

    def delete_incident(self, incident, incident_type):
        if incident_type == 'red-flag':
            redflag_table.remove(incident)
        elif incident_type == 'intervention':
            intervention_table.remove(incident)

    def escalate_incident(self, incident):
        # get current status
        status = incident.status

        # increment status by 1 if status is less than 3
        if status < 3:
            status += 1

        # set new status
        incident.status = status

    def reject(self, incident):
        # set status to -1 to match last item in status list
        incident.status = -1
