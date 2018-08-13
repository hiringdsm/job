from database import db
from models.job import Job
from response import json_response
from validation import validate
from flask import request
from werkzeug.utils import secure_filename


values = ["user_id:integer", "company:string:min-3:max-100", "role:string:min-3:max-100",
          "featured:boolean:min-3:max-100", "link:string:min-3:max-100", "location_id:integer"]

allowed_extensions = ["jpg", "jpeg", "png"]

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
            "image": the_job.image,
            "location_id": the_job.location_id
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
            "link": j.link,
            "location_id": j.location_id
        })

    return json_response(200, jobs_dict)


def post(data):
    validation_errors = validate(values, data)

    if "image" not in request.files:
        validation_errors.append("You must upload an image.")
    else:
        image_file = request.files["image"]
        if image_file.filename == "":
            validation_errors.append("No file selected.")
        else:
            ext = image_file.filename.split(".")[-1]
            if image_file and (ext in allowed_extensions):
                filename = secure_filename(image_file.filename)
                image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # handle errors
    if validation_errors:
        return json_response(400, {"errors": validation_errors})

    # No validation errors...continue

    new_job = Job(data["user_id"], data["company"], data["role"], 
                  data["featured"], data["link"], filename, data["location_id"])

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
