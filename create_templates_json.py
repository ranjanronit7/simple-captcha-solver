import os
import pickle
import cv2
from dotenv import load_dotenv

load_dotenv()


# get list of immediate files in a directory
def get_subfiles(path):
    return next(os.walk(path))[2]


# create a json object with templates data
def create_templates_json(path):
    templates_json = list()
    filenames = get_subfiles(path)
    for filename in filenames:
        template_img = cv2.imread(os.path.join(path, filename), cv2.IMREAD_UNCHANGED)
        template_gray = 255 - template_img[:, :, 3]
        ret, template_binary = cv2.threshold(template_gray, 127, 255, cv2.THRESH_BINARY)
        template_binary_inverse = cv2.bitwise_not(template_binary)
        temp = dict()
        try:
            temp['value'] = int(filename.split('.')[0])
            temp['type'] = 'int'
        except:
            temp['value'] = filename.split('.')[0]
            temp['type'] = 'char'
        temp['imageDataArray'] = template_binary_inverse

        cv2.imshow('template_binary_inverse', template_binary_inverse)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        templates_json.append(temp)
    return templates_json


# save templates json data into file
def save_templates_json(templates_json):
    with open(os.getenv('TEMPLATES_JSON_PATH'), 'wb') as f:
        pickle.dump(templates_json, f)
    print('\nSaved templates.json successfully ...\n')


if __name__ == '__main__':
    templates_path = os.getenv('TEMPLATE_IMAGES_PATH')
    templates_json = create_templates_json(templates_path)
    save_templates_json(templates_json)
