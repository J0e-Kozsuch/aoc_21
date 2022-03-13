

        
        
# calculate min of x
        
min_x = 14

# iterate from min of x to ~20 and calculate possibly y-values
all_max_height = 0



for x in range(5,50):
    for y in range(-10,1000):
        simulation_max_height = 0
        fell_in_target_area = False

        v_x = x
        v_y = y
        
        x_pos = 0
        y_pos = 0

        while y_pos >= -156 and x_pos <= 151:
            x_pos += v_x
            y_pos += v_y

            if v_x > 0:
                v_x -= 1
            v_y -= 1

            if y_pos > simulation_max_height:
                simulation_max_height = y_pos

            if x_pos >= 94 and y_pos<=-103 and y_pos >= -156 and x_pos <= 151:
                fell_in_target_area = True
                break

        if fell_in_target_area and simulation_max_height > all_max_height:
            all_max_height = simulation_max_height
            

            

         
    
