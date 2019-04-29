import json
import os
import errno


def save_file(file_path, file_content, file_type='txt'):
    if not os.path.exists(os.path.dirname(file_path)):
        try:
            os.makedirs(os.path.dirname(file_path))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    if file_type == 'txt':
        with open(file_path, "w") as f:
            f.write(file_content)
            f.truncate()
            # json.dump(item, f)

    if file_type == 'json':
        with open(file_path, "w") as f:
            json.dump(file_content, f)

    if file_type == 'img':
        with open(file_path, "wb") as f:
            f.write(file_content)
            f.truncate()
