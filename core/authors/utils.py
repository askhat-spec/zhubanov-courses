import base64


def get_encoded_data(department, course, lecture):
    return {
            "department": base64.b64encode(department.encode('utf-8')).decode('ascii'),
            "course": base64.b64encode(course.encode('utf-8')).decode('ascii'),
            "lecture": base64.b64encode(lecture.encode('utf-8')).decode('ascii'),
            }