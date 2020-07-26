[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

# Bubble Response Sheet Scanner and Tester

This is my own OMR sheet scanner and grader (even though it is not very good or complex). It takes an OMR sheet image file as an input and then performs several intermediate tasks to output the test score after comparing the user response and correct option.

## How to test-check my response sheet?
Simple, just upload an image in the project folder (after you've cloned it :-) ) and then run the following command from your terminal/ command prompt
<pre>
<code>
python3 test_grader.py --image "your-image-file-name-here"
</code>
</pre>

You can also change the number of questions and their correct responses by changing the **ANSWER_KEY** dictionary key and values.

## Example - 1

<img src='Screenshot (11).png' width=450 height=450>

## Example - 2

<img src='Screenshot (12).png', width=450 height=450>
