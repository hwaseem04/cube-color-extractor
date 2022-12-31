import numpy as np

color_range = {'O_min': np.array([4,0,0]), 'O_max': np.array([7,255,255]),
               'W_min': np.array([0,0,0]), 'W_max': np.array([180,70,255]), 
               'B_min': np.array([82,0,0]), 'B_max': np.array([140,255,255]),
               'Y_min': np.array([16,0,0]), 'Y_max': np.array([40,255,255]),
               'R_min': np.array([0,0,0]), 'R_max': np.array([4,255,255]),
               'G_min': np.array([40,0,0]), 'G_max': np.array([80,255,255])}

def check_color_range(value):
    keys = list(color_range.keys())
    value = np.array(value)
    for i in range(len(color_range)):
        if (i % 2 == 0):
            if (value > color_range[keys[i]]).all() and (value < color_range[keys[i+1]]).all():
                if keys[i][0] == 'R':
                    return (0,50,255)
                elif keys[i][0] == 'O':
                    return (0,104,255)
                elif keys[i][0] == 'W':
                    return (255,255,255)
                elif keys[i][0] == 'B':
                    return (255,173,80)
                elif keys[i][0] == 'Y':
                    return (0,240,255)   
                elif keys[i][0] == 'G':
                    return (70,190,40)
    return None