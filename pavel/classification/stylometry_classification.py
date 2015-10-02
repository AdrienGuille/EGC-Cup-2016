__author__ = 'Pavel Soriano'
__mail__ = 'sorianopavel@gmail.com'
from stylometry_classification.extract import *

def test_stylo():
    dickens1 = StyloDocument('/media/stuff/temp/stylo/stylometry/stylometry-data/Dickens/tale-two-cities-0.txt')
    dickens1.text_output()




def main():
    test_stylo()
    # my code here

if __name__ == "__main__":
    main()