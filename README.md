# Simple Captcha Solver

## Idea
This is a computer vision based solution to identify characters in a simple captcha.

The Captcha as shown in the figure below can be solved by creating template characters from the captcha images and using template matching algorithm to identify specific characters and then sequence estimation to get the final output. The entire process can be illustrated as follows:

![alt text](https://www.dropbox.com/s/hktg8w46gnvpcvd/simple-captcha-solver_1.png?raw=1)

## Getting Started
Clone the repository:

```$ git clone https://github.com/ranjanronit7/simple-captcha-solver.git```

### Dependencies
- Python 3.6
- cv2

### Generate Output
The captcha images can be collected by executing the following command:

```$ python collect_data.py```

The test results can be checked by running the proposed algorithm on all of the collected data as follows:

```$ python test.py```

The accuracy achieved should be close to **98%**