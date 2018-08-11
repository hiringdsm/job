from database import db
from models.job import Job
from response import json_response
from validation import validate


values = ["user_id:integer", "company:string:min-3:max-100", "role:string:min-3:max-100",
          "featured:boolean:min-3:max-100", "link:string:min-3:max-100", "image:string:min-3:max-500"]

def get(id):
    if not id:
        return json_response(400, "You must provide an ID.")

    the_job = db.session.query(Job).get(id)

    if the_job:
        job_dict = {
            "user_id": the_job.user_id,
            "company": the_job.company,
            "role": the_job.role,
            "featured": the_job.featured,
            "link": the_job.link,
            "image": the_job.image
        }

        return json_response(200, job_dict)
    else:
        return json_response(404, "A Job was not found with that ID.")


def get_page(page):
    max = 2

    jobs = Job.query.paginate(int(page), max, error_out=False).items

    jobs_dict = []

    for j in jobs:
        jobs_dict.append({
            "user_id": j.user_id,
            "company": j.company,
            "role": j.role,
            "featured": j.featured,
            "image": j.image,
            "link": j.link
        })

    return json_response(200, jobs_dict)


def post(data):
    validation_errors = validate(values, data)

    # handle errors
    if validation_errors:
        return json_response(400, {"errors": validation_errors})

    # No validation errors...continue

    new_job = Job(data["user_id"], data["company"], data["role"], data["featured"], data["link"], data["image"])

    db.session.add(new_job)
    db.session.commit()

    return json_response(200, {"id": new_job.id, "msg": "You successfully created a job post."})


def delete(id):
    the_job = Job.query.filter_by(id=id)

    if the_job:
        the_job.delete()
        db.session.commit()
        db.session.flush()
        return json_response(200, "You have deleted a job.")
    else:
        return json_response(404, "No Job was found with that ID.")
