# -*- coding: utf-8 -*-

from openpyxl.styles import Border, Side, PatternFill, Color, Alignment
from openpyxl.styles.fonts import Font
import os 

def createDirectory(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print("Error: Failed to create the directory.")


def border_styles():
    my_border = Border(left=Side(border_style='thin'),
                       right=Side(border_style='thin'),
                       top=Side(border_style='thin'),
                       bottom=Side(border_style='thin'),)
    return my_border
    
    
def font_styles():
    my_font = Font(bold=True)
    return my_font

def patternfill_styles(color_index):
    my_color = Color(indexed=color_index)
    my_patternfill = PatternFill(patternType='solid', fgColor=my_color)
    return my_patternfill

def alignment_styles():
    my_alignment = Alignment(horizontal="center", vertical="center")
    return my_alignment
