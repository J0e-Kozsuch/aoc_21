
velocity_count = 0


for x in range(14,152):
    for y in range(-156,1000):
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


            if x_pos >= 94 and y_pos<=-103 and y_pos >= -156 and x_pos <= 151:
                fell_in_target_area = True
                break

        if fell_in_target_area:
            velocity_count += 1
            

            

         
    
